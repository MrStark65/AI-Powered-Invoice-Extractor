"""PDF processing service for extracting invoice data."""

import re
from datetime import datetime
from typing import Dict, Optional, Any

import PyPDF2


class PDFProcessor:
    """Extracts structured data from invoice PDFs using regex patterns."""

    # ----------------- REGEX PATTERNS -----------------

    VENDOR_PATTERNS = [
        r'(?:from|vendor|company)[\s:]+([A-Z][A-Za-z\s&.,]+?)(?:\n|invoice)',
        r'^([A-Z][A-Za-z\s&.,]{3,30})',
    ]

    INVOICE_NUMBER_PATTERNS = [
        r'invoice\s*(?:number|#|no\.?)[\s:]*([A-Z0-9-]+)',
        r'(?:^|\n)(?:invoice|inv)[\s#:]*([A-Z0-9-]{3,})',
    ]

    DATE_PATTERNS = [
        r'(?:date|dated)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:date|dated)[\s:]*(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
        r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',
    ]

    # -------- UPDATED: more forgiving amount patterns --------
    AMOUNT_PATTERNS = [
        # Phrases + optional currency symbol + integer or decimal
        r'(?:grand\s*total|total\s*amount|amount\s*payable|net\s*amount|invoice\s*total)'
        r'\s*[:\-]?\s*([₹$€£]?\s*[0-9,]+(?:\.[0-9]{1,2})?)',

        # Generic "total/amount due/balance" lines
        r'(?:total|amount\s+due|balance)'
        r'\s*[:\-]?\s*([₹$€£]?\s*[0-9,]+(?:\.[0-9]{1,2})?)',

        # Any currency-prefixed number, anywhere
        r'[₹$€£]\s*([0-9,]+(?:\.[0-9]{1,2})?)',

        # Rs / INR formats
        r'(?:rs\.?|inr)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
    ]

    CURRENCY_PATTERNS = [
        # Currency codes
        r'\b(USD|EUR|GBP|CAD|AUD|INR|SGD|AED|JPY|CNY|HKD|MYR|THB)\b',
        # Currency symbols
        r'([\$€£₹¥])',
        # Indian specific
        r'\b(Rs\.?|INR|Rupees?)\b',
    ]

    CURRENCY_MAP = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '₹': 'INR',
        '¥': 'JPY',
        'Rs': 'INR',
        'Rs.': 'INR',
        'Rupee': 'INR',
        'Rupees': 'INR',
    }

    # Currency regions for classification
    CURRENCY_REGIONS = {
        'INR': {'region': 'India', 'symbol': '₹', 'name': 'Indian Rupee'},
        'USD': {'region': 'United States', 'symbol': '$', 'name': 'US Dollar'},
        'EUR': {'region': 'Europe', 'symbol': '€', 'name': 'Euro'},
        'GBP': {'region': 'United Kingdom', 'symbol': '£', 'name': 'British Pound'},
        'CAD': {'region': 'Canada', 'symbol': 'C$', 'name': 'Canadian Dollar'},
        'AUD': {'region': 'Australia', 'symbol': 'A$', 'name': 'Australian Dollar'},
        'SGD': {'region': 'Singapore', 'symbol': 'S$', 'name': 'Singapore Dollar'},
        'AED': {'region': 'UAE', 'symbol': 'د.إ', 'name': 'UAE Dirham'},
        'JPY': {'region': 'Japan', 'symbol': '¥', 'name': 'Japanese Yen'},
        'CNY': {'region': 'China', 'symbol': '¥', 'name': 'Chinese Yuan'},
        'HKD': {'region': 'Hong Kong', 'symbol': 'HK$', 'name': 'Hong Kong Dollar'},
        'MYR': {'region': 'Malaysia', 'symbol': 'RM', 'name': 'Malaysian Ringgit'},
        'THB': {'region': 'Thailand', 'symbol': '฿', 'name': 'Thai Baht'},
    }

    # Category detection patterns
    CATEGORY_PATTERNS = {
        'Food': r'(swiggy|zomato|dominos|pizza|restaurant|cafe|food|uber\s*eats)',
        'Shopping': r'(amazon|flipkart|myntra|ajio|shopping|retail)',
        'Bills': r'(electricity|water|gas|internet|broadband|utility|bill)',
        'Travel': r'(uber|ola|flight|hotel|booking|airbnb|travel)',
    }

    # ----------------- CORE HELPERS -----------------

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text() or ''
                    text += page_text + '\n'
                return text
        except Exception as e:
            raise RuntimeError(f"Failed to extract text: {e}")

    def _apply_patterns(self, text: str, patterns: list) -> Optional[str]:
        """Apply regex patterns until a match is found."""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return None

    def _normalize_date(self, date_str: str) -> str:
        """Normalize date to YYYY-MM-DD format."""
        date_formats = [
            '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d',
            '%m-%d-%Y', '%d-%m-%Y',
            '%d %b %Y', '%d %B %Y'
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        return date_str

    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float, handling Indian and international formats."""
        # Remove currency symbols and common separators
        cleaned = re.sub(r'[₹$€£¥,\s]', '', amount_str)
        # Remove 'Rs' or 'INR' text
        cleaned = re.sub(r'(Rs\.?|INR)', '', cleaned, flags=re.IGNORECASE)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def _fallback_amount(self, text: str) -> Optional[float]:
        """
        Fallback: pick the largest money-like number in the document.
        Handles formats like 4,339 or 4,128.82.
        """
        candidates = re.findall(
            r'([0-9]{1,3}(?:,[0-9]{2,3})*(?:\.[0-9]{1,2})?)',
            text
        )
        values = []
        for c in candidates:
            cleaned = re.sub(r'[₹$€£¥,\s]', '', c)
            try:
                v = float(cleaned)
                if v > 0:
                    values.append(v)
            except ValueError:
                continue

        return max(values) if values else None

    def _extract_currency(self, text: str) -> Optional[str]:
        """Extract and standardize currency with priority for Indian Rupee."""
        # Check for ₹ symbol first (highest priority for Indian invoices)
        if '₹' in text:
            return 'INR'

        # Check for Rs or Rupees
        if re.search(r'\b(Rs\.?|Rupees?|INR)\b', text, re.IGNORECASE):
            return 'INR'

        # Check other currency patterns
        currency = self._apply_patterns(text, self.CURRENCY_PATTERNS)
        if currency:
            mapped = self.CURRENCY_MAP.get(currency, currency)
            return mapped.upper()

        return None  # No default here; caller can decide

    def _detect_category(self, text: str, vendor: str) -> str:
        """Detect invoice category based on content."""
        combined_text = f"{text} {vendor}".lower()

        for category, pattern in self.CATEGORY_PATTERNS.items():
            if re.search(pattern, combined_text, re.IGNORECASE):
                return category

        return 'Others'

    def _is_invoice(self, text: str, vendor: str, invoice_number: str, amount: float) -> tuple:
        """Determine if PDF is actually an invoice and its status."""
        invoice_keywords = r'(invoice|bill|receipt|payment|due|total|amount)'
        has_invoice_keywords = bool(re.search(invoice_keywords, text, re.IGNORECASE))

        score = 0
        if vendor != 'N/A' and len(vendor) > 2:
            score += 1
        if invoice_number != 'N/A':
            score += 2
        if amount > 0:
            score += 2
        if has_invoice_keywords:
            score += 1

        if score >= 4:
            return 'Invoice', 'Complete'
        elif score >= 2:
            return 'Invoice', 'Partial data'
        else:
            return 'Not an invoice', 'N/A'

    # ----------------- MAIN ENTRYPOINT -----------------

    def extract_invoice_data(self, pdf_path: str) -> Dict[str, Any]:
        """Extract all invoice fields from PDF."""
        raw_text = self.extract_text_from_pdf(pdf_path)

        # Keep newlines (for ^ / MULTILINE), but collapse extra spaces/tabs
        text = re.sub(r'[ \t]+', ' ', raw_text)

        vendor = self._apply_patterns(text, self.VENDOR_PATTERNS) or 'N/A'
        invoice_number = self._apply_patterns(text, self.INVOICE_NUMBER_PATTERNS) or 'N/A'

        date_raw = self._apply_patterns(text, self.DATE_PATTERNS)
        date = self._normalize_date(date_raw) if date_raw else 'N/A'

        amount_raw = self._apply_patterns(text, self.AMOUNT_PATTERNS)
        if amount_raw:
            amount = self._parse_amount(amount_raw)
        else:
            # Fallback to largest numeric value
            fallback = self._fallback_amount(text)
            amount = fallback if fallback is not None else 0.0

        currency = self._extract_currency(text)
        if not currency and vendor != 'N/A':
            # Reasonable default for your use-case (India-focused)
            currency = 'INR'
        currency = currency or 'N/A'

        currency_info = self.CURRENCY_REGIONS.get(currency, {
            'region': 'Unknown',
            'symbol': currency,
            'name': currency
        })

        category = self._detect_category(text, vendor)

        invoice_type, status = self._is_invoice(text, vendor, invoice_number, amount)

        is_incomplete = (date == 'N/A' or amount == 0.0 or currency == 'N/A')

        return {
            'vendor_name': vendor,
            'invoice_number': invoice_number,
            'date': date,
            'total_amount': amount,
            'currency': currency,
            'currency_symbol': currency_info.get('symbol', currency),
            'currency_name': currency_info.get('name', currency),
            'currency_region': currency_info.get('region', 'Unknown'),
            'category': category,
            'invoice_type': invoice_type,
            'status': status,
            'is_incomplete': is_incomplete,
        }

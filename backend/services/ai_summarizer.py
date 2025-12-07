"""AI Summarization service for invoice insights using Groq."""

from typing import List, Dict
import os
from datetime import datetime


class AISummarizer:
    """Generates AI-powered insights and summaries from invoice data."""
    
    def __init__(self):
        """Initialize the AI summarizer."""
        self.ai_available = False
        self.client = None
        self.model_name = "llama-3.1-8b-instant"  # you can change model if needed
        
        try:
            from groq import Groq  # type: ignore
            # Get API key from environment variable - NEVER hardcode API keys!
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)
                self.ai_available = True
        except ImportError:
            # groq library not installed
            # pip install groq
            pass
    
    def generate_summary(self, invoices: List[Dict], statistics: Dict) -> Dict[str, str]:
        """Generate comprehensive AI summary of invoice data."""
        
        if self.ai_available:
            return self._generate_groq_summary(invoices, statistics)
        else:
            return self._generate_rule_based_summary(invoices, statistics)
    
    def _generate_groq_summary(self, invoices: List[Dict], statistics: Dict) -> Dict[str, str]:
        """Generate summary using Groq API."""
        try:
            # Filter only actual invoices
            valid_invoices = [inv for inv in invoices if inv.get("invoice_type") == "Invoice"]
            
            prompt = self._build_prompt(valid_invoices, statistics)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial analyst assistant that provides clear, "
                            "actionable insights about invoice data. Be concise and highlight key patterns."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            
            summary_text = response.choices[0].message.content.strip()
            
            return {
                "overview": self._extract_section(summary_text, "overview"),
                "spending_insights": self._extract_section(summary_text, "spending"),
                "recommendations": self._extract_section(summary_text, "recommendations"),
                "full_summary": summary_text,
                "ai_powered": True,
            }
        except Exception as e:
            print(f"Groq API error: {e}")
            return self._generate_rule_based_summary(invoices, statistics)
    
    def _build_prompt(self, invoices: List[Dict], statistics: Dict) -> str:
        """Build prompt for AI summarization."""
        # Aggregate data
        categories: Dict[str, float] = {}
        vendors: Dict[str, float] = {}
        currencies: Dict[str, float] = {}
        monthly_data: Dict[str, float] = {}
        
        for inv in invoices:
            amount = inv.get("total_amount", 0) or 0
            
            # Category totals
            cat = inv.get("category", "Others") or "Others"
            categories[cat] = categories.get(cat, 0.0) + float(amount)
            
            # Vendor totals
            vendor = inv.get("vendor_name", "Unknown") or "Unknown"
            if vendor != "N/A":
                vendors[vendor] = vendors.get(vendor, 0.0) + float(amount)
            
            # Currency totals
            curr = inv.get("currency", "N/A") or "N/A"
            if curr != "N/A":
                currencies[curr] = currencies.get(curr, 0.0) + float(amount)
            
            # Monthly data
            date_str = inv.get("date", "N/A") or "N/A"
            if date_str != "N/A":
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    month = date.strftime("%B %Y")
                    monthly_data[month] = monthly_data.get(month, 0.0) + float(amount)
                except Exception:
                    # Ignore invalid dates
                    pass
        
        prompt = f"""Analyze this invoice data and provide insights:

STATISTICS:
- Total Invoices: {statistics.get('valid_invoices', 0)}
- Complete: {statistics.get('complete_invoices', 0)}
- Incomplete: {statistics.get('incomplete_invoices', 0)}
- Total Spend: {statistics.get('total_spend', 0)}

SPENDING BY CATEGORY:
{self._format_dict(categories)}

TOP VENDORS:
{self._format_dict(dict(sorted(vendors.items(), key=lambda x: x[1], reverse=True)[:5]))}

CURRENCIES:
{self._format_dict(currencies)}

MONTHLY BREAKDOWN:
{self._format_dict(monthly_data)}

Please provide:
1. OVERVIEW: A brief 2-3 sentence summary of the overall spending pattern
2. SPENDING INSIGHTS: Key observations about categories, vendors, and trends
3. RECOMMENDATIONS: 2-3 actionable suggestions for better expense management

Format your response with clear sections and headings like:
OVERVIEW:
SPENDING INSIGHTS:
RECOMMENDATIONS:
"""
        
        return prompt
    
    def _format_dict(self, data: Dict) -> str:
        """Format dictionary for prompt."""
        if not data:
            return "None"
        
        lines = []
        for k, v in data.items():
            try:
                v_float = float(v)
                lines.append(f"- {k}: {v_float:.2f}")
            except (TypeError, ValueError):
                lines.append(f"- {k}: {v}")
        return "\n".join(lines)
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """
        Extract specific section from AI response.

        Looks for headings like:
        OVERVIEW:
        SPENDING INSIGHTS:
        RECOMMENDATIONS:
        """
        lines = text.split("\n")
        section_lines = []
        capturing = False
        section_name_lower = section_name.lower()
        
        for line in lines:
            clean = line.strip()
            lower = clean.lower()
            if not clean:
                if capturing:
                    section_lines.append("")  # keep paragraph breaks a bit
                continue
            
            # Start capturing when we see a heading that contains the section name
            if not capturing and section_name_lower in lower and ":" in clean:
                capturing = True
                continue
            
            # Stop when we hit another heading
            if capturing and any(
                key in lower for key in ["overview", "spending", "recommendations"]
            ) and ":" in clean:
                break
            
            if capturing:
                section_lines.append(clean)
        
        if not section_lines:
            # Fallback: just return first 200 chars
            return text[:200]
        
        # Join with spaces but preserve some separation
        return " ".join(section_lines).strip()
    
    def _generate_rule_based_summary(self, invoices: List[Dict], statistics: Dict) -> Dict[str, str]:
        """Generate summary using rule-based logic (fallback)."""
        valid_invoices = [inv for inv in invoices if inv.get("invoice_type") == "Invoice"]
        
        if not valid_invoices:
            return {
                "overview": "No valid invoices found to analyze.",
                "spending_insights": "Upload invoice PDFs to get detailed spending insights.",
                "recommendations": "Ensure your PDFs contain clear invoice information.",
                "full_summary": "No data available for analysis.",
                "ai_powered": False,
            }
        
        # Calculate insights
        total_spend = float(statistics.get("total_spend", 0) or 0)
        valid_count = int(statistics.get("valid_invoices", 0) or 0)
        avg_invoice = total_spend / valid_count if valid_count > 0 else 0
        
        # Category analysis
        categories: Dict[str, float] = {}
        for inv in valid_invoices:
            cat = inv.get("category", "Others") or "Others"
            amount = float(inv.get("total_amount", 0) or 0)
            categories[cat] = categories.get(cat, 0.0) + amount
        
        top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else "Unknown"
        top_category_amount = categories.get(top_category, 0.0)
        top_category_pct = (top_category_amount / total_spend * 100) if total_spend > 0 else 0
        
        # Currency analysis
        currencies_set = {
            inv.get("currency", "N/A")
            for inv in valid_invoices
            if inv.get("currency") not in (None, "", "N/A")
        }
        multi_currency = len(currencies_set) > 1
        
        # Vendor analysis
        vendors: Dict[str, float] = {}
        for inv in valid_invoices:
            vendor = inv.get("vendor_name", "Unknown") or "Unknown"
            if vendor != "N/A":
                amount = float(inv.get("total_amount", 0) or 0)
                vendors[vendor] = vendors.get(vendor, 0.0) + amount
        
        top_vendor = max(vendors.items(), key=lambda x: x[1])[0] if vendors else "Unknown"
        unique_vendors = len(vendors)
        
        # Incomplete data check
        incomplete_count = int(statistics.get("incomplete_invoices", 0) or 0)
        incomplete_pct = (incomplete_count / valid_count * 100) if valid_count > 0 else 0
        
        # Generate overview
        overview = f"You processed {valid_count} invoices with a total spend of {total_spend:.2f}. "
        overview += f"Your average invoice amount is {avg_invoice:.2f}. "
        if multi_currency:
            overview += f"Transactions span {len(currencies_set)} currencies ({', '.join(currencies_set)}). "
        else:
            overview += (
                f"All transactions are in {list(currencies_set)[0] if currencies_set else 'unknown currency'}. "
            )
        
        # Generate insights
        insights = (
            f"Your highest spending category is {top_category}, accounting for {top_category_pct:.1f}% "
            f"of total expenses. "
        )
        insights += (
            f"You have transactions with {unique_vendors} different vendors, "
            f"with {top_vendor} being your top vendor. "
        )
        
        if incomplete_pct > 20:
            insights += f"Note: {incomplete_pct:.0f}% of invoices have missing data (dates or amounts). "
        
        # Category-specific insights
        if "Food" in categories and categories["Food"] > total_spend * 0.3:
            insights += "Food delivery expenses are significant - consider meal planning to reduce costs. "
        if "Shopping" in categories and categories["Shopping"] > total_spend * 0.4:
            insights += "Shopping represents a large portion of spending - review for unnecessary purchases. "
        
        # Generate recommendations
        recommendations = []
        
        if incomplete_pct > 10:
            recommendations.append(
                f"Review and complete {incomplete_count} invoices with missing data for accurate tracking."
            )
        
        if top_category_pct > 50:
            recommendations.append(
                f"Consider setting a budget for {top_category} expenses as they dominate your spending."
            )
        
        if unique_vendors > 10:
            recommendations.append(
                f"You're using {unique_vendors} vendors - consolidating could help negotiate better rates."
            )
        
        if multi_currency:
            recommendations.append("Track currency exchange rates to optimize international payments.")
        
        if not recommendations:
            recommendations.append("Your spending is well-distributed across categories.")
            recommendations.append("Continue monitoring monthly trends for better financial planning.")
        
        recommendations_text = " ".join(recommendations)
        
        # Full summary
        full_summary = f"""
📊 SPENDING OVERVIEW
{overview}

💡 KEY INSIGHTS
{insights}

🎯 RECOMMENDATIONS
{recommendations_text}

📈 BREAKDOWN
- Total Invoices: {valid_count}
- Average Invoice: {avg_invoice:.2f}
- Top Category: {top_category} ({top_category_pct:.1f}%)
- Top Vendor: {top_vendor}
- Currencies: {', '.join(currencies_set) if currencies_set else 'None'}
"""
        
        return {
            "overview": overview.strip(),
            "spending_insights": insights.strip(),
            "recommendations": recommendations_text.strip(),
            "full_summary": full_summary.strip(),
            "ai_powered": False,
        }

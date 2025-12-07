# Indian Invoice Support Guide

This guide explains how the Invoice Extractor handles Indian invoices and currency detection.

## 🇮🇳 Indian Rupee (INR) Support

The system has **enhanced support** for Indian invoices with multiple detection methods:

### Currency Detection Priority

1. **₹ Symbol** (Highest Priority)
   - Detects the Rupee symbol directly
   - Example: `Total: ₹1,500.00`

2. **Rs. / Rs Text**
   - Recognizes "Rs." or "Rs" prefix
   - Example: `Amount: Rs. 2,500`

3. **INR Code**
   - Detects ISO currency code
   - Example: `Total: INR 3,000`

4. **Rupees Text**
   - Recognizes "Rupee" or "Rupees"
   - Example: `Amount: 1500 Rupees`

### Amount Parsing

The system handles Indian number formatting:
- Comma separators: `₹1,50,000` → 150000
- Decimal points: `₹1,500.50` → 1500.50
- Without symbols: `Rs. 2500` → 2500

## 📊 Currency Classification

All currencies are automatically classified by region:

| Currency | Code | Symbol | Region |
|----------|------|--------|--------|
| Indian Rupee | INR | ₹ | India |
| US Dollar | USD | $ | United States |
| Euro | EUR | € | Europe |
| British Pound | GBP | £ | United Kingdom |
| Canadian Dollar | CAD | C$ | Canada |
| Australian Dollar | AUD | A$ | Australia |
| Singapore Dollar | SGD | S$ | Singapore |
| UAE Dirham | AED | د.إ | UAE |
| Japanese Yen | JPY | ¥ | Japan |
| Chinese Yuan | CNY | ¥ | China |
| Hong Kong Dollar | HKD | HK$ | Hong Kong |
| Malaysian Ringgit | MYR | RM | Malaysia |
| Thai Baht | THB | ฿ | Thailand |

## 🎯 Features for Indian Invoices

### 1. Currency Breakdown
View spending by currency with:
- Total amount per currency
- Number of invoices
- Currency symbol and region
- Visual cards for each currency

### 2. Currency Filter
Filter invoices by currency:
- Select "INR" to see only Indian invoices
- Compare spending across currencies
- Identify multi-currency transactions

### 3. Region Display
Each invoice shows:
- Currency code (INR)
- Currency symbol (₹)
- Region (India)

## 📝 Sample Indian Invoice Formats

The system recognizes these common formats:

### Format 1: With ₹ Symbol
```
INVOICE

From: Swiggy
Invoice Number: SWG-12345
Date: 07/12/2024

Items:
- Biryani: ₹350
- Raita: ₹50

Total: ₹400
```

### Format 2: With Rs.
```
TAX INVOICE

Vendor: Flipkart
Invoice No: FLP-98765
Date: 07-12-2024

Subtotal: Rs. 2,500
GST (18%): Rs. 450
Grand Total: Rs. 2,950
```

### Format 3: With INR
```
BILL

Company: Zomato
Bill #: ZOM-54321
Date: 2024-12-07

Amount Due: INR 650.00
```

### Format 4: Text Format
```
RECEIPT

From: Local Store
Receipt: REC-001
Date: 07/12/2024

Total Amount: 1500 Rupees
```

## 🔍 Vendor Auto-Categorization

Indian vendors are automatically categorized:

### Food
- Swiggy, Zomato, Dominos
- Pizza Hut, KFC, McDonald's
- Local restaurants

### Shopping
- Amazon India, Flipkart
- Myntra, Ajio, Snapdeal
- BigBasket, Grofers

### Bills
- Electricity bills (BESCOM, MSEB, etc.)
- Internet/Broadband
- Water, Gas utilities

### Travel
- Uber, Ola
- IRCTC (Indian Railways)
- MakeMyTrip, Goibibo

## 💡 Tips for Best Results

### 1. PDF Quality
- Use text-based PDFs (not scanned images)
- Ensure text is selectable in the PDF
- Avoid heavily formatted or image-based invoices

### 2. Invoice Format
- Include clear labels: "Total", "Amount", "Invoice Number"
- Use standard date formats: DD/MM/YYYY or DD-MM-YYYY
- Include vendor name at the top

### 3. Currency Clarity
- Include ₹ symbol or "Rs." prefix
- Place currency near the amount
- Use consistent formatting

## 🚀 Advanced Features

### Multi-Currency Support
Process invoices in multiple currencies simultaneously:
- INR invoices from Indian vendors
- USD invoices from international vendors
- EUR invoices from European suppliers

### Currency Breakdown Dashboard
View comprehensive statistics:
- Total spend per currency
- Number of invoices per currency
- Regional distribution
- Visual comparison

### Smart Filtering
Filter and analyze:
- By currency (INR, USD, EUR, etc.)
- By category (Food, Shopping, Bills, Travel)
- By invoice type (Complete, Incomplete)
- By date range

## 📱 Mobile Support

Access from any device:
- Upload invoices from phone camera
- View currency breakdown on mobile
- Edit data on tablet
- Download reports on desktop

## 🔧 Troubleshooting

### Currency Not Detected
**Problem:** Currency shows as "N/A"

**Solutions:**
1. Check if PDF has ₹, Rs., or INR text
2. Ensure amount is near currency indicator
3. Verify PDF is text-based (not scanned)
4. Try adding currency manually in the table

### Wrong Currency Detected
**Problem:** INR invoice detected as USD

**Solutions:**
1. Check if $ symbol appears before ₹
2. Edit currency directly in the table
3. Re-download with corrected data

### Amount Not Extracted
**Problem:** Amount shows as 0

**Solutions:**
1. Look for "Total", "Amount Due", or "Grand Total" labels
2. Ensure amount has clear formatting
3. Check for comma/decimal separators
4. Edit amount manually if needed

## 📊 Example Output

For a set of Indian invoices, you'll see:

```
Currency Breakdown:
┌─────────────────────────────┐
│ ₹ INR                       │
│ Total: ₹15,450.00          │
│ Invoices: 8                 │
│ Region: India               │
└─────────────────────────────┘

┌─────────────────────────────┐
│ $ USD                       │
│ Total: $250.00             │
│ Invoices: 2                 │
│ Region: United States       │
└─────────────────────────────┘
```

## 🎓 Best Practices

1. **Organize by Currency**: Use currency filter to review INR invoices separately
2. **Verify Amounts**: Check that Indian number formatting is parsed correctly
3. **Edit if Needed**: Use inline editing to correct any misdetections
4. **Download Reports**: Export to Excel for detailed analysis
5. **Track by Category**: Monitor spending across Food, Shopping, Bills, Travel

## 🌟 Pro Tips

- **GST Invoices**: Works with GST-compliant Indian invoices
- **Multiple Vendors**: Handles various Indian vendor formats
- **Date Formats**: Supports DD/MM/YYYY (Indian standard)
- **Lakhs/Crores**: Parses amounts like ₹1,50,000 correctly
- **Regional Languages**: Works best with English text

---

**Need Help?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md) for setup instructions.

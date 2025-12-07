# 📄 Invoice & Bills Extractor

**A premium full-stack application for extracting financial data from invoice PDFs with AI-powered insights and beautiful visualizations.**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

### Core Functionality
- 📤 **Drag & Drop Upload** - Upload multiple invoice PDFs via modern web interface
- 🔍 **Smart Extraction** - Extract vendor name, invoice number, date, amount, and currency
- 📊 **Multiple Export Formats** - Generate CSV, Excel, and chart visualizations
- 📈 **Interactive Charts** - Real-time Chart.js visualizations with smooth animations
- 🎨 **Premium Dashboard** - Split-screen layout with glassmorphic design
- ⚡ **Fast Processing** - Async API with real-time progress updates

### Smart Features
- 🤖 **AI-Powered Insights** - Intelligent analysis of spending patterns with actionable recommendations
- 🏷️ **Auto-categorization** - Automatically categorizes invoices (Food, Shopping, Bills, Travel, Others)
- 🔍 **Invoice Detection** - Distinguishes between actual invoices and non-invoice PDFs
- ⚠️ **Data Validation** - Highlights incomplete data (missing dates, zero amounts)
- ✏️ **Inline Editing** - Edit extracted data directly in the table before downloading
- 🔄 **Filter & Sort** - Filter by category/type/currency, sort by any column
- 💰 **Smart Statistics** - Total spend, top vendor, biggest invoice, completion status
- 🌍 **Multi-currency Support** - Detects 13 currencies including INR (₹), USD, EUR, GBP
- 💱 **Currency Breakdown** - Visual breakdown by currency with regional classification
- 📊 **Summary Cards** - Neumorphic cards with key metrics

### Premium UI/UX
- 🎨 **Glassmorphism Design** - Frosted glass effects with backdrop blur
- ✨ **Micro-interactions** - Smooth animations and hover effects
- 📱 **Fully Responsive** - Optimized for mobile, tablet, and desktop
- 🎯 **Split-screen Layout** - Left sidebar for insights, right panel for data
- 🌈 **Gradient Accents** - Purple-to-violet brand gradient throughout
- 🔮 **Animated Background** - Moving dot pattern for depth
- 💎 **Neumorphic Cards** - Soft shadows creating 3D depth

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                  │
│  • Modern UI with Chart.js visualizations                   │
│  • Split-screen dashboard layout                            │
│  • Real-time data editing and filtering                     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI + Python)                 │
│  • PDF text extraction (PyPDF2)                             │
│  • Regex-based data parsing                                 │
│  • AI summarization (Graq/ Rule-based)               │
│  • CSV/Excel/Chart generation                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm

### Installation

**1. Clone the repository**
```bash
git clone <repository-url>
cd invoice-extractor
```

**2. Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**3. Install Frontend Dependencies**
```bash
cd frontend
npm install
```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python app.py
```
Backend runs on: `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

**3. Open in Browser:**
```
http://localhost:3000
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Upload Invoices**
   - Click the upload area or drag & drop PDF files
   - Select multiple invoices at once
   - See file list with selected items

2. **Extract Data**
   - Click "Extract Data" button
   - Watch real-time processing
   - View success banner when complete

3. **Explore Insights**
   - **Left Sidebar**: Summary cards, currency breakdown, AI insights
   - **Right Panel**: Interactive chart, data table, download options

4. **Review & Edit**
   - Click any table cell to edit
   - Filter by type, category, or currency
   - Sort by clicking column headers

5. **Download Results**
   - CSV for raw data
   - Excel for formatted spreadsheet
   - Chart image for presentations

---

## 🎨 UI Features

### Split-Screen Dashboard

**Left Sidebar (Sticky)**
- Summary Cards (Total Spend, Valid Invoices, Top Vendor, Biggest Invoice)
- Currency Breakdown (Multi-currency support with regional info)
- AI Insights (Overview, Spending Insights, Recommendations)
- Full AI Analysis (Expandable detailed report)

**Right Content Panel**
- Interactive Chart (Monthly spending trends with Chart.js)
- Download Actions (CSV, Excel, Chart image)
- Data Table (Sortable, filterable, editable)
- Status Information (Data quality indicators)

### Visual Design Elements

- **Glassmorphism**: Frosted glass containers with backdrop blur
- **Neumorphism**: Soft 3D shadows on cards
- **Gradient Accents**: Purple-to-violet brand colors
- **Animated Grid**: Moving dot pattern background
- **Smooth Transitions**: Cubic-bezier animations
- **Hover Effects**: Cards lift and scale on interaction
- **Color Psychology**: Green for success, red for warnings, blue for info

---

## 🤖 AI Features

### Two Modes of Operation

**1. Rule-Based Mode (Default - No Setup)**
- Works immediately out of the box
- Intelligent pattern analysis
- Category and vendor insights
- Spending recommendations
- Completely free

**2. AI-Powered Mode (Optional - Enhanced)**
- Uses OpenAI GPT-3.5 for advanced insights
- Natural language summaries
- Contextual recommendations
- Requires OpenAI API key (~$0.002 per summary)

### AI Insights Include

- **Overview**: High-level spending summary
- **Spending Insights**: Category breakdown, vendor analysis, trends
- **Recommendations**: Actionable suggestions for cost optimization
- **Full Analysis**: Detailed report with all findings

**Setup AI Mode:**
```bash
export OPENAI_API_KEY='your-api-key'
```

See [AI_SETUP.md](AI_SETUP.md) for detailed instructions.

---

## 💱 Currency Support

### Supported Currencies (13 Total)

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

### Indian Rupee (INR) Priority

The system has **enhanced support** for Indian invoices:
- ₹ symbol detection (highest priority)
- Rs., Rs, Rupees, Rupee text recognition
- Indian number formatting (₹1,50,000)
- GST-compliant invoice support

See [INDIAN_INVOICE_GUIDE.md](INDIAN_INVOICE_GUIDE.md) for details.

---

## 📊 Output Files

### Generated Files

1. **invoices.csv**
   - Raw extracted data in CSV format
   - All invoice fields in separate columns
   - Easy import into Excel, Google Sheets, etc.

2. **invoices_dashboard.xlsx**
   - Formatted Excel spreadsheet
   - Auto-adjusted column widths
   - Professional styling

3. **monthly_spending.png**
   - Bar chart showing spending by month
   - High-resolution (300 DPI)
   - Ready for presentations

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async web framework
- **PyPDF2** - PDF text extraction
- **pandas** - Data manipulation
- **openpyxl** - Excel file generation
- **matplotlib** - Chart generation
- **OpenAI** - AI-powered insights (optional)

### Frontend
- **React 18** - UI framework
- **Vite** - Fast build tool
- **Chart.js** - Interactive charts
- **Axios** - HTTP client
- **CSS3** - Glassmorphism & animations

---

## 📁 Project Structure

```
invoice-extractor/
├── backend/
│   ├── app.py                      # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   └── services/
│       ├── pdf_processor.py        # PDF extraction & parsing
│       ├── output_generator.py     # CSV/Excel/Chart generation
│       └── ai_summarizer.py        # AI insights (GPT/Rule-based)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── App.css                 # Premium styles
│   │   ├── main.jsx                # React entry point
│   │   └── index.css               # Global styles
│   ├── index.html                  # HTML template
│   ├── package.json                # Node dependencies
│   └── vite.config.js              # Vite configuration
│
├── README.md                       # This file
├── QUICKSTART.md                   # Quick setup guide
├── AI_SETUP.md                     # AI configuration guide
├── INDIAN_INVOICE_GUIDE.md         # INR support details
├── KIRO_CONTRIBUTION.md            # Kiro AI assistance details
└── EXAMPLE_AI_SUMMARY.md           # AI insights examples
```

---

## 🎯 Key Features Explained

### 1. Invoice Type Detection
Automatically identifies whether a PDF is actually an invoice:
- **Invoice**: Has vendor, invoice number, amount, and invoice keywords
- **Not an invoice**: Random PDFs like notes, receipts without amounts
- **Partial data**: Missing some fields but appears to be an invoice

### 2. Data Completeness Tracking
Rows with missing data are highlighted:
- Red background for cells with N/A or 0 values
- "Incomplete" badge for easy identification
- Status line shows: "X invoices complete · Y invoice(s) missing date/amount"

### 3. Smart Categorization
Automatic category detection based on vendor names:
- **Food**: Swiggy, Zomato, Dominos, restaurants
- **Shopping**: Amazon, Flipkart, Myntra
- **Bills**: Electricity, internet, utilities
- **Travel**: Uber, Ola, flights, hotels
- **Others**: Everything else

### 4. Inline Editing + Re-download
- Click any cell to edit vendor, invoice number, date, amount, or currency
- Edited data is used when downloading CSV/Excel
- Perfect for correcting extraction errors

### 5. Interactive Chart Visualization
- Real-time Chart.js bar chart
- Monthly spending trends
- Smooth animations
- Responsive design
- Capsule-style bars with gradient colors

---

## 🔧 Configuration

### Environment Variables

**Backend (.env file):**
```env
OPENAI_API_KEY=sk-your-api-key-here  # Optional, for AI mode
```

**Frontend (vite.config.js):**
```javascript
export default defineConfig({
  server: {
    port: 3000  // Change frontend port
  }
})
```

---

## 🐛 Troubleshooting

### Backend Issues

**"No module named 'fastapi'"**
```bash
cd backend
pip install -r requirements.txt
```

**"Address already in use"**
```bash
# Change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**"Cannot find module"**
```bash
cd frontend
npm install
```

**"Port 3000 is already in use"**
- Vite will automatically suggest another port (like 3001)

### CORS Errors

**"CORS policy blocked"**
- Ensure backend is running on port 8000
- Check frontend is accessing `http://localhost:8000` (not https)

### PDF Processing Errors

**"Failed to extract text"**
- Some PDFs are image-based (scanned documents) and won't work
- Try with text-based PDF invoices

---

## 📱 Mobile & Responsive

The UI is fully responsive and optimized for:
- 📱 **Mobile phones** (portrait & landscape)
- 📱 **Tablets** (iPad, Android tablets)
- 💻 **Desktop** (any screen size)
- 🖥️ **Large screens** (4K, ultra-wide)

### Responsive Breakpoints
- **Mobile**: < 768px (single column)
- **Tablet**: 768px - 1200px (2-column grids)
- **Desktop**: > 1200px (split-screen layout)
- **Large**: > 1400px (extra padding)

---

## 🎓 Where Kiro AI Helped

This project was built with assistance from **Kiro AI**. Key contributions:

### Regex Pattern Engineering
- Designed robust patterns for vendor names, invoice numbers, dates, amounts
- Multi-format date parsing
- Currency detection acrncies

### 2. Architecture Design
- Suggested FastAPI for backend (async, modern, fast)
- Recommended React + Vite for frontend
- Designed session-based file management
- Structured service layer

### 3. Smart Logic Implementation
- Invoice vs non-invoice detection algorithm
- Category detection patterns and rules
- Data completeness validation logic
- Statistics calculation

### 4. UI/UX Enhancements
- Glassmorphism and neumorphic design
- Split-screen dashboard layout
- Interactive chart integration
- Filter andt functionality

### 5. AI Integration
- Rule-based summarization fallback
- OpenAI GPT integration
- Prompt engineering for insights

See [KIRO_CONTRIBUTION.md](KIRO_CONTRIBUTION.md) for detailed breakdown.

---

## 🚀 Deployment

### Backend (Python)

**Option 1: Heroku**
```bash
heroku create invoice-extractor-api
git push heroku main
```

**Option 2: Railway**
```bash
railway init
railway up
```

**Option 3: Docker**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "app.py"]
```

### Frontend (React)

**Option 1: Vercel**
```bash
cd frontend
vercel
```

**Option 2: Netlify**
```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

**Option 3: GitHub Pages**
```bash
cd frontend
npm run build
# Deploy dist/ folder
```

---

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

- 📧 Email: Lakshaysingh86.5@gmail.com

---

## 🌟 Acknowledgments

- **Kiro AI** - For assistance with regex patterns, architecture, and UI design
- **FastAPI** - For the amazing async web framework
- **React** - For the powerful UI library
- **Chart.js** - For beautiful interactive charts
- **OpenAI** - For GPT-powered insights

---

## 📈 Roadmap

- [ ] OCR support for scanned invoices
- [ ] Bulk processing (100+ invoices)
- [ ] Email integration (auto-fetch from Gmail)
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Custom regex patterns (user-defined)
- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Team collaboration features
- [ ] API webhooks

---

**Built with ❤️ using Kiro AI**

*Transform your invoice chaos into organized insights!*

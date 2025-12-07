# Quick Start Guide

Get the Invoice Extractor running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Terminal/Command Prompt access

## Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Step 3: Start the Backend Server

Open a terminal and run:

```bash
cd backend
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open!

## Step 4: Start the Frontend

Open a NEW terminal and run:

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

## Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:3000
```

## Usage

1. Click the upload area to select PDF invoice files
2. Click "Extract Data" to process
3. View extracted data in the table
4. Edit any incorrect data directly in the table
5. Download CSV, Excel, or chart files

## Troubleshooting

### Backend won't start

**Error: "No module named 'fastapi'"**
- Solution: Make sure you installed dependencies: `pip install -r requirements.txt`

**Error: "Address already in use"**
- Solution: Port 8000 is busy. Kill the process or change the port in `app.py`

### Frontend won't start

**Error: "Cannot find module"**
- Solution: Run `npm install` in the frontend directory

**Error: "Port 3000 is already in use"**
- Solution: The port is busy. Vite will automatically suggest another port (like 3001)

### CORS Errors

**Error: "CORS policy blocked"**
- Solution: Make sure backend is running on port 8000
- Check that frontend is accessing `http://localhost:8000` (not https)

### PDF Processing Errors

**Error: "Failed to extract text"**
- Some PDFs are image-based (scanned documents) and won't work
- Try with text-based PDF invoices

## Testing with Sample Data

Don't have invoice PDFs? Create a simple test:

1. Open any word processor
2. Type:
   ```
   INVOICE

   From: Test Company
   Invoice Number: INV-001
   Date: 12/07/2024
   
   Total: $100.00
   ```
3. Save as PDF
4. Upload to the app

## Mobile/Tablet Access

The UI is fully responsive! Access from:
- 📱 Mobile phones (portrait/landscape)
- 📱 Tablets (iPad, Android tablets)
- 💻 Desktop (any screen size)

To access from another device on your network:
1. Find your computer's IP address
2. On mobile/tablet, go to: `http://YOUR_IP:3000`

## Next Steps

- Read the full [README.md](README.md) for features
- Check [KIRO_CONTRIBUTION.md](KIRO_CONTRIBUTION.md) to see how Kiro helped
- Customize regex patterns in `backend/services/pdf_processor.py`
- Adjust categories in the same file

## Need Help?

- Check the console for error messages
- Ensure both backend and frontend are running
- Verify you're using the correct URLs
- Make sure PDF files are text-based (not scanned images)

Happy extracting! 🚀

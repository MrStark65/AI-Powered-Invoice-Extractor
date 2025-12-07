"""FastAPI backend for Invoice Extractor."""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Dict
import os
import shutil
from pathlib import Path
import uuid

from services.pdf_processor import PDFProcessor
from services.output_generator import OutputGenerator
from services.ai_summarizer import AISummarizer

app = FastAPI(title="Invoice Extractor API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

pdf_processor = PDFProcessor()
output_generator = OutputGenerator()
ai_summarizer = AISummarizer()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Invoice Extractor API"}


@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload PDF files for processing."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    session_id = str(uuid.uuid4())
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            continue
        
        file_path = session_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append(file.filename)
    
    return {
        "session_id": session_id,
        "uploaded_files": uploaded_files,
        "count": len(uploaded_files)
    }


@app.post("/api/process/{session_id}")
async def process_invoices(session_id: str):
    """Process uploaded invoices and extract data."""
    session_dir = UPLOAD_DIR / session_id
    
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    
    pdf_files = list(session_dir.glob("*.pdf"))
    
    if not pdf_files:
        raise HTTPException(status_code=400, detail="No PDF files found")
    
    # Process each PDF
    results = []
    for pdf_file in pdf_files:
        try:
            data = pdf_processor.extract_invoice_data(str(pdf_file))
            data['filename'] = pdf_file.name
            results.append(data)
        except Exception as e:
            results.append({
                'filename': pdf_file.name,
                'error': str(e),
                'vendor_name': 'ERROR',
                'invoice_number': 'ERROR',
                'date': 'N/A',
                'total_amount': 0.0,
                'currency': 'N/A',
                'category': 'Others',
                'invoice_type': 'Not an invoice',
                'status': 'Error',
                'is_incomplete': True
            })
    
    # Calculate statistics
    valid_invoices = [r for r in results if r.get('invoice_type') == 'Invoice']
    complete_invoices = [r for r in valid_invoices if not r.get('is_incomplete', False)]
    incomplete_invoices = [r for r in valid_invoices if r.get('is_incomplete', False)]
    non_invoices = [r for r in results if r.get('invoice_type') == 'Not an invoice']
    
    total_spend = sum(r.get('total_amount', 0) for r in valid_invoices)
    
    # Find top vendor and biggest invoice
    vendor_totals = {}
    for inv in valid_invoices:
        vendor = inv.get('vendor_name', 'N/A')
        if vendor != 'N/A':
            vendor_totals[vendor] = vendor_totals.get(vendor, 0) + inv.get('total_amount', 0)
    
    top_vendor = max(vendor_totals.items(), key=lambda x: x[1])[0] if vendor_totals else 'N/A'
    biggest_invoice = max(valid_invoices, key=lambda x: x.get('total_amount', 0)) if valid_invoices else None
    
    # Calculate currency breakdown
    currency_breakdown = {}
    for inv in valid_invoices:
        currency = inv.get('currency', 'N/A')
        if currency != 'N/A':
            if currency not in currency_breakdown:
                currency_breakdown[currency] = {
                    'total': 0,
                    'count': 0,
                    'symbol': inv.get('currency_symbol', currency),
                    'region': inv.get('currency_region', 'Unknown')
                }
            currency_breakdown[currency]['total'] += inv.get('total_amount', 0)
            currency_breakdown[currency]['count'] += 1
    
    # Generate outputs
    output_session_dir = OUTPUT_DIR / session_id
    output_session_dir.mkdir(exist_ok=True)
    
    csv_path = output_generator.generate_csv(results, output_session_dir)
    excel_path = output_generator.generate_excel(results, output_session_dir)
    chart_path = output_generator.generate_chart(valid_invoices, output_session_dir)
    
    # Generate AI summary
    stats_for_ai = {
        "total_files": len(results),
        "valid_invoices": len(valid_invoices),
        "complete_invoices": len(complete_invoices),
        "incomplete_invoices": len(incomplete_invoices),
        "non_invoices": len(non_invoices),
        "total_spend": round(total_spend, 2),
        "top_vendor": top_vendor,
    }
    ai_summary = ai_summarizer.generate_summary(results, stats_for_ai)
    
    return {
        "session_id": session_id,
        "invoices": results,
        "ai_summary": ai_summary,
        "statistics": {
            "total_files": len(results),
            "valid_invoices": len(valid_invoices),
            "complete_invoices": len(complete_invoices),
            "incomplete_invoices": len(incomplete_invoices),
            "non_invoices": len(non_invoices),
            "total_spend": round(total_spend, 2),
            "top_vendor": top_vendor,
            "biggest_invoice": {
                "vendor": biggest_invoice.get('vendor_name') if biggest_invoice else 'N/A',
                "amount": biggest_invoice.get('total_amount') if biggest_invoice else 0
            },
            "currency_breakdown": currency_breakdown
        },
        "outputs": {
            "csv": f"/api/download/{session_id}/csv",
            "excel": f"/api/download/{session_id}/excel",
            "chart": f"/api/download/{session_id}/chart"
        }
    }


@app.post("/api/update-data/{session_id}")
async def update_data(session_id: str, updated_data: List[Dict]):
    """Update invoice data with edited values before download."""
    output_dir = OUTPUT_DIR / session_id
    
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Regenerate outputs with updated data
    csv_path = output_generator.generate_csv(updated_data, output_dir)
    excel_path = output_generator.generate_excel(updated_data, output_dir)
    
    valid_invoices = [r for r in updated_data if r.get('invoice_type') == 'Invoice']
    chart_path = output_generator.generate_chart(valid_invoices, output_dir)
    
    return {"message": "Data updated successfully"}


@app.get("/api/download/{session_id}/{file_type}")
async def download_file(session_id: str, file_type: str):
    """Download generated files."""
    output_dir = OUTPUT_DIR / session_id
    
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")
    
    file_map = {
        "csv": "invoices.csv",
        "excel": "invoices_dashboard.xlsx",
        "chart": "monthly_spending.png"
    }
    
    if file_type not in file_map:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_path = output_dir / file_map[file_type]
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_map[file_type],
        media_type="application/octet-stream"
    )


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Clean up session files."""
    upload_dir = UPLOAD_DIR / session_id
    output_dir = OUTPUT_DIR / session_id
    
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    return {"message": "Session deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

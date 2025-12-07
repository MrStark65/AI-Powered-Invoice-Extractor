# Design Document

## Overview

The Lazy Invoice & Bills Extractor is a Python-based automation tool that processes invoice PDFs to extract structured financial data and generate analytical outputs. The system follows a pipeline architecture: scan → extract → transform → output. It uses PyPDF2 or pdfplumber for PDF text extraction, regex patterns for field identification, pandas for data manipulation, and matplotlib/openpyxl for visualization and Excel generation.

The tool is designed to be run as a command-line application, processing all PDFs in a specified directory and producing three output artifacts: a CSV file for data portability, an Excel dashboard for spreadsheet analysis, and a monthly spending chart for visual insights.

## Architecture

The system follows a modular pipeline architecture with clear separation of concerns:

```
┌─────────────┐
│     CLI     │ (Entry point, argument parsing, user feedback)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PDF Scanner │ (Directory traversal, PDF identification)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Data Parser │ (Text extraction, regex matching, field extraction)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Transform  │ (Data normalization, date parsing, currency handling)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Output    │ (CSV, Excel, Chart generation)
│  Generator  │
└─────────────┘
```

### Key Design Decisions

1. **PDF Library Selection**: Use `pdfplumber` as the primary PDF extraction library due to its superior text extraction capabilities and layout preservation. Fall back to `PyPDF2` if pdfplumber fails.

2. **Regex-Based Extraction**: Employ multiple regex patterns per field with priority ordering. This allows handling various invoice formats without requiring machine learning or complex NLP.

3. **Error Resilience**: Each invoice is processed independently. Failures in one invoice do not stop processing of others. Missing fields are recorded as "N/A" or empty values.

4. **Data Pipeline**: Use pandas DataFrame as the central data structure for easy manipulation, filtering, and output generation.

5. **CLI Framework**: Use `argparse` for command-line argument parsing with sensible defaults and help documentation.

## Components and Interfaces

### 1. CLI Module (`cli.py`)

**Responsibilities:**
- Parse command-line arguments
- Validate input directory
- Orchestrate the extraction pipeline
- Display progress and results to user

**Interface:**
```python
def main():
    """Entry point for CLI application"""
    
def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments"""
    
def run_extraction(directory: str, output_dir: str) -> ExtractionResult:
    """Execute the full extraction pipeline"""
```

### 2. PDF Scanner Module (`scanner.py`)

**Responsibilities:**
- Traverse directory for PDF files
- Filter invoice-like PDFs (basic heuristics)
- Return list of PDF file paths

**Interface:**
```python
def scan_directory(directory: str) -> List[str]:
    """Scan directory and return list of PDF file paths"""
    
def is_invoice_pdf(pdf_path: str) -> bool:
    """Determine if PDF is likely an invoice based on content heuristics"""
```

### 3. Data Parser Module (`parser.py`)

**Responsibilities:**
- Extract text from PDF files
- Apply regex patterns to identify invoice fields
- Handle extraction failures gracefully

**Interface:**
```python
class InvoiceParser:
    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from PDF"""
        
    def parse_invoice(self, pdf_path: str) -> InvoiceData:
        """Extract all invoice fields from PDF"""
        
    def extract_vendor(self, text: str) -> str:
        """Extract vendor name using regex patterns"""
        
    def extract_invoice_number(self, text: str) -> str:
        """Extract invoice number using regex patterns"""
        
    def extract_date(self, text: str) -> str:
        """Extract invoice date using regex patterns"""
        
    def extract_amount(self, text: str) -> float:
        """Extract total amount using regex patterns"""
        
    def extract_currency(self, text: str) -> str:
        """Extract currency code or symbol using regex patterns"""
```

### 4. Transform Module (`transform.py`)

**Responsibilities:**
- Normalize extracted data
- Parse and standardize dates
- Clean and format currency values
- Handle missing or malformed data

**Interface:**
```python
def normalize_date(date_str: str) -> str:
    """Parse various date formats and return ISO format (YYYY-MM-DD)"""
    
def normalize_currency(currency_str: str) -> str:
    """Standardize currency codes (e.g., $ → USD, € → EUR)"""
    
def clean_amount(amount_str: str) -> float:
    """Remove formatting characters and parse numeric amount"""
```

### 5. Output Generator Module (`output.py`)

**Responsibilities:**
- Generate CSV file from extracted data
- Create Excel dashboard with formatting
- Generate monthly spending chart
- Handle file I/O and error cases

**Interface:**
```python
def generate_csv(data: pd.DataFrame, output_path: str) -> None:
    """Write extracted data to CSV file"""
    
def generate_excel(data: pd.DataFrame, output_path: str) -> None:
    """Create Excel file with formatted data"""
    
def generate_chart(data: pd.DataFrame, output_path: str) -> None:
    """Create and save monthly spending visualization"""
```

## Data Models

### InvoiceData

Represents extracted data from a single invoice:

```python
@dataclass
class InvoiceData:
    filename: str           # Original PDF filename
    vendor: str            # Vendor/company name
    invoice_number: str    # Invoice or bill number
    date: str             # Invoice date (ISO format YYYY-MM-DD)
    amount: float         # Total amount (numeric)
    currency: str         # Currency code (USD, EUR, etc.)
    extraction_status: str # "success", "partial", or "failed"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for DataFrame creation"""
```

### ExtractionResult

Represents the overall result of processing a directory:

```python
@dataclass
class ExtractionResult:
    total_files: int
    successful: int
    failed: int
    invoices: List[InvoiceData]
    output_files: List[str]  # Paths to generated output files
```

### Regex Pattern Configuration

Patterns are organized by field type with priority ordering:

```python
PATTERNS = {
    'vendor': [
        r'(?:From|Vendor|Company):\s*(.+?)(?:\n|$)',
        r'^([A-Z][A-Za-z\s&]+(?:Inc|LLC|Ltd|Corp))',
        # Additional patterns...
    ],
    'invoice_number': [
        r'Invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
        r'Bill\s*#?\s*:?\s*([A-Z0-9-]+)',
        # Additional patterns...
    ],
    'date': [
        r'Date:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'Invoice Date:\s*(\d{1,2}\s+\w+\s+\d{4})',
        # Additional patterns...
    ],
    'amount': [
        r'Total:?\s*\$?\s*([\d,]+\.?\d*)',
        r'Amount Due:?\s*\$?\s*([\d,]+\.?\d*)',
        # Additional patterns...
    ],
    'currency': [
        r'(\$|USD|€|EUR|£|GBP)',
        # Additional patterns...
    ]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: PDF Discovery Completeness
*For any* directory containing PDF files, scanning that directory should return all PDF files present in the root level
**Validates: Requirements 1.1**

### Property 2: Non-Invoice Resilience
*For any* non-invoice PDF file, processing it should not raise exceptions or crash the system
**Validates: Requirements 1.3**

### Property 3: Field Extraction Consistency
*For any* invoice PDF with extractable fields, parsing should return an InvoiceData object with all five fields populated (vendor, invoice_number, date, amount, currency)
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 4: Missing Field Handling
*For any* invoice where a field cannot be extracted, that field should contain a placeholder value (e.g., "N/A" or empty string) rather than causing an error
**Validates: Requirements 3.1**

### Property 5: Pipeline Resilience
*For any* batch of PDFs containing at least one corrupted file, the system should successfully process all valid PDFs and continue execution
**Validates: Requirements 3.2**

### Property 6: Date Normalization
*For any* valid date string in common formats (MM/DD/YYYY, DD-MM-YYYY, Month DD, YYYY), normalization should produce a valid ISO format date (YYYY-MM-DD)
**Validates: Requirements 3.3**

### Property 7: Currency Standardization
*For any* currency symbol or code ($, USD, €, EUR, £, GBP), standardization should produce a consistent three-letter currency code
**Validates: Requirements 3.4**

### Property 8: Amount Parsing
*For any* amount string with formatting characters (commas, spaces, currency symbols), parsing should extract the correct numeric value
**Validates: Requirements 3.5**

### Property 9: CSV Row Count Invariant
*For any* list of N successfully extracted invoices, the generated CSV file should contain exactly N+1 rows (N data rows plus 1 header row)
**Validates: Requirements 4.3**

### Property 10: CSV Header Completeness
*For any* generated CSV file, it should contain headers for all required fields: filename, vendor, invoice_number, date, amount, currency
**Validates: Requirements 4.2**

### Property 11: Excel Column Completeness
*For any* generated Excel file, it should contain columns for all required fields: filename, vendor, invoice_number, date, amount, currency
**Validates: Requirements 5.3**

### Property 12: Monthly Grouping Correctness
*For any* set of invoices with dates in the same month, the chart generation should group them together and sum their amounts correctly
**Validates: Requirements 6.2, 6.3**

### Property 13: Month Coverage Completeness
*For any* set of invoices spanning M unique months, the generated chart should display exactly M data points
**Validates: Requirements 6.5**

### Property 14: CLI Summary Accuracy
*For any* extraction run processing N invoices, the CLI summary should report exactly N as the count of processed invoices
**Validates: Requirements 7.3**

### Property 15: Regex Pattern Fallback
*For any* field with multiple regex patterns, if the first pattern fails to match, subsequent patterns should be attempted in order
**Validates: Requirements 8.2**

### Property 16: Whitespace Normalization
*For any* PDF text containing multiple consecutive whitespace characters, normalization should reduce them to single spaces before pattern matching
**Validates: Requirements 8.4**

## Error Handling

### Error Categories

1. **File System Errors**
   - Directory not found → Display clear error message and exit
   - Permission denied → Display error message and skip file
   - File not found → Log warning and continue processing

2. **PDF Processing Errors**
   - Corrupted PDF → Log error, record as failed, continue with next file
   - Encrypted PDF → Log error, record as failed, continue with next file
   - Text extraction failure → Try fallback library, if still fails, record as failed

3. **Data Extraction Errors**
   - Field not found → Record placeholder value ("N/A" or empty)
   - Invalid date format → Record raw string or "Invalid Date"
   - Invalid amount format → Record 0.0 or NaN
   - Multiple matches → Use first match or most confident match

4. **Output Generation Errors**
   - Cannot write file → Display error and exit (critical failure)
   - Invalid data for chart → Skip chart generation, log warning
   - Excel formatting failure → Generate basic Excel without formatting

### Error Logging

All errors should be logged with:
- Timestamp
- Error type/category
- File being processed (if applicable)
- Error message
- Stack trace (for debugging mode)

### Recovery Strategies

- **Graceful Degradation**: If Excel generation fails, still produce CSV and chart
- **Partial Success**: If some invoices fail, still output results for successful ones
- **User Feedback**: Always inform user of what succeeded and what failed

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality of individual components:

1. **Scanner Module Tests**
   - Test directory scanning with known file structures
   - Test PDF identification logic
   - Test handling of empty directories

2. **Parser Module Tests**
   - Test each regex pattern against sample text
   - Test text extraction from sample PDFs
   - Test handling of missing fields

3. **Transform Module Tests**
   - Test date parsing with various formats
   - Test currency normalization
   - Test amount cleaning with edge cases (negative, zero, very large)

4. **Output Module Tests**
   - Test CSV generation with sample data
   - Test Excel generation with sample data
   - Test chart generation with sample data

### Property-Based Testing

Property-based tests will verify universal properties using the Hypothesis library for Python. Each test will run a minimum of 100 iterations with randomly generated inputs.

**Testing Framework**: Hypothesis (Python property-based testing library)

**Test Configuration**:
- Minimum 100 iterations per property test
- Custom generators for invoice data, dates, amounts, currencies
- Shrinking enabled to find minimal failing examples

**Property Test Tags**:
Each property-based test will include a comment tag in this format:
```python
# Feature: invoice-bills-extractor, Property N: [property description]
```

**Key Property Tests**:

1. **PDF Discovery** - Generate random directory structures, verify all PDFs found
2. **Date Normalization** - Generate dates in various formats, verify ISO output
3. **Amount Parsing** - Generate formatted amounts, verify numeric extraction
4. **CSV Row Count** - Generate random invoice lists, verify row count invariant
5. **Monthly Grouping** - Generate invoices with random dates, verify grouping logic

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Full Pipeline Test** - Process sample invoice directory, verify all outputs generated
2. **Error Recovery Test** - Process directory with corrupted PDFs, verify graceful handling
3. **Empty Input Test** - Process empty directory, verify appropriate output

### Test Data

- **Sample Invoices**: Collection of real-world invoice PDFs (anonymized) covering various formats
- **Edge Cases**: Empty PDFs, non-invoice PDFs, corrupted PDFs, encrypted PDFs
- **Synthetic Data**: Generated invoices with known field values for validation

## Dependencies

### Core Libraries

- **pdfplumber** (>=0.9.0): Primary PDF text extraction
- **PyPDF2** (>=3.0.0): Fallback PDF extraction
- **pandas** (>=2.0.0): Data manipulation and CSV generation
- **openpyxl** (>=3.1.0): Excel file generation
- **matplotlib** (>=3.7.0): Chart generation
- **python-dateutil** (>=2.8.0): Date parsing

### Development Libraries

- **pytest** (>=7.0.0): Unit testing framework
- **hypothesis** (>=6.0.0): Property-based testing
- **black**: Code formatting
- **mypy**: Type checking
- **flake8**: Linting

### Python Version

- Minimum: Python 3.9
- Recommended: Python 3.11+

## Performance Considerations

1. **PDF Processing**: Process PDFs sequentially to avoid memory issues with large files
2. **Batch Size**: No hard limit, but recommend processing <1000 PDFs per run
3. **Memory**: Each PDF held in memory during processing, then released
4. **Caching**: No caching implemented in initial version
5. **Parallelization**: Future enhancement - parallel PDF processing with multiprocessing

## Security Considerations

1. **File System Access**: Only read access to specified directory, write access to output directory
2. **PDF Content**: No execution of embedded scripts or macros
3. **Input Validation**: Validate directory paths to prevent path traversal attacks
4. **Data Privacy**: All processing done locally, no external API calls or data transmission

## Future Enhancements

1. **Machine Learning**: Train ML model for better field extraction on diverse invoice formats
2. **OCR Support**: Add OCR capability for scanned/image-based invoices
3. **Multi-currency**: Convert all amounts to single currency for accurate totals
4. **Database Storage**: Option to store extracted data in SQLite or PostgreSQL
5. **Web Interface**: Simple web UI for non-technical users
6. **Duplicate Detection**: Identify and flag duplicate invoices
7. **Category Classification**: Auto-categorize expenses (utilities, supplies, services, etc.)
8. **Email Integration**: Automatically process invoices from email attachments

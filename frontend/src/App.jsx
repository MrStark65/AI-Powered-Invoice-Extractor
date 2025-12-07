import { useState, useMemo } from 'react'
import axios from 'axios'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js'
import './App.css'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const API_URL = 'http://localhost:8000'

function App() {
  const [files, setFiles] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [editedData, setEditedData] = useState({})
  const [filterCategory, setFilterCategory] = useState('All')
  const [filterType, setFilterType] = useState('All')
  const [filterCurrency, setFilterCurrency] = useState('All')
  const [sortColumn, setSortColumn] = useState(null)
  const [sortDirection, setSortDirection] = useState('asc')

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles(selectedFiles)
    setError(null)
  }

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Please select PDF files to upload')
      return
    }

    setProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      files.forEach((file) => {
        formData.append('files', file)
      })

      const uploadResponse = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { session_id } = uploadResponse.data
      setSessionId(session_id)

      const processResponse = await axios.post(
        `${API_URL}/api/process/${session_id}`
      )
      setResults(processResponse.data)
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.detail || 'An error occurred')
    } finally {
      setProcessing(false)
    }
  }

  const handleDownload = async (fileType) => {
    if (!results || !sessionId) return

    const mergedData = results.invoices.map((invoice, idx) => ({
      ...invoice,
      ...(editedData[idx] || {})
    }))

    try {
      await axios.post(`${API_URL}/api/update-data/${sessionId}`, mergedData)
      window.open(`${API_URL}/api/download/${sessionId}/${fileType}`, '_blank')
    } catch (err) {
      console.error('Download error:', err)
    }
  }

  const handleReset = () => {
    setFiles([])
    setSessionId(null)
    setResults(null)
    setError(null)
    setEditedData({})
    setFilterCategory('All')
    setFilterType('All')
    setFilterCurrency('All')
    setSortColumn(null)
    setSortDirection('asc')
  }

  const handleCellEdit = (index, field, value) => {
    setEditedData((prev) => ({
      ...prev,
      [index]: {
        ...(prev[index] || {}),
        [field]: value
      }
    }))
  }

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortColumn(column)
      setSortDirection('asc')
    }
  }

  const getDisplayData = (invoice, index) => {
    return {
      ...invoice,
      ...(editedData[index] || {})
    }
  }

  const filteredAndSortedInvoices = useMemo(() => {
    if (!results) return []

    let filtered = results.invoices.filter((inv) => {
      if (filterCategory !== 'All' && inv.category !== filterCategory) return false
      if (filterType !== 'All' && inv.invoice_type !== filterType) return false
      if (filterCurrency !== 'All' && inv.currency !== filterCurrency) return false
      return true
    })

    if (sortColumn) {
      filtered = [...filtered].sort((a, b) => {
        let aVal = a[sortColumn]
        let bVal = b[sortColumn]

        if (sortColumn === 'total_amount') {
          aVal = parseFloat(aVal) || 0
          bVal = parseFloat(bVal) || 0
        }

        if (aVal == null) return 1
        if (bVal == null) return -1

        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1
        return 0
      })
    }

    return filtered
  }, [
    results,
    filterCategory,
    filterType,
    filterCurrency,
    sortColumn,
    sortDirection
  ])

  const availableCurrencies = useMemo(() => {
    if (!results) return []
    const currencies = new Set(results.invoices.map((inv) => inv.currency))
    return Array.from(currencies)
      .filter((c) => c && c !== 'N/A')
      .sort()
  }, [results])

  // ---- Monthly chart data from invoices ----
  const monthlyChart = useMemo(() => {
    if (!results) return null

    const buckets = {}
    results.invoices.forEach((inv) => {
      if (inv.invoice_type !== 'Invoice') return
      if (!inv.date || inv.date === 'N/A') return

      const monthKey = inv.date.slice(0, 7) // "YYYY-MM"
      const amount = parseFloat(inv.total_amount) || 0

      buckets[monthKey] = (buckets[monthKey] || 0) + amount
    })

    const labels = Object.keys(buckets).sort()
    const data = labels.map((label) => buckets[label])

    if (!labels.length) return null

    return { labels, data }
  }, [results])

  const chartData = useMemo(() => {
    if (!monthlyChart) return null
    return {
      labels: monthlyChart.labels,
      datasets: [
        {
          label: 'Total Spend',
          data: monthlyChart.data,
          borderRadius: 14,
          backgroundColor: 'rgba(102, 126, 234, 0.9)',
          hoverBackgroundColor: 'rgba(118, 75, 162, 0.95)',
          borderSkipped: false,
          maxBarThickness: 42
        }
      ]
    }
  }, [monthlyChart])

  const chartOptions = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          padding: 12,
          borderRadius: 10,
          titleFont: { weight: '700', size: 13 },
          bodyFont: { size: 12 },
          callbacks: {
            label: (ctx) =>
              ` ₹ ${ctx.parsed.y.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              })}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            color: '#4b5563',
            font: { size: 11 }
          }
        },
        y: {
          grid: {
            color: 'rgba(148, 163, 184, 0.25)',
            drawBorder: false
          },
          ticks: {
            color: '#6b7280',
            font: { size: 11 },
            callback: (value) => `₹${value}`
          }
        }
      }
    }),
    []
  )

  const getCategoryColor = (category) => {
    const colors = {
      Food: '#ff6b6b',
      Shopping: '#4ecdc4',
      Bills: '#45b7d1',
      Travel: '#f9ca24',
      Others: '#95a5a6'
    }
    return colors[category] || colors['Others']
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📄 Invoice Extractor</h1>
        <p>Upload invoice PDFs to extract and analyze financial data</p>
        <p className="subtitle">
          Smart parsing · AI insights · Clean exports in CSV / Excel
        </p>
      </header>

      <main className="main">
        {!results ? (
          <div className="upload-section">
            <div className="upload-box">
              <input
                type="file"
                id="file-input"
                multiple
                accept=".pdf"
                onChange={handleFileChange}
                className="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                <div className="upload-icon">📁</div>
                <div className="upload-text">
                  {files.length > 0
                    ? `${files.length} file(s) selected`
                    : 'Click to select PDF files'}
                </div>
                <span className="upload-sub">Drop invoices here or browse</span>
              </label>
            </div>

            {files.length > 0 && (
              <div className="file-list">
                <h3>Selected Files</h3>
                <ul>
                  {files.map((file, idx) => (
                    <li key={idx}>{file.name}</li>
                  ))}
                </ul>
              </div>
            )}

            {error && <div className="error">{error}</div>}

            <button
              onClick={handleUpload}
              disabled={processing || files.length === 0}
              className="btn btn-primary"
            >
              {processing ? 'Processing…' : 'Extract Data'}
            </button>
          </div>
        ) : (
          <div className="results-section">
            {/* Processing / success pill */}
            <div className="processing-banner">
              <span className="icon">✅</span>
              <span className="label">
                Processing complete — your invoices have been analyzed and
                insights are ready.
              </span>
            </div>

            {/* MAIN DASHBOARD LAYOUT */}
            <div className="dashboard-layout">
              {/* LEFT: SUMMARY / AI / CURRENCY */}
              <aside className="insights-sidebar">
                <section className="summary">
                  <h2>Invoice Overview</h2>
                  <p className="summary-sub">
                    High-level snapshot of your extracted data.
                  </p>

                  <div className="summary-cards">
                    <div className="summary-card">
                      <div className="card-icon">💰</div>
                      <div className="card-content">
                        <div className="card-label">Total Spend</div>
                        <div className="card-value">
                          {results.statistics.total_spend.toFixed(2)}
                        </div>
                      </div>
                    </div>

                    <div className="summary-card">
                      <div className="card-icon">📄</div>
                      <div className="card-content">
                        <div className="card-label">Valid Invoices</div>
                        <div className="card-value">
                          {results.statistics.valid_invoices}
                        </div>
                      </div>
                    </div>

                    <div className="summary-card">
                      <div className="card-icon">🏪</div>
                      <div className="card-content">
                        <div className="card-label">Top Vendor</div>
                        <div className="card-value small">
                          {results.statistics.top_vendor}
                        </div>
                      </div>
                    </div>

                    <div className="summary-card">
                      <div className="card-icon">📊</div>
                      <div className="card-content">
                        <div className="card-label">Biggest Invoice</div>
                        <div className="card-value">
                          {results.statistics.biggest_invoice.amount.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="status-line">
                    {results.statistics.complete_invoices} invoices complete ·
                    {results.statistics.incomplete_invoices > 0 && (
                      <span className="incomplete-text">
                        {' '}
                        {results.statistics.incomplete_invoices} invoice(s)
                        missing date/amount
                      </span>
                    )}
                    {results.statistics.non_invoices > 0 && (
                      <span className="non-invoice-text">
                        {' '}
                        · {results.statistics.non_invoices} non-invoice file(s)
                      </span>
                    )}
                  </div>
                </section>

                {/* Currency breakdown */}
                {results.statistics.currency_breakdown &&
                  Object.keys(results.statistics.currency_breakdown).length >
                    0 && (
                    <section className="currency-breakdown">
                      <h4>💱 Currency Breakdown</h4>
                      <div className="currency-grid">
                        {Object.entries(
                          results.statistics.currency_breakdown
                        ).map(([currency, data]) => (
                          <div key={currency} className="currency-item">
                            <div className="currency-header">
                              <span className="currency-flag">
                                {data.symbol}
                              </span>
                              <span className="currency-name">{currency}</span>
                            </div>
                            <div className="currency-details">
                              <div className="currency-stat">
                                <span className="stat-label">Total</span>
                                <span className="stat-value">
                                  {data.symbol}{' '}
                                  {data.total.toFixed(2).toLocaleString()}
                                </span>
                              </div>
                              <div className="currency-stat">
                                <span className="stat-label">Invoices</span>
                                <span className="stat-value">
                                  {data.count}
                                </span>
                              </div>
                              <div className="currency-stat">
                                <span className="stat-label">Region</span>
                                <span className="stat-value">
                                  {data.region}
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </section>
                  )}

                {/* AI insights */}
                {results.ai_summary && (
                  <section className="ai-summary-section">
                    <div className="ai-header">
                      <h3>🤖 AI-Powered Insights</h3>
                      {results.ai_summary.ai_powered && (
                        <span className="ai-badge">Powered by GPT</span>
                      )}
                    </div>

                    <div className="ai-cards">
                      <div className="ai-card overview-card">
                        <div className="ai-card-icon">📊</div>
                        <div className="ai-card-content">
                          <h4>Overview</h4>
                          <p>{results.ai_summary.overview}</p>
                        </div>
                      </div>

                      <div className="ai-card insights-card">
                        <div className="ai-card-icon">💡</div>
                        <div className="ai-card-content">
                          <h4>Spending Insights</h4>
                          <p>{results.ai_summary.spending_insights}</p>
                        </div>
                      </div>

                      <div className="ai-card recommendations-card">
                        <div className="ai-card-icon">🎯</div>
                        <div className="ai-card-content">
                          <h4>Recommendations</h4>
                          <p>{results.ai_summary.recommendations}</p>
                        </div>
                      </div>
                    </div>

                    <details className="full-summary">
                      <summary>View full AI analysis</summary>
                      <pre className="summary-text">
                        {results.ai_summary.full_summary}
                      </pre>
                    </details>
                  </section>
                )}
              </aside>

              {/* RIGHT: CHART + DOWNLOADS + TABLE */}
              <section className="data-content">
                {chartData && (
                  <section className="chart-section">
                    <div className="chart-header">
                      <div>
                        <h3>📈 Monthly Spending Trends</h3>
                        <p className="chart-subtitle">
                          Smooth, capsule-style bars showing total spend per
                          month.
                        </p>
                      </div>
                      <div className="chart-legend">
                        <span className="legend-dot" />
                        <span>Total spend</span>
                      </div>
                    </div>
                    <div className="chart-container">
                      <Bar data={chartData} options={chartOptions} />
                    </div>
                  </section>
                )}

                <section className="downloads">
                  <h3>Download Results</h3>
                  <div className="download-buttons">
                    <button
                      onClick={() => handleDownload('csv')}
                      className="btn btn-download"
                    >
                      📊 CSV
                    </button>
                    <button
                      onClick={() => handleDownload('excel')}
                      className="btn btn-download"
                    >
                      📈 Excel
                    </button>
                    <button
                      onClick={() => handleDownload('chart')}
                      className="btn btn-download"
                    >
                      🖼 Chart Image
                    </button>
                  </div>
                </section>

                <section className="invoice-table">
                  <div className="table-header">
                    <h3>Extracted Data</h3>
                    <div className="filters">
                      <select
                        value={filterType}
                        onChange={(e) => setFilterType(e.target.value)}
                        className="filter-select"
                      >
                        <option value="All">All Types</option>
                        <option value="Invoice">Invoices only</option>
                        <option value="Not an invoice">Non-invoices</option>
                      </select>

                      <select
                        value={filterCategory}
                        onChange={(e) => setFilterCategory(e.target.value)}
                        className="filter-select"
                      >
                        <option value="All">All Categories</option>
                        <option value="Food">Food</option>
                        <option value="Shopping">Shopping</option>
                        <option value="Bills">Bills</option>
                        <option value="Travel">Travel</option>
                        <option value="Others">Others</option>
                      </select>

                      <select
                        value={filterCurrency}
                        onChange={(e) => setFilterCurrency(e.target.value)}
                        className="filter-select"
                      >
                        <option value="All">All Currencies</option>
                        {availableCurrencies.map((curr) => (
                          <option key={curr} value={curr}>
                            {curr}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th onClick={() => handleSort('invoice_type')}>
                            Type{' '}
                            {sortColumn === 'invoice_type' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th onClick={() => handleSort('filename')}>
                            Filename{' '}
                            {sortColumn === 'filename' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th onClick={() => handleSort('vendor_name')}>
                            Vendor{' '}
                            {sortColumn === 'vendor_name' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th onClick={() => handleSort('invoice_number')}>
                            Invoice #
                          </th>
                          <th onClick={() => handleSort('date')}>
                            Date{' '}
                            {sortColumn === 'date' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th onClick={() => handleSort('total_amount')}>
                            Amount{' '}
                            {sortColumn === 'total_amount' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th onClick={() => handleSort('currency')}>
                            Currency{' '}
                            {sortColumn === 'currency' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th>Region</th>
                          <th onClick={() => handleSort('category')}>
                            Category{' '}
                            {sortColumn === 'category' &&
                              (sortDirection === 'asc' ? '↑' : '↓')}
                          </th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredAndSortedInvoices.map((invoice, idx) => {
                          const displayData = getDisplayData(invoice, idx)
                          const isIncomplete = invoice.is_incomplete
                          const isNonInvoice =
                            invoice.invoice_type === 'Not an invoice'

                          return (
                            <tr
                              key={idx}
                              className={`${
                                invoice.error ? 'error-row' : ''
                              } ${isIncomplete ? 'incomplete-row' : ''} ${
                                isNonInvoice ? 'non-invoice-row' : ''
                              }`}
                            >
                              <td>
                                <span
                                  className={`type-badge ${
                                    invoice.invoice_type === 'Invoice'
                                      ? 'badge-invoice'
                                      : 'badge-non-invoice'
                                  }`}
                                >
                                  {invoice.invoice_type}
                                </span>
                              </td>
                              <td>{displayData.filename}</td>
                              <td>
                                <input
                                  type="text"
                                  value={displayData.vendor_name || ''}
                                  onChange={(e) =>
                                    handleCellEdit(
                                      idx,
                                      'vendor_name',
                                      e.target.value
                                    )
                                  }
                                  className="editable-cell"
                                />
                              </td>
                              <td>
                                <input
                                  type="text"
                                  value={displayData.invoice_number || ''}
                                  onChange={(e) =>
                                    handleCellEdit(
                                      idx,
                                      'invoice_number',
                                      e.target.value
                                    )
                                  }
                                  className="editable-cell"
                                />
                              </td>
                              <td
                                className={
                                  displayData.date === 'N/A'
                                    ? 'missing-data'
                                    : ''
                                }
                              >
                                <input
                                  type="text"
                                  value={displayData.date || ''}
                                  onChange={(e) =>
                                    handleCellEdit(idx, 'date', e.target.value)
                                  }
                                  className="editable-cell"
                                />
                                {displayData.date === 'N/A' && (
                                  <span className="incomplete-badge">
                                    Missing
                                  </span>
                                )}
                              </td>
                              <td
                                className={
                                  !displayData.total_amount
                                    ? 'missing-data'
                                    : ''
                                }
                              >
                                <input
                                  type="number"
                                  value={displayData.total_amount || 0}
                                  onChange={(e) =>
                                    handleCellEdit(
                                      idx,
                                      'total_amount',
                                      parseFloat(e.target.value) || 0
                                    )
                                  }
                                  className="editable-cell"
                                />
                                {!displayData.total_amount && (
                                  <span className="incomplete-badge">
                                    Missing
                                  </span>
                                )}
                              </td>
                              <td>
                                <div className="currency-cell">
                                  <span className="currency-code">
                                    {displayData.currency}
                                  </span>
                                  {displayData.currency_symbol &&
                                    displayData.currency !== 'N/A' && (
                                      <span className="currency-symbol">
                                        {displayData.currency_symbol}
                                      </span>
                                    )}
                                </div>
                              </td>
                              <td>
                                <span className="region-badge">
                                  {displayData.currency_region || 'Unknown'}
                                </span>
                              </td>
                              <td>
                                <span
                                  className="category-chip"
                                  style={{
                                    backgroundColor: getCategoryColor(
                                      displayData.category
                                    )
                                  }}
                                >
                                  {displayData.category}
                                </span>
                              </td>
                              <td>
                                {isIncomplete && (
                                  <span className="status-badge incomplete">
                                    Incomplete
                                  </span>
                                )}
                                {!isIncomplete &&
                                  invoice.invoice_type === 'Invoice' && (
                                    <span className="status-badge complete">
                                      Complete
                                    </span>
                                  )}
                              </td>
                            </tr>
                          )
                        })}
                      </tbody>
                    </table>
                  </div>
                </section>

                <section className="bottom-actions">
                  <button
                    onClick={handleReset}
                    className="btn btn-secondary btn-reset"
                  >
                    🔄 Process More Invoices
                  </button>
                </section>

                <footer className="app-footer">
                  <p>
                    🚀 Built with{' '}
                    <a
                      href="https://kiro.ai"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Kiro AI
                    </a>
                  </p>
                  <p className="footer-note">
                    Regex generation · parsing logic · API design assistance
                  </p>
                </footer>
              </section>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

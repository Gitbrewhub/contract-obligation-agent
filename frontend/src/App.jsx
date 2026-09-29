import {
  Bell,
  ChevronDown,
  FileText,
  LayoutDashboard,
  ListChecks,
  LogOut,
  Menu,
  Plus,
  Search,
  Settings,
  ShieldAlert,
  Upload,
  X,
  AlertTriangle,
  CheckCircle2,
  CalendarDays,
} from 'lucide-react'

import {
  useRef,
  useState,
} from 'react'

import {
  BrowserRouter,
  Link,
  Route,
  Routes,
  useLocation,
} from 'react-router-dom'

import './App.css'


/* =========================================================
   APP
========================================================= */

function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  )
}


/* =========================================================
   MAIN LAYOUT
========================================================= */

function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="app-shell">

      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={`sidebar ${
          sidebarOpen ? 'sidebar-open' : ''
        }`}
      >

        <div className="sidebar-header">

          <Link
            to="/"
            className="brand"
            onClick={() => setSidebarOpen(false)}
          >

            <div className="brand-mark">
              <ShieldAlert size={20} />
            </div>

            <div className="brand-text">
              <span className="brand-name">
                Contract
              </span>

              <span className="brand-ai">
                .AI
              </span>
            </div>

          </Link>

          <button
            className="mobile-close"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>

        </div>


        <div className="sidebar-section">

          <span className="section-label">
            WORKSPACE
          </span>

          <nav className="navigation">

            <NavItem
              to="/"
              icon={<LayoutDashboard size={19} />}
              label="Overview"
              closeSidebar={() => setSidebarOpen(false)}
            />

            <NavItem
              to="/contracts"
              icon={<FileText size={19} />}
              label="Contracts"
              closeSidebar={() => setSidebarOpen(false)}
            />

            <NavItem
              to="/obligations"
              icon={<ListChecks size={19} />}
              label="Obligations"
              closeSidebar={() => setSidebarOpen(false)}
            />

            <NavItem
              to="/risks"
              icon={<ShieldAlert size={19} />}
              label="Risk Analysis"
              closeSidebar={() => setSidebarOpen(false)}
            />

          </nav>

        </div>


        <div className="sidebar-section">

          <span className="section-label">
            MANAGE
          </span>

          <nav className="navigation">

            <NavItem
              to="/upload"
              icon={<Upload size={19} />}
              label="Upload Contract"
              closeSidebar={() => setSidebarOpen(false)}
            />

            <NavItem
              to="/settings"
              icon={<Settings size={19} />}
              label="Settings"
              closeSidebar={() => setSidebarOpen(false)}
            />

          </nav>

        </div>


        <div className="sidebar-bottom">

          <div className="upgrade-card">

            <div className="upgrade-icon">
              <ShieldAlert size={18} />
            </div>

            <div>
              <strong>
                AI Contract Review
              </strong>

              <p>
                Analyze contracts faster
              </p>
            </div>

            <ChevronDown size={15} />

          </div>


          <button className="logout-button">

            <LogOut size={18} />

            <span>
              Sign out
            </span>

          </button>

        </div>

      </aside>


      <main className="main-area">

        <header className="topbar">

          <div className="topbar-left">

            <button
              className="menu-button"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={21} />
            </button>

            <Breadcrumb />

          </div>


          <div className="topbar-right">

            <button className="icon-button">
              <Search size={19} />
            </button>

            <button className="icon-button notification-button">
              <Bell size={19} />
              <span className="notification-dot" />
            </button>

            <div className="user-profile">

              <div className="avatar">
                PS
              </div>

              <div className="user-info">

                <strong>
                  Project User
                </strong>

                <span>
                  Administrator
                </span>

              </div>

              <ChevronDown size={16} />

            </div>

          </div>

        </header>


        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/contracts"
            element={<ContractsPage />}
          />

          <Route
            path="/obligations"
            element={<ObligationsPage />}
          />

          <Route
            path="/risks"
            element={<RisksPage />}
          />

          <Route
            path="/upload"
            element={<UploadPage />}
          />

          <Route
            path="/settings"
            element={<SettingsPage />}
          />

        </Routes>

      </main>

    </div>
  )
}


/* =========================================================
   BREADCRUMB
========================================================= */

function Breadcrumb() {

  const location = useLocation()

  const names = {
    '/': 'Overview',
    '/contracts': 'Contracts',
    '/obligations': 'Obligations',
    '/risks': 'Risk Analysis',
    '/upload': 'Upload Contract',
    '/settings': 'Settings',
  }

  return (
    <div className="breadcrumb">

      <span>
        Workspace
      </span>

      <span className="breadcrumb-separator">
        /
      </span>

      <strong>
        {names[location.pathname] || 'Overview'}
      </strong>

    </div>
  )
}


/* =========================================================
   NAV ITEM
========================================================= */

function NavItem({
  to,
  icon,
  label,
  closeSidebar,
}) {

  const location = useLocation()

  const active =
    to === '/'
      ? location.pathname === '/'
      : location.pathname.startsWith(to)

  return (
    <Link
      to={to}
      className={`nav-item ${
        active ? 'active' : ''
      }`}
      onClick={closeSidebar}
    >

      {icon}

      <span>
        {label}
      </span>

    </Link>
  )
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard() {

  return (
    <div className="content">

      <section className="page-heading">

        <div>

          <p className="eyebrow">
            CONTRACT INTELLIGENCE
          </p>

          <h1>
            Good morning, welcome back.
          </h1>

          <p className="page-description">
            Keep track of your contracts,
            obligations, and potential risks.
          </p>

        </div>

        <Link
          to="/upload"
          className="primary-button"
        >
          <Plus size={18} />
          Upload Contract
        </Link>

      </section>


      <section className="stats-grid">

        <StatCard
          label="Total Contracts"
          value="24"
          change="+12%"
          icon={<FileText size={20} />}
        />

        <StatCard
          label="Active Obligations"
          value="38"
          change="+8%"
          icon={<ListChecks size={20} />}
        />

        <StatCard
          label="Due This Month"
          value="08"
          change="3 urgent"
          warning
          icon={<CalendarDays size={20} />}
        />

        <StatCard
          label="Risky Clauses"
          value="05"
          change="Needs review"
          warning
          icon={<ShieldAlert size={20} />}
        />

      </section>


      <section className="dashboard-grid">

        <div className="panel">

          <div className="panel-header">

            <div>
              <h2>
                Recent Contracts
              </h2>

              <p>
                Your latest uploaded agreements
              </p>
            </div>

            <Link
              to="/contracts"
              className="text-button"
            >
              View all
            </Link>

          </div>


          <ContractRow
            name="Software Development Agreement"
            type="Development"
            date="Sep 16, 2026"
            status="Analyzed"
            statusType="success"
          />

          <ContractRow
            name="Non-Disclosure Agreement"
            type="NDA"
            date="Sep 14, 2026"
            status="Analyzed"
            statusType="success"
          />

          <ContractRow
            name="Cloud Services Agreement"
            type="Services"
            date="Sep 12, 2026"
            status="Review required"
            statusType="warning"
          />

        </div>


        <div className="panel">

          <div className="panel-header">

            <div>
              <h2>
                Upcoming Obligations
              </h2>

              <p>
                Things that need attention
              </p>
            </div>

          </div>


          <Obligation
            title="Submit monthly report"
            contract="Software Development Agreement"
            date="Sep 20"
            urgent
          />

          <Obligation
            title="Service renewal review"
            contract="Cloud Services Agreement"
            date="Sep 24"
          />

          <Obligation
            title="Insurance certificate"
            contract="Vendor Partnership Agreement"
            date="Sep 28"
          />

        </div>

      </section>

    </div>
  )
}


/* =========================================================
   UPLOAD PAGE
========================================================= */

function UploadPage() {

  const fileInputRef = useRef(null)

  const [selectedFile, setSelectedFile] =
    useState(null)

  const [error, setError] =
    useState('')

  const [isDragging, setIsDragging] =
    useState(false)

  const [isAnalyzing, setIsAnalyzing] =
    useState(false)

  const [analysisResult, setAnalysisResult] =
    useState(null)

  const [analysisStep, setAnalysisStep] =
    useState(0)


  const steps = [
    'Reading document',
    'Extracting clauses',
    'Finding obligations',
    'Analyzing risk signals',
    'Preparing contract intelligence',
  ]


  /* =====================================================
     FILE VALIDATION
  ===================================================== */

  const validateFile = (file) => {

    if (!file) {
      return false
    }

    const extension =
      file.name
        .toLowerCase()
        .slice(
          file.name.lastIndexOf('.')
        )

    if (
      extension !== '.pdf' &&
      extension !== '.docx'
    ) {

      setError(
        'Only PDF and DOCX files are supported.'
      )

      return false
    }

    if (
      file.size >
      25 * 1024 * 1024
    ) {

      setError(
        'File size must be 25 MB or smaller.'
      )

      return false
    }

    setError('')
    setSelectedFile(file)

    return true
  }


  /* =====================================================
     FILE SELECT
  ===================================================== */

  const handleFileSelect = (event) => {

    const file =
      event.target.files?.[0]

    if (file) {
      validateFile(file)
    }
  }


  /* =====================================================
     DROP
  ===================================================== */

  const handleDrop = (event) => {

    event.preventDefault()

    setIsDragging(false)

    const file =
      event.dataTransfer.files?.[0]

    if (file) {
      validateFile(file)
    }
  }


  /* =====================================================
     REMOVE
  ===================================================== */

  const handleRemove = () => {

    setSelectedFile(null)
    setError('')
    setAnalysisResult(null)
    setAnalysisStep(0)
    setIsAnalyzing(false)

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }


  /* =====================================================
     REAL BACKEND REQUEST
  ===================================================== */

  const handleAnalyze = async () => {
    if (!selectedFile) {
      return
    }

    setError('')
    setAnalysisResult(null)
    setAnalysisStep(0)
    setIsAnalyzing(true)

    let progressTimer = null

    /*
     * The progress UI is intentionally capped at 80%.
     * The final 20% belongs to the real Flask response.
     *
     * This prevents the UI from showing 100% while the
     * backend is still processing the contract.
     */

    progressTimer = setInterval(() => {
      setAnalysisStep((current) => {
        if (current >= steps.length - 2) {
          return current
        }

        return current + 1
      })
    }, 1200)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch(
        'http://127.0.0.1:5000/contracts/upload',
        {
          method: 'POST',
          body: formData,
        }
      )

      let data = null

      try {
        data = await response.json()
      } catch {
        throw new Error(
          'The backend returned an invalid response.'
        )
      }

      if (!response.ok) {
        throw new Error(
          data?.details ||
          data?.error ||
          'Contract processing failed.'
        )
      }

      /*
       * Flask has now actually completed LangGraph processing.
       * Only now do we mark the final step complete.
       */
      setAnalysisStep(steps.length)
      setAnalysisResult(data)
    } catch (err) {
      console.error(
        'Contract analysis error:',
        err
      )

      setError(
        err.message ||
        'Unable to connect to the Contract.AI backend.'
      )
    } finally {
      if (progressTimer) {
        clearInterval(progressTimer)
      }

      setIsAnalyzing(false)
    }
  }
  /* =====================================================
     FILE SIZE
  ===================================================== */

  const formatFileSize = (bytes) => {

    if (
      bytes <
      1024 * 1024
    ) {

      return `${(
        bytes / 1024
      ).toFixed(1)} KB`
    }

    return `${(
      bytes /
      (1024 * 1024)
    ).toFixed(1)} MB`
  }


  /* =====================================================
     PROCESSING SCREEN
  ===================================================== */

  if (isAnalyzing) {

    return (
      <div className="content">

        <section className="page-heading">

          <div>

            <p className="eyebrow">
              AI CONTRACT ANALYSIS
            </p>

            <div className="page-title-with-icon">

              <div className="page-title-icon">
                <ShieldAlert size={25} />
              </div>

              <h1>
                Analyzing Contract
              </h1>

            </div>

            <p className="page-description">
              Contract.AI is processing your
              document through the LangGraph
              backend.
            </p>

          </div>

        </section>


        <div className="analysis-processing-card">

          <div className="processing-document">

            <div className="processing-file-icon">
              <FileText size={24} />
            </div>

            <div className="processing-file-info">

              <strong>
                {selectedFile.name}
              </strong>

              <span>
                {formatFileSize(
                  selectedFile.size
                )}
              </span>

            </div>

            <div className="processing-spinner">
              <span />
            </div>

          </div>


          <div className="processing-divider" />


          <div className="processing-header">

            <div>

              <h2>
                Contract intelligence in progress
              </h2>

              <p>
                Running LangGraph analysis. The final step
                completes when the Flask backend returns.
              </p>

            </div>

            <span className="processing-percent">
              {analysisStep >= steps.length
                ? 100
                : Math.min(
                    80,
                    Math.round(
                      ((analysisStep + 1) /
                        steps.length) * 100
                    )
                  )}%
            </span>

          </div>


          <div className="processing-progress">

            <div
              className="processing-progress-bar"
              style={{
                width: `${
                  analysisStep >= steps.length
                    ? 100
                    : Math.min(
                        80,
                        ((analysisStep + 1) /
                          steps.length) * 100
                      )
                }%`,
              }}
            />

          </div>


          <div className="analysis-steps">

            {steps.map(
              (step, index) => {

                const completed =
                  analysisStep >= steps.length ||
                  index < analysisStep

                const current =
                  analysisStep < steps.length &&
                  index === analysisStep

                return (
                  <div
                    className={`analysis-step ${
                      completed
                        ? 'completed'
                        : ''
                    } ${
                      current
                        ? 'current'
                        : ''
                    }`}
                    key={step}
                  >

                    <div className="analysis-step-indicator">

                      {completed ? (

                        <span className="step-check">
                          ✓
                        </span>

                      ) : current ? (

                        <span className="step-spinner" />

                      ) : (

                        <span className="step-number">
                          {index + 1}
                        </span>

                      )}

                    </div>


                    <div className="analysis-step-content">

                      <strong>
                        {step}
                      </strong>

                      <span>
                        {completed
                          ? 'Completed'
                          : current
                            ? 'Processing'
                            : 'Waiting'}
                      </span>

                    </div>

                  </div>
                )
              }
            )}

          </div>

        </div>

      </div>
    )
  }


  /* =====================================================
     RESULTS SCREEN
  ===================================================== */

  if (analysisResult) {

    const obligations =
      Array.isArray(
        analysisResult.obligations
      )
        ? analysisResult.obligations
        : []


    const riskResults =
      obligations.map(
        (item, index) =>
          normalizeRisk(
            item,
            index
          )
      )


    const highRiskCount =
      riskResults.filter(
        item =>
          item.level === 'HIGH'
      ).length


    const mediumRiskCount =
      riskResults.filter(
        item =>
          item.level === 'MEDIUM'
      ).length


    const lowRiskCount =
      riskResults.filter(
        item =>
          item.level === 'LOW' ||
          item.level === 'NO_DEADLINE'
      ).length

    const reviewRiskCount =
      riskResults.filter(
        item =>
          item.level === 'REVIEW'
      ).length


    return (
      <div className="content">

        <section className="page-heading">

          <div>

            <p className="eyebrow">
              AI CONTRACT ANALYSIS
            </p>

            <div className="page-title-with-icon">

              <div className="page-title-icon analysis-complete-icon">
                <CheckCircle2 size={25} />
              </div>

              <h1>
                Analysis Complete
              </h1>

            </div>

            <p className="page-description">
              Contract.AI successfully processed
              your agreement.
            </p>

          </div>

        </section>


        {/* SUMMARY */}

        <div className="result-summary-card">

          <div className="result-success">

            <CheckCircle2 size={20} />

            <div>

              <strong>
                Contract processed successfully
              </strong>

              <span>
                {analysisResult.filename}
              </span>

            </div>

          </div>

          <span className="backend-badge">
            LangGraph
          </span>

        </div>


        {/* METRICS */}

        <div className="stats-grid result-stats">

          <ResultMetric
            icon={<ListChecks size={19} />}
            label="Obligations"
            value={obligations.length}
          />

          <ResultMetric
            icon={<AlertTriangle size={19} />}
            label="High risk signals"
            value={highRiskCount}
            warning
          />

          <ResultMetric
            icon={<ShieldAlert size={19} />}
            label="Medium risk signals"
            value={mediumRiskCount}
          />

          <ResultMetric
            icon={<CheckCircle2 size={19} />}
            label="Low risk signals"
            value={lowRiskCount}
          />

          <ResultMetric
            icon={<ShieldAlert size={19} />}
            label="Needs review"
            value={reviewRiskCount}
            warning={reviewRiskCount > 0}
          />

        </div>


        {/* RISK OVERVIEW */}

        <div className="panel result-panel">

          <div className="panel-header">

            <div>

              <h2>
                Risk Overview
              </h2>

              <p>
                Review signals detected in the
                extracted contractual information.
              </p>

            </div>

          </div>


          <div className="risk-overview">

            <RiskOverviewItem
              label="High attention"
              value={highRiskCount}
              type="high"
            />

            <RiskOverviewItem
              label="Medium attention"
              value={mediumRiskCount}
              type="medium"
            />

            <RiskOverviewItem
              label="Lower attention"
              value={lowRiskCount}
              type="low"
            />

            <RiskOverviewItem
              label="Needs review"
              value={reviewRiskCount}
              type="review"
            />

          </div>

        </div>


        {/* OBLIGATIONS */}

        <div className="panel result-panel">

          <div className="panel-header">

            <div>

              <h2>
                Extracted Obligations
              </h2>

              <p>
                Contractual responsibilities returned
                by the LangGraph pipeline.
              </p>

            </div>

          </div>


          {obligations.length === 0 ? (

            <div className="empty-result">
              No obligations were returned by
              the current analysis pipeline.
            </div>

          ) : (

            <div className="result-obligation-list">

              {obligations.map(
                (item, index) => {

                  const obligation =
                    normalizeObligation(
                      item
                    )

                  const risk =
                    riskResults[index]

                  return (
                    <div
                      className="result-obligation"
                      key={index}
                    >

                      <div className="result-obligation-number">
                        {index + 1}
                      </div>


                      <div className="result-obligation-main">

                        <strong>
                          {obligation.title}
                        </strong>

                        {obligation.description && (
                          <p>
                            {obligation.description}
                          </p>
                        )}

                        <div className="result-obligation-meta">

                          {obligation.dueDate && (
                            <span>
                              <CalendarDays size={13} />
                              {obligation.dueDate}
                            </span>
                          )}

                          {obligation.responsibleParty && (
                            <span>
                              Responsible:
                              {' '}
                              {obligation.responsibleParty}
                            </span>
                          )}

                          {obligation.clauseReference && (
                            <span>
                              Clause:
                              {' '}
                              {obligation.clauseReference}
                            </span>
                          )}

                          {risk.verificationStatus && (
                            <span>
                              Verification:
                              {' '}
                              {risk.verificationStatus}
                            </span>
                          )}

                          {risk.groundingScore !== null && (
                            <span>
                              Grounding:
                              {' '}
                              {Math.round(
                                risk.groundingScore * 100
                              )}%
                            </span>
                          )}

                        </div>

                      </div>


                      <RiskBadge
                        level={risk.level}
                      />

                    </div>
                  )
                }
              )}

            </div>

          )}

        </div>


        {/* RISK SIGNALS */}

        <div className="panel result-panel">

          <div className="panel-header">

            <div>

              <h2>
                Risk Signals
              </h2>

              <p>
                Clause-level review signals generated
                from the extracted contractual text.
              </p>

            </div>

          </div>


          {riskResults.length === 0 ? (

            <div className="empty-result">
              No obligation text was returned for
              risk-signal analysis.
            </div>

          ) : (

            <div className="risk-list">

              {riskResults.map(
                (risk, index) => (

                  <div
                    className="risk-row"
                    key={index}
                  >

                    <RiskBadge
                      level={risk.level}
                    />

                    <div className="risk-info">

                      <strong>
                        {risk.title}
                      </strong>

                      <span>
                        Obligation {index + 1}
                      </span>

                      <p>
                        {risk.reason}
                      </p>

                      {risk.clauseRisks.length > 0 && (
                        <div className="risk-tags">
                          {risk.clauseRisks.map(
                            (signal, signalIndex) => (
                              <span
                                className="risk-tag"
                                key={`${index}-${signalIndex}`}
                              >
                                {signal.category || 'Risk signal'}
                              </span>
                            )
                          )}
                        </div>
                      )}

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>


        {/* ACTION */}

        <div className="result-actions">

          <button
            type="button"
            className="primary-button"
            onClick={() => {

              setSelectedFile(null)
              setAnalysisResult(null)
              setAnalysisStep(0)
              setError('')

              if (fileInputRef.current) {
                fileInputRef.current.value = ''
              }

            }}
          >

            <Upload size={17} />

            Analyze Another Contract

          </button>

        </div>

      </div>
    )
  }


  /* =====================================================
     UPLOAD SCREEN
  ===================================================== */

  return (
    <div className="content">

      <section className="page-heading">

        <div>

          <p className="eyebrow">
            DOCUMENT INGESTION
          </p>

          <div className="page-title-with-icon">

            <div className="page-title-icon">
              <Upload size={25} />
            </div>

            <h1>
              Upload Contract
            </h1>

          </div>

          <p className="page-description">
            Upload a PDF or DOCX agreement
            to begin real contract analysis.
          </p>

        </div>

      </section>


      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden-file-input"
        onChange={handleFileSelect}
      />


      {!selectedFile ? (

        <div
          className={`upload-panel ${
            isDragging
              ? 'upload-panel-dragging'
              : ''
          }`}
          onDragOver={(event) => {
            event.preventDefault()
            setIsDragging(true)
          }}
          onDragLeave={() => {
            setIsDragging(false)
          }}
          onDrop={handleDrop}
        >

          <div className="upload-icon">
            <Upload size={28} />
          </div>

          <h2>
            Drop your contract here
          </h2>

          <p>
            Drag and drop your contract here,
            or browse your computer to select
            a file.
          </p>

          <button
            type="button"
            className="primary-button"
            onClick={() =>
              fileInputRef.current?.click()
            }
          >

            <Upload size={17} />

            Browse Files

          </button>

          <span className="upload-hint">
            Supported formats: PDF, DOCX ·
            Maximum size: 25 MB
          </span>

          {error && (
            <div className="upload-error">
              {error}
            </div>
          )}

        </div>

      ) : (

        <div className="selected-file-section">

          <div className="selected-file-card">

            <div className="selected-file-icon">
              <FileText size={23} />
            </div>


            <div className="selected-file-info">

              <strong>
                {selectedFile.name}
              </strong>

              <span>
                {formatFileSize(selectedFile.size)}
                {' · '}
                {selectedFile.name
                  .toLowerCase()
                  .endsWith('.pdf')
                  ? 'PDF'
                  : 'DOCX'}
              </span>

            </div>


            <div className="file-valid">

              <span className="file-valid-dot" />

              Ready

            </div>


            <button
              type="button"
              className="remove-file-button"
              onClick={handleRemove}
            >
              <X size={18} />
            </button>

          </div>


          <div className="analyze-section">

            <div>

              <h3>
                Ready for real analysis
              </h3>

              <p>
                Your document will be sent to the
                Flask API and processed by the
                LangGraph contract pipeline.
              </p>

            </div>


            <button
              type="button"
              className="primary-button analyze-button"
              onClick={handleAnalyze}
            >

              <ShieldAlert size={17} />

              Analyze Contract

            </button>

          </div>


          {error && (
            <div className="upload-error">
              {error}
            </div>
          )}

        </div>

      )}


      <div className="analysis-section">

        <div className="analysis-section-heading">

          <h2>
            What Contract.AI analyzes
          </h2>

          <p>
            Information extracted from your
            agreement.
          </p>

        </div>


        <div className="analysis-features">

          <AnalysisFeature
            icon={<ListChecks size={19} />}
            title="Obligations"
            description="Identify contractual responsibilities."
          />

          <AnalysisFeature
            icon={<CalendarDays size={19} />}
            title="Important Dates"
            description="Extract deadlines and time-sensitive commitments."
          />

          <AnalysisFeature
            icon={<ShieldAlert size={19} />}
            title="Risk Signals"
            description="Identify clauses requiring additional review."
          />

          <AnalysisFeature
            icon={<FileText size={19} />}
            title="Key Terms"
            description="Surface important contractual information."
          />

        </div>

      </div>

    </div>
  )
}


/* =========================================================
   RISK ANALYSIS
========================================================= */

/*
 * Risk information now comes from the real backend risk engine.
 *
 * The frontend does not invent risk levels from keywords.
 * It displays:
 *
 *   risk_tier
 *   clause_risks
 *   risk_reasons
 *   days_until_deadline
 *   verification_status
 *   grounding_score
 *
 * returned by Flask/LangGraph.
 */

function normalizeRisk(item, index) {
  const obligation = normalizeObligation(item)

  const backendLevel =
    String(
      item?.risk_tier ||
      item?.riskTier ||
      ''
    ).toUpperCase()

  let level = backendLevel

  if (!['HIGH', 'MEDIUM', 'LOW', 'REVIEW', 'NO_DEADLINE'].includes(level)) {
    level = 'LOW'
  }

  const clauseRisks =
    Array.isArray(item?.clause_risks)
      ? item.clause_risks
      : []

  const riskReasons =
    Array.isArray(item?.risk_reasons)
      ? item.risk_reasons
      : []

  const verificationStatus =
    item?.verification_status ||
    'PENDING'

  const groundingScore =
    typeof item?.grounding_score === 'number'
      ? item.grounding_score
      : null

  let title = 'Routine contractual review'
  let reason =
    'No elevated risk signal was returned by the backend risk engine.'

  if (level === 'HIGH') {
    title = 'High-attention obligation'
    reason =
      riskReasons.join(' ') ||
      'The backend risk engine identified a high-attention condition.'
  } else if (level === 'MEDIUM') {
    title = 'Medium-attention obligation'
    reason =
      riskReasons.join(' ') ||
      'The backend risk engine identified a medium-attention condition.'
  } else if (level === 'REVIEW') {
    title = 'Verification requires review'
    reason =
      riskReasons.join(' ') ||
      'The extracted obligation could not be sufficiently grounded in the source contract text.'
  } else if (level === 'NO_DEADLINE') {
    title = 'No explicit deadline'
    reason =
      riskReasons.join(' ') ||
      'The obligation does not contain a deadline that the current parser could resolve.'
  } else if (clauseRisks.length > 0) {
    title = 'Clause-level review signal'
    reason =
      riskReasons.join(' ') ||
      clauseRisks
        .map(
          (risk) =>
            `${risk.category || 'Risk signal'}: ${risk.matched_pattern || 'matched'}`
        )
        .join('; ')
  }

  return {
    ...obligation,
    level,
    title,
    reason,
    clauseRisks,
    riskReasons,
    verificationStatus,
    groundingScore,
  }
}


/* =========================================================
   NORMALIZE BACKEND OBLIGATION
========================================================= */

function normalizeObligation(item) {
  if (
    typeof item === 'string'
  ) {
    return {
      title: item,
      description: '',
      dueDate: '',
      responsibleParty: '',
      clauseReference: '',
    }
  }

  if (
    !item ||
    typeof item !== 'object'
  ) {
    return {
      title: 'Unspecified obligation',
      description: '',
      dueDate: '',
      responsibleParty: '',
      clauseReference: '',
    }
  }

  return {
    title:
      item.obligation_text ||
      item.obligationText ||
      item.title ||
      item.obligation ||
      item.description ||
      item.text ||
      item.clause ||
      'Contractual obligation',

    description:
      item.obligation_text ||
      item.obligationText ||
      item.description ||
      item.text ||
      item.clause ||
      '',

    dueDate:
      item.deadline ||
      item.due_date ||
      item.dueDate ||
      item.parsed_deadline ||
      item.date ||
      '',

    responsibleParty:
      item.party_responsible ||
      item.partyResponsible ||
      item.responsible_party ||
      item.responsibleParty ||
      item.party ||
      item.owner ||
      '',

    clauseReference:
      item.clause_reference ||
      item.clauseReference ||
      '',
  }
}


/* =========================================================
   RISK BADGE
========================================================= */

/* =========================================================
   RISK BADGE
========================================================= */

function RiskBadge({
  level,
}) {
  const normalizedLevel =
    String(level || 'LOW').toUpperCase()

  const displayLevel =
    normalizedLevel === 'NO_DEADLINE'
      ? 'NO DEADLINE'
      : normalizedLevel

  return (
    <span
      className={`risk-badge ${
        normalizedLevel.toLowerCase()
      }`}
    >
      {normalizedLevel === 'HIGH' && (
        <AlertTriangle size={13} />
      )}

      {(normalizedLevel === 'MEDIUM' ||
        normalizedLevel === 'REVIEW') && (
        <ShieldAlert size={13} />
      )}

      {(normalizedLevel === 'LOW' ||
        normalizedLevel === 'NO_DEADLINE') && (
        <CheckCircle2 size={13} />
      )}

      {displayLevel}
    </span>
  )
}


/* =========================================================
   RESULT METRIC
========================================================= */

function ResultMetric({
  icon,
  label,
  value,
  warning = false,
}) {

  return (
    <div className="stat-card">

      <div
        className={`stat-icon ${
          warning ? 'warning' : ''
        }`}
      >
        {icon}
      </div>

      <div className="stat-content">

        <span className="stat-label">
          {label}
        </span>

        <strong className="stat-value">
          {value}
        </strong>

      </div>

    </div>
  )
}


/* =========================================================
   RISK OVERVIEW ITEM
========================================================= */

function RiskOverviewItem({
  label,
  value,
  type,
}) {

  return (
    <div className="risk-overview-item">

      <div
        className={`risk-overview-dot ${type}`}
      />

      <div>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>

    </div>
  )
}


/* =========================================================
   CONTRACTS PAGE
========================================================= */

function ContractsPage() {

  return (
    <PagePlaceholder
      eyebrow="CONTRACT MANAGEMENT"
      title="Contracts"
      description="View and manage uploaded contracts."
      icon={<FileText size={25} />}
    >

      <div className="placeholder-toolbar">

        <div className="fake-search">
          <Search size={17} />
          <span>
            Search contracts...
          </span>
        </div>

        <Link
          to="/upload"
          className="primary-button"
        >
          <Plus size={18} />
          Upload Contract
        </Link>

      </div>


      <div className="panel">

        <ContractRow
          name="Software Development Agreement"
          type="Development"
          date="Sep 16, 2026"
          status="Analyzed"
          statusType="success"
        />

        <ContractRow
          name="Non-Disclosure Agreement"
          type="NDA"
          date="Sep 14, 2026"
          status="Analyzed"
          statusType="success"
        />

        <ContractRow
          name="Cloud Services Agreement"
          type="Services"
          date="Sep 12, 2026"
          status="Review required"
          statusType="warning"
        />

      </div>

    </PagePlaceholder>
  )
}


/* =========================================================
   OBLIGATIONS PAGE
========================================================= */

function ObligationsPage() {

  return (
    <PagePlaceholder
      eyebrow="OBLIGATION TRACKING"
      title="Obligations"
      description="Track contractual responsibilities and deadlines."
      icon={<ListChecks size={25} />}
    >

      <div className="panel">

        <div className="panel-header">

          <div>

            <h2>
              Upcoming Obligations
            </h2>

            <p>
              Responsibilities extracted from contracts.
            </p>

          </div>

        </div>


        <Obligation
          title="Submit monthly report"
          contract="Software Development Agreement"
          date="Sep 20"
          urgent
        />

        <Obligation
          title="Service renewal review"
          contract="Cloud Services Agreement"
          date="Sep 24"
        />

        <Obligation
          title="Insurance certificate"
          contract="Vendor Partnership Agreement"
          date="Sep 28"
        />

      </div>

    </PagePlaceholder>
  )
}


/* =========================================================
   RISKS PAGE
========================================================= */

function RisksPage() {

  return (
    <PagePlaceholder
      eyebrow="AI RISK ANALYSIS"
      title="Risk Analysis"
      description="Review contractual information that may require attention."
      icon={<ShieldAlert size={25} />}
    >

      <div className="risk-summary-grid">

        <div className="risk-summary-card">

          <span>
            High attention
          </span>

          <strong>
            02
          </strong>

          <p>
            Requires detailed review
          </p>

        </div>


        <div className="risk-summary-card">

          <span>
            Medium attention
          </span>

          <strong>
            03
          </strong>

          <p>
            Worth reviewing
          </p>

        </div>


        <div className="risk-summary-card">

          <span>
            Contracts analyzed
          </span>

          <strong>
            19
          </strong>

          <p>
            AI processing completed
          </p>

        </div>

      </div>


      <div className="panel">

        <div className="panel-header">

          <div>

            <h2>
              Risk Signals
            </h2>

            <p>
              Potential areas requiring contractual review.
            </p>

          </div>

        </div>


        <div className="risk-row">

          <RiskBadge level="HIGH" />

          <div className="risk-info">

            <strong>
              Broad termination provision
            </strong>

            <span>
              Example contract · Section 8
            </span>

            <p>
              Review the termination conditions,
              notice period, and consequences.
            </p>

          </div>

        </div>


        <div className="risk-row">

          <RiskBadge level="HIGH" />

          <div className="risk-info">

            <strong>
              Liability exposure
            </strong>

            <span>
              Example contract · Section 11
            </span>

            <p>
              Review whether liability is capped
              and which damages are excluded.
            </p>

          </div>

        </div>


        <div className="risk-row">

          <RiskBadge level="MEDIUM" />

          <div className="risk-info">

            <strong>
              Automatic renewal
            </strong>

            <span>
              Example contract · Section 5
            </span>

            <p>
              Review renewal dates and notice requirements.
            </p>

          </div>

        </div>

      </div>

    </PagePlaceholder>
  )
}


/* =========================================================
   SETTINGS
========================================================= */

function SettingsPage() {

  return (
    <PagePlaceholder
      eyebrow="WORKSPACE SETTINGS"
      title="Settings"
      description="Manage your Contract.AI workspace."
      icon={<Settings size={25} />}
    >

      <div className="panel settings-panel">

        <div className="panel-header">

          <div>

            <h2>
              Workspace
            </h2>

            <p>
              Basic workspace configuration
            </p>

          </div>

        </div>


        <div className="settings-row">

          <div>

            <strong>
              Workspace name
            </strong>

            <span>
              Contract.AI Workspace
            </span>

          </div>

          <button className="secondary-button">
            Edit
          </button>

        </div>


        <div className="settings-row">

          <div>

            <strong>
              AI analysis
            </strong>

            <span>
              Contract intelligence and risk detection
            </span>

          </div>

          <span className="enabled-pill">
            Enabled
          </span>

        </div>

      </div>

    </PagePlaceholder>
  )
}


/* =========================================================
   PAGE PLACEHOLDER
========================================================= */

function PagePlaceholder({
  eyebrow,
  title,
  description,
  icon,
  children,
}) {

  return (
    <div className="content">

      <section className="page-heading">

        <div>

          <p className="eyebrow">
            {eyebrow}
          </p>

          <div className="page-title-with-icon">

            <div className="page-title-icon">
              {icon}
            </div>

            <h1>
              {title}
            </h1>

          </div>

          <p className="page-description">
            {description}
          </p>

        </div>

      </section>

      {children}

    </div>
  )
}


/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  label,
  value,
  change,
  icon,
  warning = false,
}) {

  return (
    <div className="stat-card">

      <div
        className={`stat-icon ${
          warning ? 'warning' : ''
        }`}
      >
        {icon}
      </div>

      <div className="stat-content">

        <span className="stat-label">
          {label}
        </span>

        <strong className="stat-value">
          {value}
        </strong>

        <span
          className={`stat-change ${
            warning
              ? 'warning-text'
              : ''
          }`}
        >
          {change}
        </span>

      </div>

    </div>
  )
}


/* =========================================================
   CONTRACT ROW
========================================================= */

function ContractRow({
  name,
  type,
  date,
  status,
  statusType,
}) {

  return (
    <div className="contract-row">

      <div className="contract-icon">
        <FileText size={19} />
      </div>

      <div className="contract-details">

        <strong>
          {name}
        </strong>

        <span>
          {type} · {date}
        </span>

      </div>

      <span
        className={`status-pill ${
          statusType
        }`}
      >

        <span className="status-dot" />

        {status}

      </span>

    </div>
  )
}


/* =========================================================
   OBLIGATION
========================================================= */

function Obligation({
  title,
  contract,
  date,
  urgent = false,
}) {

  return (
    <div className="obligation-item">

      <div
        className={`obligation-marker ${
          urgent
            ? 'urgent'
            : ''
        }`}
      />

      <div className="obligation-content">

        <strong>
          {title}
        </strong>

        <span>
          {contract}
        </span>

      </div>

      <div
        className={`obligation-date ${
          urgent
            ? 'urgent-text'
            : ''
        }`}
      >
        {date}
      </div>

    </div>
  )
}


/* =========================================================
   ANALYSIS FEATURE
========================================================= */

function AnalysisFeature({
  icon,
  title,
  description,
}) {

  return (
    <div className="analysis-feature">

      <div className="feature-icon">
        {icon}
      </div>

      <div>

        <strong>
          {title}
        </strong>

        <p>
          {description}
        </p>

      </div>

    </div>
  )
}


export default App
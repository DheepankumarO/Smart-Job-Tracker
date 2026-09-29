import { useEffect, useState } from 'react'
import './App.css'
import ApplicationForm from './components/ApplicationForm'
import type { JobApplication } from './types'

function App() {
  const [applications, setApplications] = useState<JobApplication[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [isFormOpen, setIsFormOpen] = useState(false)

  useEffect(() => {
    async function loadApplications() {
      try {
        const response = await fetch(
          'http://localhost:8000/applications'
        )

        if (!response.ok) {
          throw new Error('Could not load applications')
        }

        const data: JobApplication[] = await response.json()
        setApplications(data)
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message)
        } else {
          setError('An unexpected error occurred')
        }
      } finally {
        setIsLoading(false)
      }
    }

    loadApplications()
  }, [])

  const interviewCount = applications.filter(
    (application) => application.status === 'Interview'
  ).length

  const offerCount = applications.filter(
    (application) => application.status === 'Offer'
  ).length

  return (
    <main className="app-shell">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">SMART JOB TRACKER</p>
          <h1>Application Dashboard</h1>
          <p className="subtitle">
            Track opportunities from saved jobs to final offers.
          </p>
        </div>

        <button
          className="primary-button"
          type="button"
          onClick={() => setIsFormOpen(true)}
        >
          Add application
        </button>
      </header>

      {isFormOpen && (
        <ApplicationForm
          onClose={() => setIsFormOpen(false)}
          onApplicationCreated={(newApplication) => {
            setApplications((currentApplications) => [
              ...currentApplications,
              newApplication,
            ])

            setIsFormOpen(false)
          }}
        />
      )}

      <section className="summary-grid" aria-label="Application summary">
        <article className="summary-card">
          <span>Total applications</span>
          <strong>{applications.length}</strong>
        </article>

        <article className="summary-card">
          <span>Interviews</span>
          <strong>{interviewCount}</strong>
        </article>

        <article className="summary-card">
          <span>Offers</span>
          <strong>{offerCount}</strong>
        </article>
      </section>

      <section className="applications-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">PIPELINE</p>
            <h2>Your applications</h2>
          </div>

          <span className="record-count">
            {applications.length} records
          </span>
        </div>

        {isLoading && (
          <div className="message-state">
            <p>Loading applications...</p>
          </div>
        )}

        {error && (
          <div className="message-state error-message">
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && applications.length === 0 && (
          <div className="empty-state">
            <h3>No applications found</h3>
            <p>Add an application to begin tracking your opportunities.</p>
          </div>
        )}

        {!isLoading && !error && applications.length > 0 && (
          <div className="table-container">
            <table className="applications-table">
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Position</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Applied</th>
                  <th>Job link</th>
                </tr>
              </thead>

              <tbody>
                {applications.map((application) => (
                  <tr key={application.id}>
                    <td>{application.company}</td>
                    <td>{application.position}</td>
                    <td>{application.location}</td>
                    <td>
                      <span className="status-badge">
                        {application.status}
                      </span>
                    </td>
                    <td>{application.application_date}</td>
                    <td>
                      <a
                        href={application.job_url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        View job
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  )
}

export default App
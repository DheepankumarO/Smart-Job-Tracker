import { useEffect, useState } from 'react'
import './App.css'
import ApplicationForm from './components/ApplicationForm'
import type { JobApplication } from './types'

function App() {
  const [applications, setApplications] = useState<JobApplication[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [actionError, setActionError] = useState('')
  const [updatingId, setUpdatingId] = useState<number | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')
  const [sortOption, setSortOption] = useState('newest')
  const [applicationToEdit, setApplicationToEdit] = useState<JobApplication | null>(null)

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

  const normalizedSearchTerm = searchTerm.trim().toLowerCase()

  const filteredApplications = applications
    .filter((application) => {
      const matchesSearch =
        application.company
          .toLowerCase()
          .includes(normalizedSearchTerm) ||
        application.position
          .toLowerCase()
          .includes(normalizedSearchTerm) ||
        application.location
          .toLowerCase()
          .includes(normalizedSearchTerm)

      const matchesStatus =
        statusFilter === 'All' ||
        application.status === statusFilter

      return matchesSearch && matchesStatus
    })
    .sort((firstApplication, secondApplication) => {
      if (sortOption === 'company') {
        return firstApplication.company.localeCompare(
          secondApplication.company
        )
      }

      const firstDate = new Date(
        firstApplication.application_date
      ).getTime()

      const secondDate = new Date(
        secondApplication.application_date
      ).getTime()

      if (sortOption === 'oldest') {
        return firstDate - secondDate
      }

      return secondDate - firstDate
    })
  
  async function handleDelete(application: JobApplication) {
    const confirmed = window.confirm(
      `Delete the application for ${application.company}?`
    )

    if (!confirmed) {
      return
    }

    setDeletingId(application.id)
    setActionError('')

    try {
      const response = await fetch(
        `http://localhost:8000/applications/${application.id}`,
        {
          method: 'DELETE',
        }
      )

      if (!response.ok) {
        throw new Error('Could not delete the application')
      }

      setApplications((currentApplications) =>
        currentApplications.filter(
          (currentApplication) =>
            currentApplication.id !== application.id
        )
      )
    } catch (error) {
      if (error instanceof Error) {
        setActionError(error.message)
      } else {
        setActionError('An unexpected error occurred')
      }
    } finally {
      setDeletingId(null)
    }
  }

  async function handleStatusChange(
    applicationId: number,
    newStatus: string
  ) {
    setUpdatingId(applicationId)
    setActionError('')

    try {
      const response = await fetch(
        `http://localhost:8000/applications/${applicationId}/status`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            status: newStatus,
          }),
        }
      )

      if (!response.ok) {
        throw new Error('Could not update the application status')
      }

      setApplications((currentApplications) =>
        currentApplications.map((application) =>
          application.id === applicationId
            ? {
                ...application,
                status: newStatus,
              }
            : application
        )
      )
    } catch (error) {
      if (error instanceof Error) {
        setActionError(error.message)
      } else {
        setActionError('An unexpected error occurred')
      }
    } finally {
      setUpdatingId(null)
    }
  }

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
          onClick={() => {
            setApplicationToEdit(null)
            setIsFormOpen(true)
          }}
        >
          Add application
        </button>
      </header>

      {isFormOpen && (
        <ApplicationForm
          key={applicationToEdit?.id ?? 'new'}
          applicationToEdit={applicationToEdit}
          onClose={() => {
            setIsFormOpen(false)
            setApplicationToEdit(null)
          }}
          onApplicationSaved={(savedApplication) => {
            setApplications((currentApplications) => {
              const applicationAlreadyExists =
                currentApplications.some(
                  (application) =>
                    application.id === savedApplication.id
                )

              if (applicationAlreadyExists) {
                return currentApplications.map((application) =>
                  application.id === savedApplication.id
                    ? savedApplication
                    : application
                )
              }

              return [
                ...currentApplications,
                savedApplication,
              ]
            })

            setIsFormOpen(false)
            setApplicationToEdit(null)
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

      <section className="filter-panel" aria-label="Application filters">
        <label>
          Search
          <input
            type="search"
            placeholder="Company, position, or location"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
        </label>

        <label>
          Status
          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="All">All statuses</option>
            <option value="Saved">Saved</option>
            <option value="Applied">Applied</option>
            <option value="Interview">Interview</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
            <option value="Withdrawn">Withdrawn</option>
          </select>
        </label>

        <label>
          Sort
          <select
            value={sortOption}
            onChange={(event) => setSortOption(event.target.value)}
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="company">Company A–Z</option>
          </select>
        </label>
      </section>

      <section className="applications-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">PIPELINE</p>
            <h2>Your applications</h2>
          </div>

          <span className="record-count">
            {filteredApplications.length} of {applications.length} records
          </span>
        </div>

        {actionError && (
          <div className="action-error">
            {actionError}
          </div>
        )}

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
        
        {/* Applications exist, but none match the filters */}
        {!isLoading &&
          !error &&
          applications.length > 0 &&
          filteredApplications.length === 0 && (
            <div className="empty-state">
              <h3>No matching applications</h3>
              <p>Try changing your search or status filter.</p>
            </div>
          )}

        {!isLoading && !error && filteredApplications.length > 0 && (
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
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {filteredApplications.map((application) => (
                  <tr key={application.id}>
                    <td>{application.company}</td>
                    <td>{application.position}</td>
                    <td>{application.location}</td>
                    <td>
                      <select
                        className="status-select"
                        value={application.status}
                        onChange={(event) =>
                          handleStatusChange(
                            application.id,
                            event.target.value
                          )
                        }
                        disabled={updatingId === application.id}
                        aria-label={`Update status for ${application.company}`}
                      >
                        <option value="Saved">Saved</option>
                        <option value="Applied">Applied</option>
                        <option value="Interview">Interview</option>
                        <option value="Offer">Offer</option>
                        <option value="Rejected">Rejected</option>
                        <option value="Withdrawn">Withdrawn</option>
                      </select>
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
                    <td>
                      <div className="row-actions">
                        <button
                          className="edit-button"
                          type="button"
                          onClick={() => {
                            setApplicationToEdit(application)
                            setIsFormOpen(true)

                            window.scrollTo({
                              top: 0,
                              behavior: 'smooth',
                            })
                          }}
                        >
                          Edit
                        </button>

                        <button
                          className="delete-button"
                          type="button"
                          onClick={() => handleDelete(application)}
                          disabled={deletingId === application.id}
                        >
                          {deletingId === application.id
                            ? 'Deleting...'
                            : 'Delete'}
                        </button>
                      </div>
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
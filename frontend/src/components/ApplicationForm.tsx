import { useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import type {
  JobApplication,
  NewJobApplication,
} from '../types'

interface ApplicationFormProps {
  applicationToEdit: JobApplication | null
  onClose: () => void
  onApplicationSaved: (application: JobApplication) => void
}

const emptyFormData: NewJobApplication = {
  company: '',
  position: '',
  location: '',
  job_url: '',
  application_date: '',
  status: 'Saved',
  notes: '',
}

function ApplicationForm({
  applicationToEdit,
  onClose,
  onApplicationSaved,
}: ApplicationFormProps) {
  const isEditing = applicationToEdit !== null

  const initialFormData: NewJobApplication = applicationToEdit
    ? {
        company: applicationToEdit.company,
        position: applicationToEdit.position,
        location: applicationToEdit.location,
        job_url: applicationToEdit.job_url ?? '',
        application_date: applicationToEdit.application_date,
        status: applicationToEdit.status,
        notes: applicationToEdit.notes ?? '',
      }
    : emptyFormData

  const [formData, setFormData] =
    useState<NewJobApplication>(initialFormData)

  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')

  function handleChange(
    event: ChangeEvent<
      HTMLInputElement |
      HTMLSelectElement |
      HTMLTextAreaElement
    >
  ) {
    const { name, value } = event.target

    setFormData((currentFormData) => ({
      ...currentFormData,
      [name]: value,
    }))
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()
    setIsSaving(true)
    setError('')

    const url = isEditing
      ? `http://localhost:8000/applications/${applicationToEdit.id}`
      : 'http://localhost:8000/applications'

    const method = isEditing ? 'PUT' : 'POST'

    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error(
          isEditing
            ? 'Could not update the application'
            : 'Could not create the application'
        )
      }

      const savedApplication: JobApplication =
        await response.json()

      onApplicationSaved(savedApplication)
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError('An unexpected error occurred')
      }
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <section className="form-panel">
      <div className="form-header">
        <div>
          <p className="eyebrow">
            {isEditing ? 'EDIT RECORD' : 'NEW RECORD'}
          </p>

          <h2>
            {isEditing
              ? 'Edit application'
              : 'Add an application'}
          </h2>
        </div>

        <button
          className="close-button"
          type="button"
          onClick={onClose}
          aria-label="Close form"
        >
          ×
        </button>
      </div>

      <form
        className="application-form"
        onSubmit={handleSubmit}
      >
        <label>
          Company
          <input
            name="company"
            type="text"
            value={formData.company}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Position
          <input
            name="position"
            type="text"
            value={formData.position}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Location
          <input
            name="location"
            type="text"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Job URL
          <input
            name="job_url"
            type="url"
            value={formData.job_url}
            onChange={handleChange}
          />
        </label>

        <label>
          Application date
          <input
            name="application_date"
            type="date"
            value={formData.application_date}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Status
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="Saved">Saved</option>
            <option value="Applied">Applied</option>
            <option value="Interview">Interview</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
            <option value="Withdrawn">Withdrawn</option>
          </select>
        </label>

        <label className="full-width">
          Notes
          <textarea
            name="notes"
            rows={4}
            value={formData.notes}
            onChange={handleChange}
          />
        </label>

        {error && (
          <p className="form-error full-width">
            {error}
          </p>
        )}

        <div className="form-actions full-width">
          <button
            className="secondary-button"
            type="button"
            onClick={onClose}
            disabled={isSaving}
          >
            Cancel
          </button>

          <button
            className="primary-button"
            type="submit"
            disabled={isSaving}
          >
            {isSaving
              ? 'Saving...'
              : isEditing
                ? 'Update application'
                : 'Save application'}
          </button>
        </div>
      </form>
    </section>
  )
}

export default ApplicationForm
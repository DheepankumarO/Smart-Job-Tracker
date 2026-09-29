export interface JobApplication {
  id: number
  company: string
  position: string
  location: string
  job_url: string
  application_date: string
  status: string
  notes: string
}

export type NewJobApplication = Omit<JobApplication, 'id'>
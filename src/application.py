class JobApplication:
    def __init__(self, company, position, location, URL, application_date, status):
        self.company = company
        self.position = position
        self.location = location
        self.Job_URL = URL
        self.application_date = application_date
        self.status = status
        
    def __str__(self):
        return(
            f"company: {self.company}\n"
            f"position: {self.position}\n"
            f"Location: {self.location}\n"
            f"Job URL: {self.Job_URL}\n"
            f"Application date: {self.application_date}\n"
            f"status: {self.status}"
    )    

application_one = JobApplication(
    "TechCorp", 
    "Software Engineer", 
    "New York", 
    "https://techcorp.com/jobs/1",
    "2026/09/03",
    "Applied"
    )



print(application_one)
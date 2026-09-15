import json

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
    pass

    def to_dict(self):
        return {
            "company": self.company,
            "position": self.position,
            "location": self.location,
            "job_url": self.Job_URL,
            "application_date": self.application_date,
            "status": self.status
        }

class ApplicationTracker:
    def __init__(self):
        self.applications = []
        
    def add_applications(self, application):
        self.applications.append(application)
        
    def list_applications(self):
        if not self.applications:
            print("No application found.")
            return
        
        for application in self.applications:
            print(application)
            print("-" * 40)
            
    def find_application(self, company):
        for application in self.applications:
            if application.company.lower() == company.lower():
                return application
        return None           
    
    def update_application(self, company, new_status):
        allowed_statuses = ["Saved", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"]
        
        formated_status = new_status.title()
        if formated_status not in allowed_statuses:
            print(f"Invalid status: {new_status}")
            print(f"Allowed statuses: {', '.join(allowed_statuses)}")
            return False
        
        application = self.find_application(company)
        if application is None:
            return False
          
        application.status = formated_status
        return True
    
    def save_applications(self, filename):
        application_data = [
            application.to_dict()
            for application in self.applications
        ]
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(application_data, file, indent=4)
    
    def load_applications(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                application_data = json.load(file)

            self.applications = []

            for data in application_data:
                application = JobApplication(
                    data["company"],
                    data["position"],
                    data["location"],
                    data["job_url"],
                    data["application_date"],
                    data["status"]
                )

            self.applications.append(application)

        except FileNotFoundError:
            self.applications = []
    
    
if __name__ == "__main__":

    application_one = JobApplication(
        "TechCorp", 
        "Software Engineer", 
        "New York", 
        "https://techcorp.com/jobs/1",
        "2026/09/01",
        "Applied"
        )

    application_two = JobApplication(
        "Dataworks", 
        "AI Engineer", 
        "New York", 
        "https://dataworks.com/jobs/1",
        "2026/09/02",
        "Applied"
        )

    tracker = ApplicationTracker()

    tracker.list_applications()

    tracker.add_applications(application_one)
    tracker.add_applications(application_two)

    applications = [application_one, application_two]

    tracker.list_applications()
        
    print(f"Total applications: {len(tracker.applications)}")

    print("\nSearching for TechCorp:")

    found_application = tracker.find_application("techcorp")

    if found_application:
        print("Application found:")
        print(found_application)
    else:
        print("Application not found.")
        
    print("\nUpdating application status for TechCorp:")
    update_successful = tracker.update_application("TechCorp", "Interview")
    if update_successful:
        print("Status updated successfully.")
        print(tracker.find_application("TechCorp"))
    else:
        print("Application not found. Status was not updated.")
        
        
    print("\nTrying to update an unknown company:")
    update_successful = tracker.update_application("UnknownCompany", "Rejected")
    if update_successful:
        print("Status updated successfully.")
    else:
        print("Application not found. Status was not updated.")
        
        
    print("\nTesting lowercase valid status:")
    update_successful = tracker.update_application("TechCorp", "offer")
    if update_successful:
        print("Status updated successfully.")
        print(tracker.find_application("TechCorp"))
    else:
        print("Status was not updated.")
        
    print("\nTesting invalid status:")
    update_successful = tracker.update_application("TechCorp", "Waiting")
    if update_successful:
        print("Status updated successfully.")
    else:
        print("Status was not updated.")
        
    print("\nApplication converted to dictionary:")
    print(application_one.to_dict())    
            
    tracker.save_applications("applications.json")
    print("\nApplications saved successfully.")

    loaded_tracker = ApplicationTracker()
    loaded_tracker.load_applications("applications.json")

    print("\nApplications loaded from JSON:")
    loaded_tracker.list_applications()
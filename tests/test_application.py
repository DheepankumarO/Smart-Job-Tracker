from src.application import JobApplication , ApplicationTracker

def test_add_applications():
    tracker = ApplicationTracker()
    
    application = JobApplication(
        "TechCorp",
        "Software Engineer",
        "Newyork",
        "https://techcorp.com/jobs/1",
        "2026-09-01",
        "Applied"
    )
    
    tracker.add_applications(application)
    
    assert len(tracker.applications) == 1
    assert tracker.applications[0] == application
    
def test_find_existing_application(): 
    tracker = ApplicationTracker()
    
    application = JobApplication(
        "TechCorp",
        "Software Engineer",
        "New York",
        "https://techcorp.com/jobs/1",
        "2026-09-01",
        "Applied"
    )
    
    tracker.add_applications(application)
    result = tracker.find_application("techcorp")
    assert result == application
    
def test_find_missing_application():  # test case for company does not exist
    tracker = ApplicationTracker()
    
    result = tracker.find_application("Unknown Company")
    assert result is None
    
def test_update_application_with_valid_status():  #Test a successful status update with lowercase normalization
    tracker = ApplicationTracker()

    application = JobApplication(
        "TechCorp",
        "Software Engineer",
        "New York",
        "https://techcorp.com/jobs/1",
        "2026-09-01",
        "Applied"
    )
    
    tracker.add_applications(application)
    result = tracker.update_application("TechCorp", "offer")
    
    assert result is True
    assert application.status == "Offer"
    
def test_update_application_with_invalid_status():
    tracker=ApplicationTracker()
    application = JobApplication(
        "TechCorp",
        "Software Engineer",
        "New York",
        "https://techcorp.com/jobs/1",
        "2026-09-01",
        "Applied"
    )
    tracker.add_applications(application)
    result = tracker.update_application("TechCorp", "Waiting")
    
    assert result is False
    assert application.status == "Applied"
    
def test_update_missin_application():
    tracker = ApplicationTracker()
    
    result = tracker.update_application("Unknown Company", "Interview")
    assert result is False

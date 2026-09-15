from application import JobApplication, ApplicationTracker


DATA_FILE = "applications.json"


def display_menu():
    print("\nSmart Job Tracker")
    print("1. Add application")
    print("2. List applications")
    print("3. Search application")
    print("4. Update application status")
    print("5. Exit")

def add_application_from_input(tracker):
    print("\nAdd a new application")

    company = input("Company: ").strip()
    position = input("Position: ").strip()
    location = input("Location: ").strip()
    job_url = input("Job URL: ").strip()
    application_date = input("Application date: ").strip()
    status = input("Status: ").strip()

    application = JobApplication(
        company,
        position,
        location,
        job_url,
        application_date,
        status
    )

    tracker.add_applications(application)
    tracker.save_applications(DATA_FILE)

    print("Application added successfully.")

def search_application_from_input(tracker):
    print("\nSearch for an application")

    company = input("Enter company name: ").strip()
    application = tracker.find_application(company)

    if application is None:
        print("Application not found.")
        return

    print("\nApplication found:")
    print(application)

def update_status_from_input(tracker):
    print("\nUpdate application status")

    company = input("Company: ").strip()
    new_status = input("New status: ").strip()

    update_successful = tracker.update_application(company, new_status)

    if update_successful:
        tracker.save_applications(DATA_FILE)
        print("Status updated successfully.")
    else:
        print("Status was not updated.")

def main():
    tracker = ApplicationTracker()
    tracker.load_applications(DATA_FILE)

    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_application_from_input(tracker)

        elif choice == "2":
            tracker.list_applications()

        elif choice == "3":
            search_application_from_input(tracker)

        elif choice == "4":
            update_status_from_input(tracker)

        elif choice == "5":
            tracker.save_applications(DATA_FILE)
            print("Applications saved. Goodbye!")
            break

        else:
            print("Invalid option. Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
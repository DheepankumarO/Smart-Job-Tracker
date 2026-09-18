from datetime import datetime
from application_repository import (
    create_application,
    find_applications_by_company,
    get_all_applications,
    update_application_status,
    delete_application,
)

ALLOWED_STATUSES = {
    "Saved",
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn"
}

def display_menu():
    print("\nSmart Job Tracker")
    print("1. Add application")
    print("2. List applications")
    print("3. Search applications")
    print("4. Update application status")
    print("5. Delete application")
    print("6. Exit")

def list_applications_from_database():  #database listing function
    applications = get_all_applications()

    if not applications:
        print("No applications found.")
        return

    for application in applications:
        print("-" * 40)
        print(f"ID: {application['id']}")
        print(f"Company: {application['company']}")
        print(f"Position: {application['position']}")
        print(f"Location: {application['location']}")
        print(f"Job URL: {application['job_url']}")
        print(
            f"Application Date: "
            f"{application['application_date']}"
        )
        print(f"Status: {application['status']}")
        print(f"Notes: {application['notes']}")

    print("-" * 40)

def add_application_from_input():
    print("\nAdd a new application")

    company = input("Company: ").strip()
    position = input("Position: ").strip()
    location = input("Location: ").strip()
    job_url = input("Job URL: ").strip()

    date_text = input(
        "Application date (YYYY-MM-DD): "
    ).strip()

    try:
        application_date = datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    status = input(
        "Status (Saved, Applied, Interview, Offer, "
        "Rejected, Withdrawn): "
        ).strip().title()

    if status not in ALLOWED_STATUSES:
        print("Invalid status.")
        print("Allowed statuses: " + ", ".join(sorted(ALLOWED_STATUSES)))
        return

    notes = input("Notes (optional): ").strip()
    created_application = create_application(
        company,
        position,
        location,
        job_url,
        application_date,
        status,
        notes or None
    )

    print(
        "Application created successfully "
        f"with ID {created_application['id']}."
    )

def search_application_from_input():
    company = input("Enter company name: ").strip()

    applications = find_applications_by_company(company)

    if not applications:
        print("Application not found.")
        return

    for application in applications:
        print("-" * 40)
        print(f"ID: {application['id']}")
        print(f"Company: {application['company']}")
        print(f"Position: {application['position']}")
        print(f"Location: {application['location']}")
        print(f"Job URL: {application['job_url']}")
        print(f"Status: {application['status']}")
        print(f"Notes: {application['notes']}")

    print("-" * 40)

def update_status_from_input():
    print("\nUpdate application status")

    application_id_text = input(
        "Application ID: "
    ).strip()

    try:
        application_id = int(application_id_text)
    except ValueError:
        print("Application ID must be a number.")
        return

    new_status = input(
        "New status: "
    ).strip().title()

    if new_status not in ALLOWED_STATUSES:
        print("Invalid status.")
        print(
            "Allowed statuses: "
            + ", ".join(sorted(ALLOWED_STATUSES))
        )
        return

    updated_application = update_application_status(
        application_id,
        new_status
    )

    if updated_application is None:
        print("Application not found.")
        return

    print("Status updated successfully.")
    print(
        f"{updated_application['company']}: "
        f"{updated_application['status']}"
    )

def delete_application_from_input():
    print("\nDelete application")

    application_id_text = input("Application ID: ").strip()

    try:
        application_id = int(application_id_text)
    except ValueError:
        print("Application ID must be a number.")
        return

    confirmation = input(
        f"Are you sure you want to delete application {application_id}? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion cancelled.")
        return

    deleted_application = delete_application(application_id)

    if deleted_application is None:
        print("Application not found.")
        return

    print("Application deleted successfully.")
    print(
        f"{deleted_application['company']} - "
        f"{deleted_application['position']}"
    )

def main():
    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_application_from_input()

        elif choice == "2":
            list_applications_from_database()

        elif choice == "3":
            search_application_from_input()

        elif choice == "4":
            update_status_from_input()

        elif choice == "5":
            delete_application_from_input()
        
        elif choice == "6":
            print("Applications saved. Goodbye!")
            break

        else:
            print("Invalid option. Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
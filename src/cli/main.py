import os
from src.service.customer_service import CustomerService
from src.service.vehicle_service import VehicleService
from src.service.rental_service import RentalService
from src.service.payment_service import PaymentService
from src.service.maintenance_service import MaintenanceService

print("👉 Loaded main from:", os.path.abspath(__file__))

# ---------------- CUSTOMER MENU ---------------- #
def customer_menu():
    customer_service = CustomerService()

    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Delete Customer")
        print("4. List Customers")
        print("5. Search Customer")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            license_no = input("Driver License: ")
            address = input("Address: ")
            print(customer_service.add_customer(name, email, phone, license_no, address))

        elif choice == "2":
            customer_id = input("Customer ID to update: ")
            name = input("New Name: ") or None
            email = input("New Email: ") or None
            phone = input("New Phone: ") or None
            address = input("New Address: ") or None
            print(customer_service.update_customer(customer_id, name, email, phone, address))

        elif choice == "3":
            cid = input("Customer ID to delete: ")
            print(customer_service.delete_customer(cid))

        elif choice == "4":
            for c in customer_service.list_customers():
                print(f"ID: {c['id']} | Name: {c['name']} | Email: {c['email']} | Phone: {c['phone']}")

        elif choice == "5":
            cid = input("Search by Customer ID: ")
            print(customer_service.search_customer(cid))

        elif choice == "6":
            break
        else:
            print("Invalid choice! Try again.")


# ---------------- VEHICLE MENU ---------------- #
def vehicle_menu():
    vehicle_service = VehicleService()

    while True:
        print("\n--- VEHICLE MENU ---")
        print("1. Add Vehicle")
        print("2. Update Vehicle")
        print("3. Delete Vehicle")
        print("4. List Vehicles")
        print("5. Search Vehicle")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            plate = input("Plate No: ")
            model = input("Model: ")
            vtype = input("Type: ")
            rate = float(input("Rate per Day: "))
            print(vehicle_service.add_vehicle(plate, model, vtype, rate))

        elif choice == "2":
            vid = input("Vehicle ID to update: ")
            model = input("New Model: ") or None
            vtype = input("New Type: ") or None
            rate = input("New Rate: ") or None
            available = input("Available (True/False): ") or None
            if available:
                available = available.lower() == "true"
            print(vehicle_service.update_vehicle(vid, model, vtype, rate, available))

        elif choice == "3":
            vid = input("Vehicle ID to delete: ")
            print(vehicle_service.delete_vehicle(vid))

        elif choice == "4":
            for v in vehicle_service.list_vehicles():
                print(f"ID: {v['id']} | Model: {v['model']} | Type: {v['type']} | Rate: {v['rate']} | Available: {v['available']}")

        elif choice == "5":
            vid = input("Search by Vehicle ID: ")
            print(vehicle_service.search_vehicle(vid))

        elif choice == "6":
            break
        else:
            print("Invalid choice! Try again.")


# ---------------- RENTAL MENU ---------------- #
def rental_menu():
    rental_service = RentalService()

    while True:
        print("\n--- RENTAL MENU ---")
        print("1. Add Rental")
        print("2. Update Rental")
        print("3. Delete Rental")
        print("4. List Rentals")
        print("5. Search Rental")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            vehicle_id = input("Vehicle ID: ")
            customer_id = input("Customer ID: ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            print(rental_service.add_rental(vehicle_id, customer_id, start_date, end_date))

        elif choice == "2":
            rid = input("Rental ID to update: ")
            start_date = input("New Start Date: ") or None
            end_date = input("New End Date: ") or None
            print(rental_service.update_rental(rid, start_date, end_date))

        elif choice == "3":
            rid = input("Rental ID to delete: ")
            print(rental_service.delete_rental(rid))

        elif choice == "4":
            for r in rental_service.list_rentals():
                print(f"ID: {r['id']} | Vehicle ID: {r['vehicle_id']} | Customer ID: {r['customer_id']} | Start: {r['start_date']} | End: {r['end_date']}")

        elif choice == "5":
            rid = input("Search by Rental ID: ")
            print(rental_service.search_rental(rid))

        elif choice == "6":
            break
        else:
            print("Invalid choice! Try again.")


# ---------------- PAYMENT MENU ---------------- #
def payment_menu():
    payment_service = PaymentService()

    while True:
        print("\n--- PAYMENT MENU ---")
        print("1. Add Payment")
        print("2. Update Payment")
        print("3. Delete Payment")
        print("4. List Payments")
        print("5. Search Payment")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            rental_id = input("Rental ID: ")
            customer_id = input("Customer ID: ")
            amount = float(input("Amount: "))
            payment_date = input("Payment Date (YYYY-MM-DD): ")
            payment_type = input("Payment Type (Cash/Card/UPI): ")
            print(payment_service.add_payment(rental_id, customer_id, amount, payment_date, payment_type))

        elif choice == "2":
            pid = input("Payment ID to update: ")
            amount = input("New Amount: ") or None
            payment_date = input("New Payment Date: ") or None
            payment_type = input("New Payment Type: ") or None
            print(payment_service.update_payment(pid, amount, payment_date, payment_type))

        elif choice == "3":
            pid = input("Payment ID to delete: ")
            print(payment_service.delete_payment(pid))

        elif choice == "4":
            for p in payment_service.list_payments():
                print(f"ID: {p['id']} | Rental: {p['rental_id']} | Customer: {p['customer_id']} | Amount: {p['amount']} | Type: {p['payment_type']} | Date: {p['payment_date']}")

        elif choice == "5":
            pid = input("Search by Payment ID: ")
            print(payment_service.search_payment(pid))

        elif choice == "6":
            break
        else:
            print("Invalid choice! Try again.")


# ---------------- MAINTENANCE MENU ---------------- #
def maintenance_menu():
    maintenance_service = MaintenanceService()

    while True:
        print("\n--- MAINTENANCE MENU ---")
        print("1. Add Maintenance Record")
        print("2. Update Maintenance")
        print("3. Delete Maintenance")
        print("4. List Maintenance Records")
        print("5. Search Maintenance Record")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            vid = input("Vehicle ID: ")
            desc = input("Description: ")
            cost = float(input("Cost: "))
            date = input("Date (YYYY-MM-DD): ")
            print(maintenance_service.add_maintenance(vid, desc, cost, date))

        elif choice == "2":
            mid = input("Maintenance ID to update: ")
            desc = input("New Description: ") or None
            cost = input("New Cost: ") or None
            date = input("New Date: ") or None
            print(maintenance_service.update_maintenance(mid, desc, cost, date))

        elif choice == "3":
            mid = input("Maintenance ID to delete: ")
            print(maintenance_service.delete_maintenance(mid))

        elif choice == "4":
            for m in maintenance_service.list_maintenance():
                print(f"ID: {m['id']} | Vehicle ID: {m['vehicle_id']} | Description: {m['description']} | Cost: {m['cost']} | Date: {m['date']}")

        elif choice == "5":
            mid = input("Search by Maintenance ID: ")
            print(maintenance_service.search_maintenance(mid))

        elif choice == "6":
            break
        else:
            print("Invalid choice! Try again.")


# ---------------- MAIN MENU ---------------- #
def main():
    while True:
        print("\n=== VEHICLE RENTAL MANAGEMENT SYSTEM ===")
        print("1. Manage Customers")
        print("2. Manage Vehicles")
        print("3. Manage Rentals")
        print("4. Manage Payments")
        print("5. Manage Maintenance")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            customer_menu()
        elif choice == "2":
            vehicle_menu()
        elif choice == "3":
            rental_menu()
        elif choice == "4":
            payment_menu()
        elif choice == "5":
            maintenance_menu()
        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()

from src.service.customer_service import CustomerService
from src.service.vehicle_service import VehicleService
from src.service.rental_service import RentalService
from src.service.payment_service import PaymentService
from src.service.maintenance_service import MaintenanceService

def main():
    customer_service = CustomerService()
    vehicle_service = VehicleService()
    rental_service = RentalService()
    payment_service = PaymentService()
    maintenance_service = MaintenanceService()

    while True:
        print("\n--- Vehicle Rental Management System ---")
        print("1. Customer Management")
        print("2. Vehicle Management")
        print("3. Rental Management")
        print("4. Payment Management")
        print("5. Maintenance Management")
        print("6. Exit")

        choice = input("Enter choice: ")

        # ---------------- CUSTOMER MENU ----------------
        if choice == "1":
            while True:
                print("\n--- Customer Menu ---")
                print("1. Add Customer")
                print("2. Update Customer")
                print("3. Delete Customer")
                print("4. List Customers")
                print("5. Search Customer")
                print("6. Back to Main Menu")
                c_choice = input("Enter choice: ")

                if c_choice == "1":
                    name = input("Name: ")
                    email = input("Email: ")
                    phone = input("Phone: ")
                    license_no = input("Driver License: ")
                    address = input("Address: ")
                    print(customer_service.add_customer(name, email, phone, license_no, address))

                elif c_choice == "2":
                    customer_id = input("Customer ID to update: ")
                    name = input("New Name (leave blank if no change): ") or None
                    email = input("New Email: ") or None
                    phone = input("New Phone: ") or None
                    address = input("New Address: ") or None
                    print(customer_service.update_customer(customer_id, name, email, phone, address))

                elif c_choice == "3":
                    customer_id = input("Customer ID to delete: ")
                    print(customer_service.delete_customer(customer_id))

                elif c_choice == "4":
                    customers = customer_service.list_customers()
                    for c in customers:
                        print(c)

                elif c_choice == "5":
                    keyword = input("Search keyword (name/email/license): ")
                    results = customer_service.search_customer(keyword)
                    for c in results:
                        print(c)

                elif c_choice == "6":
                    break
                else:
                    print("Invalid choice!")

        # ---------------- VEHICLE MENU ----------------
        elif choice == "2":
            while True:
                print("\n--- Vehicle Menu ---")
                print("1. Add Vehicle")
                print("2. Update Vehicle")
                print("3. Delete Vehicle")
                print("4. List Vehicles")
                print("5. Search Vehicle")
                print("6. Back to Main Menu")
                v_choice = input("Enter choice: ")

                if v_choice == "1":
                    plate = input("Plate Number: ")
                    model = input("Model: ")
                    vtype = input("Type (Car/Bike/Van): ")
                    rate = float(input("Rental Rate: "))
                    print(vehicle_service.add_vehicle(plate, model, vtype, rate))

                elif v_choice == "2":
                    vehicle_id = input("Vehicle ID to update: ")
                    model = input("New Model: ") or None
                    vtype = input("New Type: ") or None
                    rate_input = input("New Rental Rate: ")
                    rate = float(rate_input) if rate_input else None
                    availability = input("Availability (Available/Rented/Maintenance): ") or None
                    print(vehicle_service.update_vehicle(vehicle_id, model, vtype, rate, availability))

                elif v_choice == "3":
                    vehicle_id = input("Vehicle ID to delete: ")
                    print(vehicle_service.delete_vehicle(vehicle_id))

                elif v_choice == "4":
                    vehicles = vehicle_service.list_vehicles()
                    for v in vehicles:
                        print(v)

                elif v_choice == "5":
                    keyword = input("Enter model/type/plate to search: ")
                    results = vehicle_service.search_vehicle(keyword)
                    for v in results:
                        print(v)

                elif v_choice == "6":
                    break
                else:
                    print("Invalid choice!")

        # ---------------- RENTAL MENU ----------------
        elif choice == "3":
            while True:
                print("\n--- Rental Menu ---")
                print("1. Create Rental")
                print("2. End Rental")
                print("3. Delete Rental")
                print("4. List Rentals")
                print("5. Search Rentals")
                print("6. Back to Main Menu")
                r_choice = input("Enter choice: ")

                if r_choice == "1":
                    customer_id = input("Customer ID: ")
                    vehicle_id = input("Vehicle ID: ")
                    rental_date = input("Rental Date (YYYY-MM-DD): ")
                    return_date = input("Expected Return Date (YYYY-MM-DD): ")
                    print(rental_service.create_rental(customer_id, vehicle_id, rental_date, return_date))

                elif r_choice == "2":
                    rental_id = input("Rental ID to complete: ")
                    actual_return = input("Actual Return Date (YYYY-MM-DD): ")
                    print(rental_service.end_rental(rental_id, actual_return))

                elif r_choice == "3":
                    rental_id = input("Rental ID to delete: ")
                    print(rental_service.delete_rental(rental_id))

                elif r_choice == "4":
                    rentals = rental_service.list_rentals()
                    for r in rentals:
                        print(r)

                elif r_choice == "5":
                    keyword = input("Search Rentals (status/customer/vehicle): ")
                    results = rental_service.search_rentals(keyword)
                    for r in results:
                        print(r)

                elif r_choice == "6":
                    break
                else:
                    print("Invalid choice!")

        # ---------------- PAYMENT MENU ----------------
        elif choice == "4":
            while True:
                print("\n--- Payment Menu ---")
                print("1. Add Payment")
                print("2. Update Payment")
                print("3. Delete Payment")
                print("4. List Payments")
                print("5. Search Payments")
                print("6. Back to Main Menu")
                p_choice = input("Enter choice: ")

                if p_choice == "1":
                    rental_id = input("Rental ID: ")
                    customer_id = input("Customer ID: ")
                    amount = float(input("Amount: "))
                    payment_date = input("Payment Date (YYYY-MM-DD): ")
                    payment_type = input("Payment Type (Cash/Card/UPI/Online): ")
                    print(payment_service.add_payment(rental_id, customer_id, amount, payment_date, payment_type))

                elif p_choice == "2":
                    payment_id = input("Payment ID to update: ")
                    amount_input = input("New Amount: ")
                    amount = float(amount_input) if amount_input else None
                    payment_date = input("New Payment Date (YYYY-MM-DD): ") or None
                    payment_type = input("New Payment Type: ") or None
                    print(payment_service.update_payment(payment_id, amount, payment_date, payment_type))

                elif p_choice == "3":
                    payment_id = input("Payment ID to delete: ")
                    print(payment_service.delete_payment(payment_id))

                elif p_choice == "4":
                    payments = payment_service.list_payments()
                    for p in payments:
                        print(p)

                elif p_choice == "5":
                    keyword = input("Search Payments: ")
                    results = payment_service.search_payments(keyword)
                    for p in results:
                        print(p)

                elif p_choice == "6":
                    break
                else:
                    print("Invalid choice!")

        # ---------------- MAINTENANCE MENU ----------------
        elif choice == "5":
            while True:
                print("\n--- Maintenance Menu ---")
                print("1. Add Maintenance")
                print("2. Update Maintenance")
                print("3. Delete Maintenance")
                print("4. List Maintenance")
                print("5. Search Maintenance")
                print("6. Back to Main Menu")
                m_choice = input("Enter choice: ")

                if m_choice == "1":
                    vehicle_id = input("Vehicle ID: ")
                    description = input("Description: ")
                    maintenance_date = input("Date (YYYY-MM-DD): ")
                    status = input("Status (Pending/Completed): ")
                    print(maintenance_service.add_maintenance(vehicle_id, description, maintenance_date, status))

                elif m_choice == "2":
                    maintenance_id = input("Maintenance ID to update: ")
                    description = input("New Description: ") or None
                    maintenance_date = input("New Date (YYYY-MM-DD): ") or None
                    status = input("New Status: ") or None
                    print(maintenance_service.update_maintenance(maintenance_id, description, maintenance_date, status))

                elif m_choice == "3":
                    maintenance_id = input("Maintenance ID to delete: ")
                    print(maintenance_service.delete_maintenance(maintenance_id))

                elif m_choice == "4":
                    records = maintenance_service.list_maintenance()
                    for r in records:
                        print(r)

                elif m_choice == "5":
                    keyword = input("Search Maintenance (vehicle/description): ")
                    results = maintenance_service.search_maintenance(keyword)
                    for r in results:
                        print(r)

                elif m_choice == "6":
                    break
                else:
                    print("Invalid choice!")

        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

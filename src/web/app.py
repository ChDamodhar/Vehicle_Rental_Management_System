

import streamlit as st

from src.service.customer_service import CustomerService
from src.service.vehicle_service import VehicleService
from src.service.rental_service import RentalService
from src.service.payment_service import PaymentService
from src.service.maintenance_service import MaintenanceService

# Initialize services
customer_service = CustomerService()
vehicle_service = VehicleService()
rental_service = RentalService()
payment_service = PaymentService()
maintenance_service = MaintenanceService()

st.set_page_config(page_title="Vehicle Rental Management System", layout="wide")

st.title("🚗 Vehicle Rental Management System")
st.sidebar.title("📋 Navigation")

menu = st.sidebar.radio(
    "Go to:",
    ["Customers", "Vehicles", "Rentals", "Payments", "Maintenance"]
)

# ---------------- CUSTOMER MODULE ---------------- #
if menu == "Customers":
    st.header("👤 Customer Management")
    tab1, tab2, tab3 = st.tabs(["➕ Add Customer", "📄 View Customers", "🔍 Search Customer"])

    with tab1:
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        license_no = st.text_input("Driver License No.")
        address = st.text_area("Address")
        if st.button("Add Customer"):
            st.success(customer_service.add_customer(name, email, phone, license_no, address))

    with tab2:
        st.subheader("All Customers")
        customers = customer_service.list_customers()
        if isinstance(customers, str):
            st.warning(customers)
        else:
            st.dataframe(customers)

    with tab3:
        cid = st.text_input("Enter Customer ID")
        if st.button("Search"):
            result = customer_service.search_customer(cid)
            st.write(result)


# ---------------- VEHICLE MODULE ---------------- #
elif menu == "Vehicles":
    st.header("🚙 Vehicle Management")
    tab1, tab2, tab3 = st.tabs(["➕ Add Vehicle", "📄 View Vehicles", "🔍 Search Vehicle"])

    with tab1:
        plate = st.text_input("Vehicle Plate No.")
        model = st.text_input("Model")
        vtype = st.text_input("Type")
        rate = st.number_input("Rate per Day", min_value=0.0, step=100.0)
        if st.button("Add Vehicle"):
            st.success(vehicle_service.add_vehicle(plate, model, vtype, rate))

    with tab2:
        vehicles = vehicle_service.list_vehicles()
        if isinstance(vehicles, str):
            st.warning(vehicles)
        else:
            st.dataframe(vehicles)

    with tab3:
        vid = st.text_input("Enter Vehicle ID")
        if st.button("Search Vehicle"):
            result = vehicle_service.search_vehicle(vid)
            st.write(result)


# ---------------- RENTAL MODULE ---------------- #
elif menu == "Rentals":
    st.header("📅 Rental Management")
    tab1, tab2, tab3 = st.tabs(["➕ Add Rental", "📄 View Rentals", "🔍 Search Rental"])

    with tab1:
        vehicle_id = st.text_input("Vehicle ID")
        customer_id = st.text_input("Customer ID")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if st.button("Add Rental"):
            st.success(rental_service.add_rental(vehicle_id, customer_id, start_date, end_date))

    with tab2:
        rentals = rental_service.list_rentals()
        if isinstance(rentals, str):
            st.warning(rentals)
        else:
            st.dataframe(rentals)

    with tab3:
        rid = st.text_input("Rental ID")
        if st.button("Search Rental"):
            st.write(rental_service.search_rental(rid))


# ---------------- PAYMENT MODULE ---------------- #
elif menu == "Payments":
    st.header("💳 Payment Management")
    tab1, tab2, tab3 = st.tabs(["➕ Add Payment", "📄 View Payments", "🔍 Search Payment"])

    with tab1:
        rental_id = st.text_input("Rental ID")
        customer_id = st.text_input("Customer ID")
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        payment_date = st.date_input("Payment Date")
        payment_type = st.selectbox("Payment Type", ["Cash", "Card", "UPI"])
        if st.button("Add Payment"):
            st.success(payment_service.add_payment(rental_id, customer_id, amount, payment_date, payment_type))

    with tab2:
        payments = payment_service.list_payments()
        if isinstance(payments, str):
            st.warning(payments)
        else:
            st.dataframe(payments)

    with tab3:
        pid = st.text_input("Payment ID")
        if st.button("Search Payment"):
            st.write(payment_service.search_payment(pid))


# ---------------- MAINTENANCE MODULE ---------------- #
elif menu == "Maintenance":
    st.header("🧰 Maintenance Management")
    tab1, tab2, tab3 = st.tabs(["➕ Add Maintenance", "📄 View Records", "🔍 Search Maintenance"])

    with tab1:
        vid = st.text_input("Vehicle ID")
        desc = st.text_area("Description")
        cost = st.number_input("Cost", min_value=0.0, step=100.0)
        date = st.date_input("Date")
        if st.button("Add Maintenance Record"):
            st.success(maintenance_service.add_maintenance(vid, desc, cost, date))

    with tab2:
        maintenance = maintenance_service.list_maintenance()
        if isinstance(maintenance, str):
            st.warning(maintenance)
        else:
            st.dataframe(maintenance)

    with tab3:
        mid = st.text_input("Maintenance ID")
        if st.button("Search Maintenance Record"):
            st.write(maintenance_service.search_maintenance(mid))

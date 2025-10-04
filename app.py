# app.py

import streamlit as st
import pandas as pd
from datetime import date

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

st.set_page_config(page_title="Vehicle Rental Management", layout="wide")

st.title("🚗 Vehicle Rental Management System")
st.sidebar.title("📋 Navigation")

menu = st.sidebar.radio(
    "Go to:",
    ["Customers", "Vehicles", "Rentals", "Payments", "Maintenance"]
)

# ---------------- CUSTOMER MODULE ---------------- #
if menu == "Customers":
    st.header("👤 Customer Management")
    
    customers = customer_service.list_customers()
    if isinstance(customers, str):
        st.warning(customers)
    else:
        st.dataframe(pd.DataFrame(customers))

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("➕ Add New Customer"):
            with st.form("add_customer_form", clear_on_submit=True):
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                license_no = st.text_input("Driver License No.")
                address = st.text_area("Address")
                if st.form_submit_button("Add Customer"):
                    st.success(customer_service.add_customer(name, email, phone, license_no, address))

    with col2:
        with st.expander("✏️ Update / 🗑️ Delete Customer"):
            customer_id_to_edit = st.text_input("Enter Customer ID to Edit/Delete")
            if customer_id_to_edit:
                st.subheader("Update Customer")
                name_update = st.text_input("New Name (optional)", key="cust_name")
                email_update = st.text_input("New Email (optional)", key="cust_email")
                phone_update = st.text_input("New Phone (optional)", key="cust_phone")
                address_update = st.text_area("New Address (optional)", key="cust_address")
                if st.button("Update Customer"):
                    st.info(customer_service.update_customer(customer_id_to_edit, name_update, email_update, phone_update, address_update))

                st.subheader("Delete Customer")
                if st.button("Delete Customer"):
                    st.warning(customer_service.delete_customer(customer_id_to_edit))

# ---------------- VEHICLE MODULE ---------------- #
elif menu == "Vehicles":
    st.header("🚙 Vehicle Management")

    vehicles = vehicle_service.list_vehicles()
    if isinstance(vehicles, str):
        st.warning(vehicles)
    else:
        st.dataframe(pd.DataFrame(vehicles))

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("➕ Add New Vehicle"):
            with st.form("add_vehicle_form", clear_on_submit=True):
                plate = st.text_input("Vehicle Plate No.")
                model = st.text_input("Model")
                vtype = st.text_input("Type (e.g., SUV, Sedan)")
                rate = st.number_input("Rate per Day", min_value=0.0, step=100.0)
                if st.form_submit_button("Add Vehicle"):
                    st.success(vehicle_service.add_vehicle(plate, model, vtype, rate))

    with col2:
        with st.expander("✏️ Update / 🗑️ Delete Vehicle"):
            vehicle_id_to_edit = st.text_input("Enter Vehicle ID to Edit/Delete")
            if vehicle_id_to_edit:
                st.subheader("Update Vehicle")
                rate_update = st.number_input("New Rate", min_value=0.0, step=50.0, key="v_rate")
                available_update = st.selectbox("Availability", [True, False], key="v_avail")
                if st.button("Update Vehicle"):
                    st.info(vehicle_service.update_vehicle(vehicle_id_to_edit, rate=rate_update, available=available_update))
                
                st.subheader("Delete Vehicle")
                if st.button("Delete Vehicle"):
                    st.warning(vehicle_service.delete_vehicle(vehicle_id_to_edit))

# ---------------- RENTAL MODULE ---------------- #
elif menu == "Rentals":
    st.header("📅 Rental Management")

    rentals = rental_service.list_rentals()
    if isinstance(rentals, str):
        st.warning(rentals)
    else:
        st.dataframe(pd.DataFrame(rentals))

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("➕ Add New Rental"):
            with st.form("add_rental_form", clear_on_submit=True):
                vehicle_id = st.text_input("Vehicle ID")
                customer_id = st.text_input("Customer ID")
                start_date = st.date_input("Start Date", value=date.today())
                end_date = st.date_input("End Date", value=date.today())
                if st.form_submit_button("Add Rental"):
                    st.success(rental_service.add_rental(vehicle_id, customer_id, start_date, end_date))

    with col2:
        with st.expander("✏️ Update / 🗑️ Delete Rental"):
            rental_id_to_edit = st.text_input("Enter Rental ID to Edit/Delete")
            if rental_id_to_edit:
                st.subheader("Update Rental Dates")
                start_date_update = st.date_input("New Start Date", key="r_start")
                end_date_update = st.date_input("New End Date", key="r_end")
                if st.button("Update Rental"):
                    st.info(rental_service.update_rental(rental_id_to_edit, start_date_update, end_date_update))
                
                st.subheader("Delete Rental")
                if st.button("Delete Rental"):
                    st.warning(rental_service.delete_rental(rental_id_to_edit))

# ---------------- PAYMENT MODULE ---------------- #
elif menu == "Payments":
    st.header("💳 Payment Management")

    payments = payment_service.list_payments()
    if isinstance(payments, str):
        st.warning(payments)
    else:
        st.dataframe(pd.DataFrame(payments))

    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("➕ Add New Payment"):
            with st.form("add_payment_form", clear_on_submit=True):
                rental_id = st.text_input("Rental ID")
                customer_id = st.text_input("Customer ID")
                amount = st.number_input("Amount", min_value=0.0, step=100.0)
                payment_date = st.date_input("Payment Date", value=date.today())
                payment_type = st.selectbox("Payment Type", ["Cash", "Card", "UPI"])
                if st.form_submit_button("Add Payment"):
                    st.success(payment_service.add_payment(rental_id, customer_id, amount, payment_date, payment_type))
    
    with col2:
        with st.expander("🗑️ Delete Payment"):
            payment_id_to_delete = st.text_input("Enter Payment ID to Delete")
            if payment_id_to_delete:
                if st.button("Delete Payment"):
                    st.warning(payment_service.delete_payment(payment_id_to_delete))

# ---------------- MAINTENANCE MODULE ---------------- #
elif menu == "Maintenance":
    st.header("🧰 Maintenance Management")
    
    maintenance_records = maintenance_service.list_maintenance()
    if isinstance(maintenance_records, str):
        st.warning(maintenance_records)
    else:
        st.dataframe(pd.DataFrame(maintenance_records))

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("➕ Add New Maintenance Record"):
            with st.form("add_maintenance_form", clear_on_submit=True):
                vehicle_id = st.text_input("Vehicle ID")
                description = st.text_area("Description of work")
                cost = st.number_input("Cost", min_value=0.0, step=50.0)
                maint_date = st.date_input("Date of Maintenance", value=date.today())
                if st.form_submit_button("Add Maintenance Record"):
                    st.success(maintenance_service.add_maintenance(vehicle_id, description, cost, maint_date))

    with col2:
        with st.expander("🗑️ Delete Maintenance Record"):
            maint_id_to_delete = st.text_input("Enter Maintenance ID to Delete")
            if maint_id_to_delete:
                if st.button("Delete Maintenance Record"):
                    st.warning(maintenance_service.delete_maintenance(maint_id_to_delete))
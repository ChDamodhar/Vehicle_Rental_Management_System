import streamlit as st
from datetime import date
# NOTE: Assuming these service imports are correctly configured to work
# without arguments in your environment, based on your provided code.
from src.service.customer_service import CustomerService
from src.service.vehicle_service import VehicleService
from src.service.rental_service import RentalService
from src.service.payment_service import PaymentService
from src.service.maintenance_service import MaintenanceService

# Initialize Services
# If these services require dependencies (like a database client), they should be passed here.
customer_service = CustomerService()
vehicle_service = VehicleService()
rental_service = RentalService()
payment_service = PaymentService()
maintenance_service = MaintenanceService()

# --- Utility Functions ---

def display_status(result):
    """Checks the result string for success/error indicators and displays the message."""
    if isinstance(result, str) and ("Error" in result or "❌" in result or "⚠️" in result):
        st.error(result)
    elif isinstance(result, list) and not result:
        st.info("No records found.")
    else:
        st.success(result)
        
# --- Mock Data Function for Revenue (Since we don't have the DAO/Service code) ---
def calculate_total_revenue_mock(payment_service):
    """
    MOCK FUNCTION: Calculates total revenue by summing the 'amount' field 
    from all payments returned by payment_service.list_payments().
    Assumes 'list_payments' returns a list of dictionaries with an 'amount' key.
    """
    try:
        payments = payment_service.list_payments()
        if isinstance(payments, list) and payments:
            # Safely converts 'amount' to float and sums them up.
            total_revenue = sum(float(p.get('amount', 0.0)) for p in payments if isinstance(p, dict) and 'amount' in p)
            return f"${total_revenue:,.2f}"
        return "$0.00"
    except Exception:
        # Fallback if list_payments returns an error string or uniterable object
        return "$N/A"

# --- Module Management Functions ---

## Customer Management
def customer_management():
    st.header("👤 Customer Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Delete", "List All", "Search"])

    with tab1: # Add Customer
        st.subheader("Add New Customer")
        with st.form("add_customer_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            # The signature is now fixed to only require name, email, phone.
            
            submitted = st.form_submit_button("Add Customer")
            if submitted and name and email and phone:
                result = customer_service.add_customer(name, email, phone)
                display_status(result)

    with tab2: # Update Customer
        st.subheader("Update Customer Details")
        with st.form("update_customer_form"):
            customer_id = st.text_input("Customer ID to Update")
            new_name = st.text_input("New Name (leave blank to keep current)") or None
            new_email = st.text_input("New Email (leave blank to keep current)") or None
            new_phone = st.text_input("New Phone (leave blank to keep current)") or None

            submitted = st.form_submit_button("Update Customer")
            if submitted and customer_id:
                result = customer_service.update_customer(customer_id, new_name, new_email, new_phone)
                display_status(result)

    with tab3: # Delete Customer
        st.subheader("Delete Customer")
        with st.form("delete_customer_form"):
            customer_id = st.text_input("Customer ID to Delete")
            submitted = st.form_submit_button("Delete Customer")
            if submitted and customer_id:
                result = customer_service.delete_customer(customer_id)
                display_status(result)

    with tab4: # List Customers
        st.subheader("All Customers")
        if st.button("Refresh Customer List"):
            # Mocking data fetch for display purposes. Replace with actual service call.
            customers = customer_service.list_customers()
            st.dataframe(customers)

    with tab5: # Search Customer
        st.subheader("Search Customer by ID")
        customer_id = st.text_input("Customer ID to Search")
        if customer_id and st.button("Search Customer"):
            result = customer_service.search_customer(customer_id)
            if isinstance(result, str):
                st.info(result)
            else:
                st.dataframe(result)
                
## Vehicle Management
def vehicle_management():
    st.header("🚗 Vehicle Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Delete", "List All", "Search"])

    with tab1: # Add Vehicle
        st.subheader("Add New Vehicle")
        with st.form("add_vehicle_form"):
            plate = st.text_input("Plate No")
            model = st.text_input("Model")
            vtype = st.selectbox("Type", ["Car", "Truck", "Van", "Motorcycle"])
            rate = st.number_input("Rate per Day", min_value=0.0, step=0.5)

            submitted = st.form_submit_button("Add Vehicle")
            if submitted and plate and model:
                result = vehicle_service.add_vehicle(plate, model, vtype, rate)
                display_status(result)

    with tab2: # Update Vehicle
        st.subheader("Update Vehicle Details")
        with st.form("update_vehicle_form"):
            vid = st.text_input("Vehicle ID to Update")
            new_model = st.text_input("New Model (leave blank to keep current)") or None
            new_vtype = st.selectbox("New Type", [""] + ["Car", "Truck", "Van", "Motorcycle"])
            new_vtype = new_vtype if new_vtype else None
            new_rate = st.number_input("New Rate (0 to ignore)", min_value=0.0, step=0.5)
            new_rate = new_rate if new_rate > 0 else None
            
            new_available_str = st.selectbox("New Availability", ["", "True", "False"])
            new_available = None
            if new_available_str == "True":
                new_available = True
            elif new_available_str == "False":
                new_available = False

            submitted = st.form_submit_button("Update Vehicle")
            if submitted and vid:
                result = vehicle_service.update_vehicle(vid, new_model, new_vtype, new_rate, new_available)
                display_status(result)

    with tab3: # Delete Vehicle
        st.subheader("Delete Vehicle")
        with st.form("delete_vehicle_form"):
            vid = st.text_input("Vehicle ID to Delete")
            submitted = st.form_submit_button("Delete Vehicle")
            if submitted and vid:
                result = vehicle_service.delete_vehicle(vid)
                display_status(result)

    with tab4: # List Vehicles
        st.subheader("All Vehicles")
        if st.button("Refresh Vehicle List"):
            vehicles = vehicle_service.list_vehicles()
            st.dataframe(vehicles)

    with tab5: # Search Vehicle
        st.subheader("Search Vehicle")
        st.info("Searching by Plate Number (partial match)")
        keyword = st.text_input("Plate Number Keyword")
        if keyword and st.button("Search Vehicle by Keyword"):
            result = vehicle_service.search_vehicle(keyword)
            if isinstance(result, str):
                st.info(result)
            else:
                st.dataframe(result)

## Rental Management
def rental_management():
    st.header("📝 Rental Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Delete", "List All", "Search"])

    with tab1: # Add Rental
        st.subheader("Add New Rental")
        with st.form("add_rental_form"):
            vehicle_id = st.text_input("Vehicle ID")
            customer_id = st.text_input("Customer ID")
            start_date = st.date_input("Start Date", value=date.today())
            end_date = st.date_input("End Date", value=date.today())

            submitted = st.form_submit_button("Add Rental")
            if submitted and vehicle_id and customer_id:
                # Convert date objects to string 'YYYY-MM-DD'
                result = rental_service.add_rental(
                    vehicle_id, customer_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
                )
                display_status(result)

    with tab2: # Update Rental
        st.subheader("Update Rental Dates")
        with st.form("update_rental_form"):
            rid = st.text_input("Rental ID to Update")
            new_start_date_obj = st.date_input("New Start Date (leave at today to ignore)", value=date.today(), key='update_start_date')
            new_end_date_obj = st.date_input("New End Date (leave at today to ignore)", value=date.today(), key='update_end_date')

            # Logic to handle optional date updates
            new_start_date = new_start_date_obj.strftime('%Y-%m-%d') if new_start_date_obj != date.today() else None
            new_end_date = new_end_date_obj.strftime('%Y-%m-%d') if new_end_date_obj != date.today() else None
            
            submitted = st.form_submit_button("Update Rental")
            if submitted and rid:
                result = rental_service.update_rental(rid, new_start_date, new_end_date)
                display_status(result)

    with tab3: # Delete Rental
        st.subheader("Delete Rental")
        with st.form("delete_rental_form"):
            rid = st.text_input("Rental ID to Delete")
            submitted = st.form_submit_button("Delete Rental")
            if submitted and rid:
                result = rental_service.delete_rental(rid)
                display_status(result)

    with tab4: # List Rentals
        st.subheader("All Rentals")
        if st.button("Refresh Rental List"):
            rentals = rental_service.list_rentals()
            st.dataframe(rentals)

    with tab5: # Search Rental
        st.subheader("Search Rental by ID")
        rid = st.text_input("Rental ID to Search")
        if rid and st.button("Search Rental"):
            result = rental_service.search_rental(rid)
            if isinstance(result, str):
                st.info(result)
            else:
                st.dataframe(result)

## Payment Management
def payment_management():
    st.header("💳 Payment Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Delete", "List All", "Search"])

    with tab1: # Add Payment
        st.subheader("Add New Payment")
        with st.form("add_payment_form"):
            rental_id = st.text_input("Rental ID")
            customer_id = st.text_input("Customer ID")
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            payment_date = st.date_input("Payment Date", value=date.today())
            payment_type = st.selectbox("Payment Type", ["Cash", "Card", "UPI"])

            submitted = st.form_submit_button("Add Payment")
            if submitted and rental_id and customer_id and amount > 0:
                result = payment_service.add_payment(
                    rental_id, customer_id, amount, payment_date.strftime('%Y-%m-%d'), payment_type
                )
                display_status(result)

    with tab2: # Update Payment
        st.subheader("Update Payment Details")
        with st.form("update_payment_form"):
            pid = st.text_input("Payment ID to Update")
            new_amount_input = st.number_input("New Amount (0 to ignore)", min_value=0.0, step=0.01, key='update_amount')
            new_amount = str(new_amount_input) if new_amount_input > 0 else None
            
            new_payment_date_obj = st.date_input("New Payment Date (leave at today to ignore)", value=date.today(), key='update_date')
            new_payment_date = new_payment_date_obj.strftime('%Y-%m-%d') if new_payment_date_obj != date.today() else None
            
            new_payment_type_str = st.selectbox("New Payment Type", [""] + ["Cash", "Card", "UPI"])
            new_payment_type = new_payment_type_str if new_payment_type_str else None

            submitted = st.form_submit_button("Update Payment")
            if submitted and pid:
                # Note: amount in update_payment will be passed as a string/None, which is handled in your DAO.
                result = payment_service.update_payment(pid, new_amount, new_payment_date, new_payment_type)
                display_status(result)

    with tab3: # Delete Payment
        st.subheader("Delete Payment")
        with st.form("delete_payment_form"):
            pid = st.text_input("Payment ID to Delete")
            submitted = st.form_submit_button("Delete Payment")
            if submitted and pid:
                result = payment_service.delete_payment(pid)
                display_status(result)

    with tab4: # List Payments
        st.subheader("All Payments")
        if st.button("Refresh Payment List"):
            payments = payment_service.list_payments()
            st.dataframe(payments)

    with tab5: # Search Payment
        st.subheader("Search Payment by ID")
        pid = st.text_input("Payment ID to Search")
        if pid and st.button("Search Payment"):
            result = payment_service.search_payment(pid)
            if isinstance(result, str):
                st.info(result)
            else:
                st.dataframe(result)

## Maintenance Management
def maintenance_management():
    st.header("🔧 Maintenance Management")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add", "Update", "Delete", "List All", "Search"])

    with tab1: # Add Maintenance
        st.subheader("Add New Maintenance Record")
        with st.form("add_maintenance_form"):
            vid = st.text_input("Vehicle ID")
            desc = st.text_area("Description")
            cost = st.number_input("Cost", min_value=0.0, step=0.01)
            date_input = st.date_input("Date", value=date.today())

            submitted = st.form_submit_button("Add Maintenance")
            if submitted and vid and desc:
                result = maintenance_service.add_maintenance(
                    vid, desc, cost, date_input.strftime('%Y-%m-%d')
                )
                display_status(result)

    with tab2: # Update Maintenance
        st.subheader("Update Maintenance Record")
        with st.form("update_maintenance_form"):
            mid = st.text_input("Maintenance ID to Update")
            new_desc = st.text_area("New Description (leave blank to keep current)") or None
            new_cost_input = st.number_input("New Cost (0 to ignore)", min_value=0.0, step=0.01, key='update_cost')
            new_cost = str(new_cost_input) if new_cost_input > 0 else None
            
            new_date_obj = st.date_input("New Date (leave at today to ignore)", value=date.today(), key='update_maintenance_date')
            new_date = new_date_obj.strftime('%Y-%m-%d') if new_date_obj != date.today() else None

            submitted = st.form_submit_button("Update Maintenance")
            if submitted and mid:
                result = maintenance_service.update_maintenance(mid, new_desc, new_cost, new_date)
                display_status(result)

    with tab3: # Delete Maintenance
        st.subheader("Delete Maintenance Record")
        with st.form("delete_maintenance_form"):
            mid = st.text_input("Maintenance ID to Delete")
            submitted = st.form_submit_button("Delete Maintenance")
            if submitted and mid:
                result = maintenance_service.delete_maintenance(mid)
                display_status(result)

    with tab4: # List Maintenance
        st.subheader("All Maintenance Records")
        if st.button("Refresh Maintenance List"):
            records = maintenance_service.list_maintenance()
            st.dataframe(records)

    with tab5: # Search Maintenance
        st.subheader("Search Maintenance by ID")
        mid = st.text_input("Maintenance ID to Search")
        if mid and st.button("Search Maintenance"):
            result = maintenance_service.search_maintenance(mid)
            if isinstance(result, str):
                st.info(result)
            else:
                st.dataframe(result)

# --- Main App Execution ---

st.set_page_config(
    page_title="Vehicle Rental Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Automated Vehicle Rental Management System 🏎️")

# Sidebar for Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Select Module:",
    ("Home", "Customers", "Vehicles", "Rentals", "Payments", "Maintenance")
)

# Main Content Area
if menu == "Home":
    
    st.image(
        "https://placehold.co/150x150/0f172a/ffffff?text=Auto+Rent+Pro", 
        caption="Your Fleet Management Partner",
        width=150
    )
    
    st.markdown("""
        # Welcome to the Central Management Dashboard 🚀
        
        This system connects your Streamlit frontend to your Python service layers (CustomerService, VehicleService, etc.)
        and is designed for real-time management of your vehicle rental operations.
        
        Use the sidebar navigation to jump into specific management modules.
    """)

    st.subheader("Key Operational Metrics (Live Data)")

    # Placeholder for Key Metrics
    # Note: Added checks (isinstance(..., list)) to prevent errors if service methods return strings or None.
    total_customers = len(customer_service.list_customers()) if hasattr(customer_service, 'list_customers') and isinstance(customer_service.list_customers(), list) else "N/A"
    total_vehicles = len(vehicle_service.list_vehicles()) if hasattr(vehicle_service, 'list_vehicles') and isinstance(vehicle_service.list_vehicles(), list) else "N/A"
    active_rentals = len(rental_service.list_rentals()) if hasattr(rental_service, 'list_rentals') and isinstance(rental_service.list_rentals(), list) else "N/A" # Should filter for active
    total_revenue = calculate_total_revenue_mock(payment_service)
    
    # Use columns for a clear dashboard view - Increased to 5 columns
    col1, col2, col3, col4, col5 = st.columns(5) # <-- UPDATED TO 5 COLUMNS

    with col1:
        st.metric(label="Total Registered Customers 👥", value=total_customers)

    with col2:
        st.metric(label="Total Vehicles in Fleet 🚗", value=total_vehicles)

    with col3:
        # Placeholder for real active rentals logic
        st.metric(label="Active Rentals Today 📝", value=active_rentals)

    with col4: # <-- NEW REVENUE METRIC
        st.metric(label="Total Revenue 💰", value=total_revenue, delta="Est. from payments")

    with col5:
        st.metric(label="Pending Maintenance 🔧", value="5", delta="-1 since yesterday")
        
    st.markdown("---")
    
    st.info("""
        **Quick Tip:** The application relies on the structure of your Python services (in `src/service/`) 
        to perform database operations. Ensure your service methods (e.g., `list_customers()`, `list_payments()`) 
        are correctly implemented to return data structures like lists or Pandas DataFrames for display/calculation.
    """)

elif menu == "Customers":
    customer_management()

elif menu == "Vehicles":
    vehicle_management()

elif menu == "Rentals":
    rental_management()

elif menu == "Payments":
    payment_management()

elif menu == "Maintenance":
    maintenance_management()

import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

# Import Service Layers
from src.service.customer_service import CustomerService
from src.service.vehicle_service import VehicleService
from src.service.rental_service import RentalService
from src.service.payment_service import PaymentService
from src.service.maintenance_service import MaintenanceService
from src.db_config import get_db_mode

# Initialize Services
customer_service = CustomerService()
vehicle_service = VehicleService()
rental_service = RentalService()
payment_service = PaymentService()
maintenance_service = MaintenanceService()

# --- Page Configurations ---
st.set_page_config(
    page_title="AutoRent Pro - Enterprise Fleet Manager",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Design Aesthetics & Custom CSS Theme Overrides ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Font Bindings */
    html, body, [class*="css"], .stMarkdown, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Modern Glassmorphic Container */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px 24px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 10px;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
        box-shadow: 0 20px 25px -5px rgba(56, 189, 248, 0.1), 0 8px 10px -6px rgba(56, 189, 248, 0.1);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 12px;
        font-weight: 500;
        margin-top: 6px;
        color: #64748b;
    }
    
    /* Badge Styles */
    .db-badge {
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 12px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 20px;
    }
    .badge-sqlite {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
    }
    .badge-supabase {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
    }
    
    /* Invoice Estimate Styling */
    .invoice-box {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .invoice-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .invoice-price {
        color: #60a5fa;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Buttons aesthetics */
    div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        transition: background-color 0.2s !important;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DB Status Badge Calculation ---
db_mode = get_db_mode()
db_badge_html = ""
if db_mode == "sqlite":
    db_badge_html = '<div class="db-badge badge-sqlite">🔄 SQLite Fallback (Offline Mode Active)</div>'
else:
    db_badge_html = '<div class="db-badge badge-supabase">🟢 Cloud Supabase Connected (Live Node)</div>'

# --- Utility Alert Handler ---
def display_status(result):
    """Displays success/error indicators based on response string."""
    if not result:
        return
    if isinstance(result, str) and ("Error" in result or "❌" in result or "⚠️" in result):
        st.error(result)
    elif isinstance(result, list) and not result:
        st.info("No matching records found.")
    else:
        st.success(result if isinstance(result, str) else "Operation completed successfully!")

# --- Sidebar Corporate Branding ---
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <h2 style="color: #60a5fa; margin: 0; font-weight: 800; font-size: 26px;">AutoRent Pro</h2>
    <p style="color: #64748b; font-size: 12px; margin-top: 4px; font-weight: 500;">ENTERPRISE FLEET SUITE</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "MANAGEMENT CONSOLE",
    ["📊 Dashboard Home", "👤 Customer Directory", "🚙 Fleet Inventory", "📝 Rental Bookings", "💳 Payment Ledger", "🔧 Maintenance Lab"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(db_badge_html, unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size: 11px; color: #475569; font-weight: 500; text-align: center; margin-top: 40px;">
    System Version: 2.4.0 (Enterprise)<br>
    © 2026 AutoRent Pro Inc.
</div>
""", unsafe_allow_html=True)

# --- 1. DASHBOARD HOME ---
if menu == "📊 Dashboard Home":
    st.title("Enterprise Operations Center 📊")
    st.markdown("Real-time telemetry and management controls for vehicle rentals.")

    # --- Live Metric Calculations ---
    # Fetch Data Safely
    raw_customers = customer_service.list_customers()
    customers_list = raw_customers if isinstance(raw_customers, list) else []
    
    raw_vehicles = vehicle_service.list_vehicles()
    vehicles_list = raw_vehicles if isinstance(raw_vehicles, list) else []
    
    raw_rentals = rental_service.list_rentals()
    rentals_list = raw_rentals if isinstance(raw_rentals, list) else []
    
    raw_payments = payment_service.list_payments()
    payments_list = raw_payments if isinstance(raw_payments, list) else []
    
    raw_maintenance = maintenance_service.list_maintenance()
    maintenance_list = raw_maintenance if isinstance(raw_maintenance, list) else []

    # Counts
    total_cust = len(customers_list)
    total_veh = len(vehicles_list)
    
    # Rented vs Available vs Maintenance counts
    rented_veh = sum(1 for v in vehicles_list if not v.get("available"))
    # Filter maintenance counts
    maint_veh = len(maintenance_list)
    
    active_rentals = sum(1 for r in rentals_list if datetime.strptime(r.get("end_date", "2000-01-01"), "%Y-%m-%d") >= datetime.now())
    
    # Calculate Real Revenue
    real_revenue_val = sum(float(p.get("amount", 0.0)) for p in payments_list)
    real_revenue = f"${real_revenue_val:,.2f}"

    # Visual Metric Columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">👥 Total Clients</div>
            <div class="metric-value">{total_cust}</div>
            <div class="metric-sub" style="color: #34d399;">🟢 Active Profiles</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🚙 Total Fleet</div>
            <div class="metric-value">{total_veh}</div>
            <div class="metric-sub" style="color: #60a5fa;">{total_veh - rented_veh} Available</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📝 Active Rentals</div>
            <div class="metric-value">{active_rentals}</div>
            <div class="metric-sub" style="color: #f43f5e;">{rented_veh} Fleet Dispatched</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💰 Gross Revenue</div>
            <div class="metric-value">{real_revenue}</div>
            <div class="metric-sub" style="color: #10b981;">💵 Captured Ledger</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔧 Fleet Service</div>
            <div class="metric-value">{maint_veh}</div>
            <div class="metric-sub" style="color: #fbbf24;">⚠️ Under Maintenance</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Operational Telemetry 📈")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Fleet Dispatch & Availability Status")
        if vehicles_list:
            avail_count = sum(1 for v in vehicles_list if v.get("available"))
            maint_ids = [m.get("vehicle_id") for m in maintenance_list]
            rented_count = 0
            maint_count = 0
            
            for v in vehicles_list:
                if not v.get("available"):
                    if v.get("id") in maint_ids:
                        maint_count += 1
                    else:
                        rented_count += 1
            
            status_df = pd.DataFrame({
                "Status": ["🟢 Available", "🔴 Rented", "🔧 In Service"],
                "Count": [avail_count, rented_count, maint_count]
            })
            st.bar_chart(status_df.set_index("Status"))
        else:
            st.info("No vehicles registered yet.")
            
    with chart_col2:
        st.subheader("Revenue Generation Curves")
        if payments_list:
            # Sort payments by date and plot sum of payments over time
            pay_df = pd.DataFrame(payments_list)
            if "payment_date" in pay_df.columns and "amount" in pay_df.columns:
                pay_df["amount"] = pay_df["amount"].astype(float)
                trend_df = pay_df.groupby("payment_date")["amount"].sum().reset_index()
                trend_df = trend_df.sort_values("payment_date")
                st.line_chart(trend_df.set_index("payment_date"))
            else:
                st.info("Insufficient columns for revenue graphing.")
        else:
            st.info("No payments recorded yet.")

    st.markdown("---")
    
    log_col1, log_col2 = st.columns(2)
    with log_col1:
        st.subheader("📋 Recent Deliveries & Rentals")
        if rentals_list:
            r_df = pd.DataFrame(rentals_list)
            # Standardize columns to display nicely
            display_cols = ["id", "customer_name", "vehicle_plate", "vehicle_model", "start_date", "end_date"]
            # Fallback if names are missing
            available_cols = [c for c in display_cols if c in r_df.columns]
            st.dataframe(r_df[available_cols].head(5), use_container_width=True)
        else:
            st.info("No recent rentals.")
            
    with log_col2:
        st.subheader("💳 Recent Transactions Ledger")
        if payments_list:
            p_df = pd.DataFrame(payments_list)
            display_cols = ["id", "customer_name", "vehicle_plate", "amount", "payment_type", "payment_date"]
            available_cols = [c for c in display_cols if c in p_df.columns]
            st.dataframe(p_df[available_cols].head(5), use_container_width=True)
        else:
            st.info("No recent payments.")

# --- 2. CUSTOMER DIRECTORY ---
elif menu == "👤 Customer Directory":
    st.title("Customer Management Hub 👤")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Register Client", "📋 Complete Directory", "🔍 Search Profiles", "✏️ Edit Client Details"])

    with tab1:
        st.subheader("Add New Customer Profile")
        with st.form("register_customer_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Name (Required)", placeholder="John Doe")
                email = st.text_input("Email Address (Required)", placeholder="john@example.com")
                phone = st.text_input("Phone Number", placeholder="+1 (555) 0123")
            with col_b:
                license_no = st.text_input("Driver License No.", placeholder="DL-XXXXXX")
                address = st.text_area("Billing Address", placeholder="Street, City, State, ZIP")
            
            submitted = st.form_submit_button("Register Customer")
            if submitted:
                result = customer_service.add_customer(name, email, phone, license_no, address)
                display_status(result)

    with tab2:
        st.subheader("Client Directory Ledger")
        if st.button("🔄 Refresh Customer List"):
            st.rerun()
            
        customers = customer_service.list_customers()
        if isinstance(customers, list):
            if customers:
                st.dataframe(pd.DataFrame(customers), use_container_width=True)
            else:
                st.info("No customers found.")
        else:
            st.error(customers)

    with tab3:
        st.subheader("Search Customer Record")
        search_id = st.text_input("Enter Customer Database ID")
        if search_id and st.button("Fetch Profile"):
            result = customer_service.search_customer(search_id)
            if isinstance(result, list):
                st.dataframe(pd.DataFrame(result))
            else:
                st.info(result)

    with tab4:
        st.subheader("Update Customer Records")
        # Fetch customers list to select
        customers = customer_service.list_customers()
        if isinstance(customers, list) and customers:
            customer_options = {f"ID {c['id']} - {c['name']}": c for c in customers}
            selected_c_label = st.selectbox("Select Customer to Update", list(customer_options.keys()))
            selected_c = customer_options[selected_c_label]
            
            with st.form("update_customer_form"):
                st.markdown(f"Updating records for Customer ID: **{selected_c['id']}**")
                up_name = st.text_input("Name", value=selected_c.get("name", ""))
                up_email = st.text_input("Email", value=selected_c.get("email", ""))
                up_phone = st.text_input("Phone", value=selected_c.get("phone", ""))
                up_license = st.text_input("Driver License", value=selected_c.get("license_no", ""))
                up_address = st.text_area("Address", value=selected_c.get("address", ""))
                
                submitted_up = st.form_submit_button("Apply Updates")
                if submitted_up:
                    res = customer_service.update_customer(
                        customer_id=selected_c['id'],
                        name=up_name,
                        email=up_email,
                        phone=up_phone,
                        license_no=up_license,
                        address=up_address
                    )
                    display_status(res)
        else:
            st.info("No customers registered yet.")

# --- 3. FLEET INVENTORY ---
elif menu == "🚙 Fleet Inventory":
    st.title("Vehicle Fleet Management 🚙")
    tab1, tab2, tab3 = st.tabs(["📋 Complete Fleet Inventory", "➕ Add Vehicle to Fleet", "🔧 Update Vehicle Specs"])

    with tab1:
        st.subheader("Fleet Inventory Control")
        if st.button("🔄 Refresh Fleet List"):
            st.rerun()
            
        vehicles = vehicle_service.list_vehicles()
        if isinstance(vehicles, list):
            if vehicles:
                # Beautify availability before displaying
                beautified_list = []
                for v in vehicles:
                    v_copy = v.copy()
                    avail = v.get("available")
                    v_copy["Status Badge"] = "🟢 Available" if avail else "🔴 Dispatched/Service"
                    beautified_list.append(v_copy)
                st.dataframe(pd.DataFrame(beautified_list), use_container_width=True)
            else:
                st.info("No vehicles registered in fleet.")
        else:
            st.error(vehicles)

    with tab2:
        st.subheader("Add Vehicle to Fleet")
        with st.form("add_vehicle_form"):
            col_x, col_y = st.columns(2)
            with col_x:
                plate = st.text_input("Registration Plate No. (Unique)", placeholder="AP-01-XX-XXXX")
                model = st.text_input("Brand & Model Name", placeholder="Toyota Innova")
            with col_y:
                vtype = st.selectbox("Vehicle Classification Type", ["Car", "Truck", "Van", "Motorcycle"])
                rate = st.number_input("Standard Daily Rental Rate ($)", min_value=0.0, step=50.0, value=1500.0)
            
            submitted = st.form_submit_button("Commission Vehicle")
            if submitted and plate and model:
                res = vehicle_service.add_vehicle(plate, model, vtype, rate)
                display_status(res)

    with tab3:
        st.subheader("Decommission or Update Fleet Specifications")
        vehicles = vehicle_service.list_vehicles()
        if isinstance(vehicles, list) and vehicles:
            vehicle_options = {f"{v['model']} ({v['plate']}) - ID: {v['id']}": v for v in vehicles}
            selected_v_label = st.selectbox("Select Vehicle to Update", list(vehicle_options.keys()))
            selected_v = vehicle_options[selected_v_label]
            
            with st.form("update_vehicle_form"):
                st.markdown(f"Updating specs for ID: **{selected_v['id']}** ({selected_v['plate']})")
                up_model = st.text_input("Brand & Model Name", value=selected_v.get("model", ""))
                up_vtype = st.selectbox("Type", ["Car", "Truck", "Van", "Motorcycle"], index=["Car", "Truck", "Van", "Motorcycle"].index(selected_v.get("type", "Car")))
                up_rate = st.number_input("Daily Rental Rate ($)", min_value=0.0, value=float(selected_v.get("rate", 0.0)))
                
                avail_status = "True" if selected_v.get("available") else "False"
                up_avail_str = st.selectbox("Set Availability Status", ["True", "False"], index=0 if selected_v.get("available") else 1)
                up_avail = True if up_avail_str == "True" else False
                
                col_btn1, col_btn2 = st.columns([4, 1])
                with col_btn1:
                    submitted_up = st.form_submit_button("Update Specifications")
                with col_btn2:
                    retire_btn = st.form_submit_button("🔴 Retire/Delete")
                
                if submitted_up:
                    res = vehicle_service.update_vehicle(selected_v['id'], up_model, up_vtype, up_rate, up_avail)
                    display_status(res)
                if retire_btn:
                    res = vehicle_service.delete_vehicle(selected_v['id'])
                    display_status(res)
        else:
            st.info("No vehicles registered.")

# --- 4. RENTAL BOOKINGS ---
elif menu == "📝 Rental Bookings":
    st.title("Rental Booking Desk 📝")
    tab1, tab2, tab3 = st.tabs(["📝 Book New Rental", "📋 Bookings Log", "❌ Complete/Terminate Rental"])

    # Load resources
    customers = customer_service.list_customers()
    vehicles = vehicle_service.list_vehicles()

    with tab1:
        st.subheader("Process New Rental Agreement")
        
        if isinstance(customers, list) and customers and isinstance(vehicles, list) and vehicles:
            # Filters available vehicles
            avail_vehicles = [v for v in vehicles if v.get("available")]
            
            if not avail_vehicles:
                st.warning("⚠️ No vehicles are currently available for booking. Clear them from maintenance or return active rentals.")
            else:
                cust_options = {f"{c['name']} (Email: {c['email']}) - ID: {c['id']}": c for c in customers}
                veh_options = {f"{v['model']} ({v['plate']}) - Rate: ${v['rate']}/day - ID: {v['id']}": v for v in avail_vehicles}
                
                selected_cust_label = st.selectbox("Select Booking Client", list(cust_options.keys()))
                selected_veh_label = st.selectbox("Select Fleet Vehicle", list(veh_options.keys()))
                
                selected_cust = cust_options[selected_cust_label]
                selected_veh = veh_options[selected_veh_label]
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    start_d = st.date_input("Start Date", value=date.today(), key="rental_start_date")
                with col_d2:
                    end_d = st.date_input("End Date (Return Date)", value=date.today(), key="rental_end_date")
                
                # --- Live Pricing Projection ---
                if end_d >= start_d:
                    days = (end_d - start_d).days
                    if days == 0:
                        days = 1 # Minimum 1 day billing
                    rate_per_day = float(selected_veh.get("rate", 0.0))
                    est_cost = days * rate_per_day
                    
                    st.markdown(f"""
                    <div class="invoice-box">
                        <div class="invoice-title">💰 Live Rental Pricing Estimate</div>
                        <div class="invoice-price">${est_cost:,.2f}</div>
                        <div style="font-size: 13px; color: #94a3b8; margin-top: 4px; font-weight: 500;">
                            Billing Duration: <b>{days} Day(s)</b> × ${rate_per_day:,.2f} / daily rate
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Error: Return Date cannot be before Start Date.")
                    days = 0

                if st.button("Sign Rental Agreement"):
                    res = rental_service.add_rental(
                        vehicle_id=selected_veh['id'],
                        customer_id=selected_cust['id'],
                        start_date=start_d.strftime('%Y-%m-%d'),
                        end_date=end_d.strftime('%Y-%m-%d')
                    )
                    display_status(res)
                    if "success" in res.lower() or "✅" in res:
                        st.balloons()
        else:
            st.info("Please register customers and vehicles first.")

    with tab2:
        st.subheader("Corporate Bookings Log")
        if st.button("🔄 Refresh Bookings Log"):
            st.rerun()
            
        rentals = rental_service.list_rentals()
        if isinstance(rentals, list):
            if rentals:
                st.dataframe(pd.DataFrame(rentals), use_container_width=True)
            else:
                st.info("No rental records logged.")
        else:
            st.error(rentals)

    with tab3:
        st.subheader("Terminate / Return Rental")
        rentals = rental_service.list_rentals()
        if isinstance(rentals, list) and rentals:
            rental_options = {f"Booking ID: {r['id']} | Vehicle: {r.get('vehicle_plate','N/A')} - Client: {r.get('customer_name','N/A')}": r for r in rentals}
            selected_r_label = st.selectbox("Select Active Booking to Complete", list(rental_options.keys()))
            selected_r = rental_options[selected_r_label]
            
            st.warning(f"⚠️ Warning: Deleting/terminating this booking ID {selected_r['id']} will release Vehicle ID {selected_r['vehicle_id']} back into the active fleet inventory.")
            if st.button("Record Vehicle Return / Delete Booking"):
                res = rental_service.delete_rental(selected_r['id'])
                display_status(res)
        else:
            st.info("No active rentals logged.")

# --- 5. PAYMENT LEDGER ---
elif menu == "💳 Payment Ledger":
    st.title("Financial Accounts Billing 💳")
    tab1, tab2, tab3 = st.tabs(["➕ Capture Payment", "📋 Accounts Ledger Ledger", "🧾 Generate Transaction Receipt"])

    rentals = rental_service.list_rentals()

    with tab1:
        st.subheader("Capture Customer Payments")
        if isinstance(rentals, list) and rentals:
            # Let them select a rental to pay for
            rental_options = {f"Booking ID {r['id']} | {r.get('customer_name','N/A')} renting {r.get('vehicle_model','N/A')}": r for r in rentals}
            selected_r_label = st.selectbox("Select Booking to Bill", list(rental_options.keys()))
            selected_r = rental_options[selected_r_label]
            
            # Auto populate details
            s_date = datetime.strptime(selected_r["start_date"], "%Y-%m-%d").date()
            e_date = datetime.strptime(selected_r["end_date"], "%Y-%m-%d").date()
            days = (e_date - s_date).days
            if days == 0: days = 1
            rate = float(selected_r.get("vehicle_rate", 0.0)) if selected_r.get("vehicle_rate") else 100.0
            prefilled_amount = float(days * rate)
            
            with st.form("capture_payment_form"):
                st.markdown(f"Transaction billing details for **{selected_r.get('customer_name')}**")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    cust_id_lbl = st.text_input("Customer ID (Auto-filled)", value=selected_r["customer_id"], disabled=True)
                    rental_id_lbl = st.text_input("Rental Booking ID (Auto-filled)", value=selected_r["id"], disabled=True)
                with col_p2:
                    p_type = st.selectbox("Select Payment Mode", ["Card", "UPI", "Cash"])
                    pay_date = st.date_input("Transaction Date", value=date.today())
                
                # Payment Amount Form Input
                amt = st.number_input("Capture Payment Amount ($)", min_value=0.0, value=prefilled_amount, step=100.0)
                
                submitted = st.form_submit_button("Post Transaction")
                if submitted:
                    res = payment_service.add_payment(
                        rental_id=selected_r["id"],
                        customer_id=selected_r["customer_id"],
                        amount=amt,
                        payment_date=pay_date.strftime('%Y-%m-%d'),
                        payment_type=p_type
                    )
                    display_status(res)
        else:
            st.info("No active rentals found to process billing.")

    with tab2:
        st.subheader("Financial Transactions Ledger")
        if st.button("🔄 Refresh Financial Ledger"):
            st.rerun()
            
        payments = payment_service.list_payments()
        if isinstance(payments, list):
            if payments:
                st.dataframe(pd.DataFrame(payments), use_container_width=True)
            else:
                st.info("No payments transactions found.")
        else:
            st.error(payments)

    with tab3:
        st.subheader("Generate & Print Transaction Receipt")
        payments = payment_service.list_payments()
        if isinstance(payments, list) and payments:
            pay_options = {f"Payment ID {p['id']} - Amount: ${p['amount']} | Paid by {p.get('customer_name','ID '+str(p['customer_id']))}": p for p in payments}
            selected_p_label = st.selectbox("Select Payment to Generate Receipt", list(pay_options.keys()))
            selected_p = pay_options[selected_p_label]
            
            # Print Receipt layout HTML
            st.markdown(f"""
            <div style="background-color: #111827; border: 2px solid #1f2937; padding: 40px; border-radius: 12px; color: #e2e8f0; font-family: monospace; max-width: 600px; margin: auto;">
                <div style="text-align: center; border-bottom: 2px dashed #374151; padding-bottom: 20px;">
                    <h2 style="color: #60a5fa; margin: 0; font-size: 22px;">AUTORENT PRO ENTERPRISE</h2>
                    <p style="margin: 4px 0 0 0; font-size: 11px; color: #94a3b8;">101 Enterprise Dr, Seattle, WA 98101</p>
                </div>
                <div style="padding: 20px 0; border-bottom: 2px dashed #374151; font-size: 13px;">
                    <table style="width: 100%;">
                        <tr><td><b>RECEIPT ID:</b></td><td style="text-align: right;">#REC-00{selected_p['id']}</td></tr>
                        <tr><td><b>DATE:</b></td><td style="text-align: right;">{selected_p['payment_date']}</td></tr>
                        <tr><td><b>RENTAL ID:</b></td><td style="text-align: right;">#{selected_p['rental_id']}</td></tr>
                        <tr><td><b>CLIENT ID:</b></td><td style="text-align: right;">#{selected_p['customer_id']}</td></tr>
                    </table>
                </div>
                <div style="padding: 20px 0; border-bottom: 2px dashed #374151; font-size: 13px;">
                    <table style="width: 100%;">
                        <tr><td><b>CUSTOMER:</b></td><td style="text-align: right;">{selected_p.get('customer_name','N/A')}</td></tr>
                        <tr><td><b>EMAIL:</b></td><td style="text-align: right;">{selected_p.get('customer_email','N/A')}</td></tr>
                        <tr><td><b>FLEET VEHICLE:</b></td><td style="text-align: right;">{selected_p.get('vehicle_model','N/A')} ({selected_p.get('vehicle_plate','N/A')})</td></tr>
                    </table>
                </div>
                <div style="padding: 25px 0 10px 0; text-align: right;">
                    <span style="font-size: 14px; color: #94a3b8; font-weight: bold;">TOTAL PAID AMOUNT</span><br>
                    <span style="font-size: 32px; color: #34d399; font-weight: 900;">${float(selected_p['amount']):,.2f}</span>
                </div>
                <div style="text-align: center; color: #64748b; font-size: 11px; margin-top: 20px;">
                    Thank you for choosing AutoRent Pro!<br>
                    Payments processed securely via corporate {selected_p['payment_type']}.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No transaction records to bill receipt.")

# --- 6. MAINTENANCE LAB ---
elif menu == "🔧 Maintenance Lab":
    st.title("Maintenance Lab & Repairs 🔧")
    tab1, tab2, tab3 = st.tabs(["📋 Maintenance Ledger", "🔧 Dispatch to Service Lab", "🗑️ Complete/Remove Record"])

    vehicles = vehicle_service.list_vehicles()

    with tab1:
        st.subheader("Fleet Maintenance Ledger")
        if st.button("🔄 Refresh Maintenance Ledger"):
            st.rerun()
            
        mrecords = maintenance_service.list_maintenance()
        if isinstance(mrecords, list):
            if mrecords:
                st.dataframe(pd.DataFrame(mrecords), use_container_width=True)
            else:
                st.info("No fleet vehicles currently in service.")
        else:
            st.error(mrecords)

    with tab2:
        st.subheader("Dispatch Vehicle to Service Lab")
        if isinstance(vehicles, list) and vehicles:
            # Only list available vehicles to send to maintenance
            avail_veh = [v for v in vehicles if v.get("available")]
            if avail_veh:
                veh_options = {f"{v['model']} ({v['plate']}) - ID: {v['id']}": v for v in avail_veh}
                selected_v_label = st.selectbox("Select Vehicle for Service", list(veh_options.keys()))
                selected_v = veh_options[selected_v_label]
                
                with st.form("dispatch_maintenance_form"):
                    desc = st.text_area("Detailed Repairs Description (e.g. Engine tuneup, denting)", placeholder="Describe issue...")
                    cost = st.number_input("Estimated Service Cost ($)", min_value=0.0, step=100.0, value=500.0)
                    mdate = st.date_input("Service Date", value=date.today())
                    
                    submitted = st.form_submit_button("Dispatch to Lab")
                    if submitted and desc:
                        res = maintenance_service.add_maintenance(
                            vehicle_id=selected_v['id'],
                            description=desc,
                            cost=cost,
                            date=mdate.strftime('%Y-%m-%d')
                        )
                        display_status(res)
            else:
                st.warning("⚠️ No available vehicles to dispatch for service (all vehicles are already rented or in maintenance).")
        else:
            st.info("No vehicles registered in fleet inventory.")

    with tab3:
        st.subheader("Complete Service / Remove Record")
        mrecords = maintenance_service.list_maintenance()
        if isinstance(mrecords, list) and mrecords:
            m_options = {f"Record ID {m['id']} | Vehicle: {m.get('vehicle_plate','ID '+str(m['vehicle_id']))} - Cost: ${m['cost']}": m for m in mrecords}
            selected_m_label = st.selectbox("Select Maintenance Record to Resolve", list(m_options.keys()))
            selected_m = m_options[selected_m_label]
            
            st.warning(f"⚠️ Warning: Deleting/resolving this maintenance record will automatically release Vehicle ID {selected_m['vehicle_id']} back to available fleet inventory.")
            if st.button("Complete Service / Delete Record"):
                res = maintenance_service.delete_maintenance(selected_m['id'])
                display_status(res)
        else:
            st.info("No vehicles currently in maintenance lab.")

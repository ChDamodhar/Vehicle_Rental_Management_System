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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    html, body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f8fafc;
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .auth-container {
        background: rgba(31, 41, 55, 0.6);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 30px 40px;
        max-width: 400px;
        margin: 80px auto;
        box-shadow: 0 10px 20px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
    }
    .auth-container h2 {font-family: 'Outfit', sans-serif; color:#60a5fa; text-align:center; margin-bottom:20px;}
    .auth-container input {font-family: 'Outfit', sans-serif;}
</style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user'] = None

# Initialize SQLite user table (fallback if Supabase not used)
import sqlite3
conn = sqlite3.connect('vehicle_rental.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Authentication UI
auth_option = st.sidebar.selectbox("Authentication", ["Login", "Sign Up"], key="auth_option")
if not st.session_state['authenticated']:
    if auth_option == "Login":
        st.title("AutoRent Pro – Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = cur.fetchone()
            if user:
                st.session_state['authenticated'] = True
                st.session_state['user'] = user[1]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:  # Sign Up
        st.title("AutoRent Pro – Create Account")
        new_user = st.text_input("Choose a username")
        new_pass = st.text_input("Create password", type="password")
        confirm_pass = st.text_input("Confirm password", type="password")
        if st.button("Sign Up"):
            if new_pass != confirm_pass:
                st.error("Passwords do not match")
            elif new_user == "":
                st.error("Username cannot be empty")
            else:
                try:
                    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_user, new_pass))
                    conn.commit()
                    st.success("Account created – you can now log in")
                except sqlite3.IntegrityError:
                    st.error("Username already exists")
    st.stop()

# Initialize Services (only after authentication)
customer_service = CustomerService()
vehicle_service = VehicleService()
rental_service = RentalService()
payment_service = PaymentService()
maintenance_service = MaintenanceService()

# --- Page Configurations ---


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
    ["📊 Dashboard Home", "📈 Business Analysis", "👤 Customer Directory", "🚙 Fleet Inventory", "📝 Rental Bookings", "💳 Payment Ledger", "🔧 Maintenance Lab"]
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
            st.dataframe(r_df[available_cols].head(5), width='stretch')
        else:
            st.info("No recent rentals.")
            
    with log_col2:
        st.subheader("💳 Recent Transactions Ledger")
        if payments_list:
            p_df = pd.DataFrame(payments_list)
            display_cols = ["id", "customer_name", "vehicle_plate", "amount", "payment_type", "payment_date"]
            available_cols = [c for c in display_cols if c in p_df.columns]
            st.dataframe(p_df[available_cols].head(5), width='stretch')
        else:
            st.info("No recent payments.")

# --- 2. BUSINESS ANALYSIS ---
elif menu == "📈 Business Analysis":
    st.title("Business Intelligence & Analytics 📈")
    st.markdown("Deep-dive insights into revenue performance, fleet utilisation, and customer behaviour.")

    # Load all data
    an_vehicles   = vehicle_service.list_vehicles()
    an_rentals    = rental_service.list_rentals()
    an_payments   = payment_service.list_payments()
    an_customers  = customer_service.list_customers()
    an_maint      = maintenance_service.list_maintenance()

    vehicles_list  = an_vehicles  if isinstance(an_vehicles,  list) else []
    rentals_list   = an_rentals   if isinstance(an_rentals,   list) else []
    payments_list  = an_payments  if isinstance(an_payments,  list) else []
    customers_list = an_customers if isinstance(an_customers, list) else []
    maint_list     = an_maint     if isinstance(an_maint,     list) else []

    # ── KPI row ────────────────────────────────────────────────────────────
    total_revenue = sum(float(p.get("amount", 0)) for p in payments_list)
    total_rentals = len(rentals_list)
    total_vehicles = len(vehicles_list)
    avg_rental_value = (total_revenue / total_rentals) if total_rentals else 0
    total_maint_cost = sum(float(m.get("cost", 0)) for m in maint_list)

    k1, k2, k3, k4 = st.columns(4)
    kpi_style = lambda color: f'background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;border-top:4px solid {color};border-radius:12px;padding:20px;text-align:center;'
    with k1:
        st.markdown(f'<div style="{kpi_style("#10b981")}"><div style="color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;">Total Revenue</div><div style="color:#10b981;font-size:28px;font-weight:800;">${total_revenue:,.2f}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div style="{kpi_style("#3b82f6")}"><div style="color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;">Total Rentals</div><div style="color:#3b82f6;font-size:28px;font-weight:800;">{total_rentals}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div style="{kpi_style("#f59e0b")}"><div style="color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;">Avg Rental Value</div><div style="color:#f59e0b;font-size:28px;font-weight:800;">${avg_rental_value:,.2f}</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div style="{kpi_style("#f43f5e")}"><div style="color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;">Maintenance Cost</div><div style="color:#f43f5e;font-size:28px;font-weight:800;">${total_maint_cost:,.2f}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Revenue over time  +  Payment mode breakdown ────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.subheader("💰 Revenue Over Time")
        if payments_list:
            pay_df = pd.DataFrame(payments_list)
            pay_df["amount"] = pay_df["amount"].astype(float)
            if "payment_date" in pay_df.columns:
                rev_trend = pay_df.groupby("payment_date")["amount"].sum().reset_index()
                rev_trend = rev_trend.sort_values("payment_date")
                rev_trend.columns = ["Date", "Revenue ($)"]
                st.line_chart(rev_trend.set_index("Date"))
            else:
                st.info("No date column found in payments data.")
        else:
            st.info("No payment records yet. Add payments to see the revenue trend.")

    with ch2:
        st.subheader("💳 Payment Mode Breakdown")
        if payments_list:
            pay_df2 = pd.DataFrame(payments_list)
            if "payment_type" in pay_df2.columns:
                mode_counts = pay_df2["payment_type"].value_counts().reset_index()
                mode_counts.columns = ["Mode", "Count"]
                st.bar_chart(mode_counts.set_index("Mode"))
            else:
                st.info("No payment type column available.")
        else:
            st.info("No payment records yet.")

    # ── Row 2: Most-used vehicles  +  Vehicle type revenue ─────────────────
    ch3, ch4 = st.columns(2)

    with ch3:
        st.subheader("🚙 Most-Used Vehicles (by Rentals)")
        if rentals_list:
            rent_df = pd.DataFrame(rentals_list)
            if "vehicle_plate" in rent_df.columns:
                usage = rent_df["vehicle_plate"].value_counts().reset_index()
                usage.columns = ["Vehicle Plate", "Rental Count"]
                top10 = usage.head(10)
                st.bar_chart(top10.set_index("Vehicle Plate"))
            elif "vehicle_id" in rent_df.columns:
                usage = rent_df["vehicle_id"].value_counts().reset_index()
                usage.columns = ["Vehicle ID", "Rental Count"]
                top10 = usage.head(10)
                st.bar_chart(top10.set_index("Vehicle ID"))
            else:
                st.info("Vehicle data missing from rental records.")
        else:
            st.info("No rental records yet. Book rentals to see vehicle usage stats.")

    with ch4:
        st.subheader("🏷️ Revenue by Vehicle Type")
        if payments_list and rentals_list:
            pay_df3 = pd.DataFrame(payments_list)
            rent_df3 = pd.DataFrame(rentals_list)
            pay_df3["amount"] = pay_df3["amount"].astype(float)
            # Join payments → rentals → vehicles to get vehicle type
            if "rental_id" in pay_df3.columns and "id" in rent_df3.columns:
                merged = pay_df3.merge(rent_df3[["id","vehicle_id"]], left_on="rental_id", right_on="id", how="left")
                veh_df = pd.DataFrame(vehicles_list)
                if not veh_df.empty and "id" in veh_df.columns and "type" in veh_df.columns:
                    merged2 = merged.merge(veh_df[["id","type"]], left_on="vehicle_id", right_on="id", how="left")
                    type_rev = merged2.groupby("type")["amount"].sum().reset_index()
                    type_rev.columns = ["Vehicle Type", "Revenue ($)"]
                    st.bar_chart(type_rev.set_index("Vehicle Type"))
                else:
                    st.info("Vehicle type data not available.")
            else:
                st.info("Cannot join payment and rental data — missing id columns.")
        else:
            st.info("Add payments and rentals to see revenue by vehicle type.")

    # ── Row 3: Top customers + Fleet utilisation ────────────────────────────
    ch5, ch6 = st.columns(2)

    with ch5:
        st.subheader("👤 Top 10 Customers by Spend")
        if payments_list:
            pay_df4 = pd.DataFrame(payments_list)
            pay_df4["amount"] = pay_df4["amount"].astype(float)
            if "customer_name" in pay_df4.columns:
                top_cust = pay_df4.groupby("customer_name")["amount"].sum().sort_values(ascending=False).head(10).reset_index()
                top_cust.columns = ["Customer", "Total Spend ($)"]
                st.bar_chart(top_cust.set_index("Customer"))
            elif "customer_id" in pay_df4.columns:
                top_cust = pay_df4.groupby("customer_id")["amount"].sum().sort_values(ascending=False).head(10).reset_index()
                top_cust.columns = ["Customer ID", "Total Spend ($)"]
                st.bar_chart(top_cust.set_index("Customer ID"))
            else:
                st.info("Customer data missing from payment records.")
        else:
            st.info("No payment records yet.")

    with ch6:
        st.subheader("📊 Fleet Utilisation Rate")
        if vehicles_list:
            avail = sum(1 for v in vehicles_list if v.get("available"))
            rented = len(vehicles_list) - avail
            util_df = pd.DataFrame({"Status": ["🟢 Available", "🔴 In Use"], "Count": [avail, rented]})
            st.bar_chart(util_df.set_index("Status"))
            util_rate = (rented / len(vehicles_list) * 100) if vehicles_list else 0
            st.metric("Fleet Utilisation Rate", f"{util_rate:.1f}%", delta=f"{rented} vehicles dispatched")
        else:
            st.info("No vehicles registered yet.")

    # ── Detailed data tables ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Detailed Analytics Tables")
    tab_a, tab_b, tab_c = st.tabs(["Revenue Ledger", "Rental Summary", "Maintenance Costs"])

    with tab_a:
        if payments_list:
            p_adf = pd.DataFrame(payments_list)
            p_adf["amount"] = p_adf["amount"].astype(float)
            st.dataframe(p_adf, width='stretch')
            st.markdown(f"**Total Revenue: ${p_adf['amount'].sum():,.2f}** across **{len(p_adf)} transactions**")
        else:
            st.info("No payments recorded yet.")

    with tab_b:
        if rentals_list:
            r_adf = pd.DataFrame(rentals_list)
            st.dataframe(r_adf, width='stretch')
            st.markdown(f"**Total Bookings: {len(r_adf)}**")
        else:
            st.info("No rentals recorded yet.")

    with tab_c:
        if maint_list:
            m_adf = pd.DataFrame(maint_list)
            m_adf["cost"] = m_adf["cost"].astype(float)
            st.dataframe(m_adf, width='stretch')
            st.markdown(f"**Total Maintenance Cost: ${m_adf['cost'].sum():,.2f}**")
        else:
            st.info("No maintenance records yet.")

# --- 3. CUSTOMER DIRECTORY ---
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
                st.dataframe(pd.DataFrame(customers), width='stretch')
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
                st.dataframe(pd.DataFrame(beautified_list), width='stretch')
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
                st.dataframe(pd.DataFrame(rentals), width='stretch')
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
                st.dataframe(pd.DataFrame(payments), width='stretch')
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
                st.dataframe(pd.DataFrame(mrecords), width='stretch')
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

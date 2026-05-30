# Vehicle Rental Management System

## Overview
A professional‑grade vehicle rental management application designed for enterprise use. It features:
- Dual‑mode database architecture (Supabase cloud + local SQLite fallback).
- Robust DAO layer with CRUD operations for customers, vehicles, rentals, payments, and maintenance.
- Streamlit UI with glass‑morphic design, live KPI dashboards, interactive forms, and real‑time metrics.
- CLI for scriptable management.
- Comprehensive test script for validating database connections.

## Getting Started
```bash
# Clone the repository (if not already)
git clone https://github.com/ChDamodhar/Vehicle_Rental_Management_System.git
cd Vehicle_Rental_Management_System

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Configuration
Create a `.env` file at the project root with your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
```
If the Supabase connection fails, the app automatically falls back to a local `vehicle_rental.db` SQLite database.

## Testing the Connection
Run the provided validation script to verify connectivity to Supabase and SQLite:
```bash
python test_conn.py
```

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Ensure code follows the existing style and passes all lint checks.
4. Submit a pull request.

## License
MIT License – see `LICENSE` for details.
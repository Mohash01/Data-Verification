import streamlit as st
import pandas as pd

# Google Sheets ID extracted from your URL
SHEET_ID = "1Zt-TlSOyr-M_uISbp1Y9aomR_pTbHmdUwMwGo7FBUpM"

# Google Sheets CSV export URL
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# Load Google Sheets data
@st.cache_data(ttl=60)  # Refreshes data every 60 seconds
def load_data():
    df = pd.read_csv(CSV_URL)

    # Ensure column names are correctly formatted
    df.columns = df.columns.str.strip()  # Remove extra spaces
    
    # Rename columns for easier access
    df.rename(columns={
        "Timestamp": "timestamp",
        "County": "county",
        "Name of the Participant": "participant_name",
        "Verified Phone Number": "phone_number",
        "Verified ID Number": "id_number",
        "Geo-Coordinates": "geo_coordinates"
    }, inplace=True)

    # Convert timestamp column to datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    return df

# Initialize data
df = load_data()

# Button to manually refresh data
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()  # Clear cached data
    df = load_data()  # Reload fresh data

# Streamlit UI
st.title("Google Sheets Summary Statistics")
st.write("📊 Live Data from Google Sheets")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Date Filter
start_date = st.sidebar.date_input("Start Date", df["timestamp"].min().date())
end_date = st.sidebar.date_input("End Date", df["timestamp"].max().date())

# County Filter
county_list = df["county"].dropna().unique().tolist()
selected_county = st.sidebar.multiselect("Select County", county_list, default=county_list)

# Apply Filters
filtered_df = df[
    (df["timestamp"].dt.date >= start_date) & 
    (df["timestamp"].dt.date <= end_date) & 
    (df["county"].isin(selected_county))
]

# Summary Statistics
total_submissions = len(filtered_df)
unique_counties = filtered_df["county"].nunique()

st.metric("Total Submissions", total_submissions)
st.metric("Total Counties Submitted", unique_counties)

st.write("### Filtered Data")
st.dataframe(filtered_df)

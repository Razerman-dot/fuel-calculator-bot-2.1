import streamlit as st

# Function to load custom CSS safely (with error handling)


def local_css(file_name):
    """
    Loads custom CSS from a file and injects it into the Streamlit app.
    Uses a try/except block to prevent crashes if the CSS file is not found.
    """
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # App will run without custom styles if the file is missing
        print(
            f"Warning: CSS file '{file_name}' not found. Using default Streamlit styles.")
        pass


# Load the external CSS file
local_css("style.css")

st.title("⛽ Fuel Expense & Distance Calculator")
st.write("Easily calculate your weekly and monthly transport or fuel cost!")

# Radio button to choose between calculation modes
mode = st.radio(
    "Choose calculation mode:",
    ["Distance (for car owners)", "Fare (for public transport users)"],
    index=0  # Default to Distance mode
)

# --- Car Owners Mode ---
if mode == "Distance (for car owners)":
    st.subheader("Vehicle Details and Trip Frequency")

    # Input for number of travel days
    days = st.number_input(
        "How many days do you travel in a week?",
        min_value=1,
        max_value=7,
        value=5
    )

    # Input for fuel efficiency
    km_per_litre = st.number_input(
        "Enter your car's fuel efficiency (km per litre):",
        min_value=1.0,
        value=15.0
    )

    # Input for fuel price (using Nigerian Naira symbol ₦ as in original code)
    fuel_price = st.number_input(
        "Enter current fuel price per litre (₦):",
        min_value=1.0,
        value=700.0
    )

    total_cost = 0.0
    st.subheader("Enter your daily distances:")

    # Loop to collect daily distances
    for i in range(int(days)):
        # Ensure unique keys for dynamic input elements
        distance = st.number_input(
            f"Day {i+1} distance (km):",
            min_value=0.0,
            value=10.0,
            key=f"day{i}_dist"
        )

        # Calculate daily cost
        if km_per_litre > 0:
            fuel_used = distance / km_per_litre
            cost = fuel_used * fuel_price
            total_cost += cost
        else:
            # Handle division by zero for safety (though min_value=1.0 prevents it)
            st.error("Fuel efficiency must be greater than zero.")

    # Calculate button and output section
    if st.button("Calculate Fuel Totals"):
        weekly = total_cost
        monthly = weekly * 4.34  # Using 4.34 weeks/month for a more accurate estimate

        st.success(f"💸 Total estimated fuel cost this week = ₦{weekly:,.2f}")
        st.info(f"📅 Estimated monthly fuel cost = ₦{monthly:,.2f}")
        st.caption(
            "💡 Remember to plan ahead and budget wisely! (Monthly estimate uses 4.34 weeks)")

# --- Public Transport Users Mode ---
elif mode == "Fare (for public transport users)":
    st.subheader("Fare and Trip Frequency")

    # Input for daily travel fare
    daily_fare = st.number_input(
        "Enter your average daily transport cost (₦):",
        min_value=0.0,
        value=1000.0
    )

    # Input for number of travel days
    days = st.number_input(
        "How many days do you travel in a week?",
        min_value=1,
        max_value=7,
        value=5,
        key="public_days"
    )

    # Calculate button and output section
    if st.button("Calculate Fare Totals"):
        weekly = daily_fare * days
        monthly = weekly * 4.34  # Using 4.34 weeks/month for a more accurate estimate

        st.success(f"💸 Total estimated fare cost this week = ₦{weekly:,.2f}")
        st.info(f"📅 Estimated monthly fare cost = ₦{monthly:,.2f}")
        st.caption(
            "🚍 Stay smart — track your fares and plan ahead! (Monthly estimate uses 4.34 weeks)")

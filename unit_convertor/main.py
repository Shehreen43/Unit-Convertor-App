import streamlit as st
from datetime import datetime

# Set up the page configuration
st.set_page_config("Unit Converter", page_icon="🟠", layout="centered")

# Conversion factors
conversion_factors = {
    "Length": {
        "meters (📏)": 1,
        "kilometers (🛤️)": 0.001,
        "miles (🛣️)": 0.000621371,
        "feet (👣)": 3.28084
    },
    "Weight": {
        "grams (⚖️)": 1,
        "kilograms (🏋️‍♂️)": 0.001,
        "pounds (🐂)": 0.00220462
    },
    "Volume": {
        "liters (🧴)": 1,
        "milliliters (💦)": 1000,
        "gallons (🛢️)": 0.264172
    },
    "Temperature": {
        "Celsius (🌡️) to Fahrenheit (🔥)": lambda x: (x * 9/5) + 32,
        "Celsius (🌡️) to Kelvin (❄️)": lambda x: x + 273.15,
        "Fahrenheit (🔥) to Celsius (🌡️)": lambda x: (x - 32) * 5/9,
        "Fahrenheit (🔥) to Kelvin (❄️)": lambda x: (x - 32) * 5/9 + 273.15,
        "Kelvin (❄️) to Celsius (🌡️)": lambda x: x - 273.15,
        "Kelvin (❄️) to Fahrenheit (🔥)": lambda x: (x - 273.15) * 9/5 + 32,
    },
    "Time": {
        "seconds (⏳)": 1,
        "minutes (⌛)": 60,
        "hours (⏰)": 3600,
        "days (📆)": 86400
    },
    "Area": {
        "square meters (📐)": 1,
        "square feet (🏠)": 10.7639,
        "acres (🌿)": 0.000247105
    },
    "Pressure": {
        "Pascals (💨)": 1,
        "Bar (🏗️)": 1e-5,
        "PSI (⚙️)": 0.000145038
    },
    "Speed": {
        "m/s (🏃‍♂️)": 1,
        "km/h (🚗💨)": 3.6,
        "mph (🏎️💨)": 2.23694
    },
    "Energy": {
        "Joules (⚡)": 1,
        "Calories (🍕)": 0.239006,
        "kWh (🔋)": 2.7778e-7
    },
}

# Custom CSS for styling the app
st.markdown(
    """
    <style>
    .stApp {
        background: #082032;
        color: #FFFFFF;
    }
    .custom-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #FFA500;
    }
    .custom-subheader {
        font-size: 28px;
        font-weight: bold;
        color: #FF8C00;
        text-align: center;
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #FF8C00;
        color: white;
        font-size: 16px;
        border-radius: 5px;
        border: none;
        transition: 0.3s;
        padding: 10px 20px;
        width: 100%;
        margin-top:14px;
    }
    div.stButton > button:hover {
        background-color: #FFA500;
        transform: scale(1.05);
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .Conversion_history {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-top:14px;
        margin-bottom:10px;
        color: white;
    }
    .record_history {
        text-align: center;
        font-size: 18px;
        margin: 4px;
        color: #FFFFFF;
    }
    .custom-result {
        font-size: 24px;
        font-weight: bold;
        color: #FFA500;
        text-align: center;
        margin-top: 20px;
    }    
    .empty_msg {
        text-align: center;
        font-size: 18px;
        color: #FFFFFF;
    }
    .custom-label {
        color: #FFFFFF;
        font-size: 16px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def unit_convert(value, category, unit_from, unit_to):
    if category == "Temperature":
        key = f"{unit_from} to {unit_to}"
        try:
            if key in conversion_factors["Temperature"]:
                return conversion_factors["Temperature"][key](value)
            else:
                return "Conversion not supported"
        except Exception as e:
            return f"Error in conversion: {str(e)}"
    else:
        if category in conversion_factors and unit_from in conversion_factors[category] and unit_to in conversion_factors[category]:
            return value * (conversion_factors[category][unit_from] / conversion_factors[category][unit_to])
        else:
            return "Conversion not supported"

st.markdown(f"<div class='custom-title'>Unit Converter App</div>", unsafe_allow_html=True)
st.markdown(f"<div class='custom-subheader'>Convert between different units easily! 🟠</div>", unsafe_allow_html=True)

category = st.selectbox("Select Conversion Type", list(conversion_factors.keys()))

# Handle temperature units differently because conversion keys are different
if category == "Temperature":
    temp_units = ["Celsius (🌡️)", "Fahrenheit (🔥)", "Kelvin (❄️)"]
    col1, col2 = st.columns(2)
    with col1:
        unit_from = st.selectbox("Convert from", temp_units)
    with col2:
        unit_to = st.selectbox("Convert to", [u for u in temp_units if u != unit_from])
else:
    col1, col2 = st.columns(2)
    with col1:
        unit_from = st.selectbox("Convert from", list(conversion_factors[category].keys()))
    with col2:
        unit_to = st.selectbox("Convert to", [u for u in conversion_factors[category].keys() if u != unit_from])

value = st.number_input("Enter a value to convert", min_value=1.0, step=1.0)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🔄 Convert"):
    result = unit_convert(value, category, unit_from, unit_to)
    if isinstance(result, str):
        # If error message returned
        st.error(result)
    else:
        precision = 2 if category == "Temperature" else 5
        st.markdown(f"<div class='custom-result'>Converted Value: {result:.{precision}f} {unit_to}</div>", unsafe_allow_html=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        conversion_record = f"{timestamp}: {value} {unit_from} ➝ {result:.{precision}f} {unit_to}"
        st.session_state.history.append(conversion_record)

st.markdown(f"<div class='Conversion_history'>📜 Conversion History</div>", unsafe_allow_html=True)
if st.session_state.history:
    for record in st.session_state.history[-5:]:
        st.markdown(f"<div class='record_history'>{record}</div>", unsafe_allow_html=True)
    if st.button("❌ Clear History"):
        st.session_state.history.clear()
        st.experimental_rerun()
else:
    st.markdown("<div class='empty_msg'>Your conversion history is empty.</div>", unsafe_allow_html=True)

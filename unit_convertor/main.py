import streamlit as st
from datetime import datetime

# Set up the page configuration
st.set_page_config("Unit Converter", page_icon="🟠", layout="centered")

# Accurate conversion factors — ALL in terms of base unit per unit
conversion_factors = {
    "Length": {
        "meters (📏)": 1,
        "kilometers (🛤️)": 1000,
        "miles (🛣️)": 1609.34,
        "feet (👣)": 0.3048
    },
    "Weight": {
        "grams (⚖️)": 1,
        "kilograms (🏋️‍♂️)": 1000,
        "pounds (🐂)": 453.592
    },
    "Volume": {
        "liters (🧴)": 1,
        "milliliters (💦)": 0.001,
        "gallons (🛢️)": 3.78541
    },
    "Temperature": {
        # handled separately in logic
        "Celsius (🌡️)": None,
        "Fahrenheit (🔥)": None,
        "Kelvin (❄️)": None
    },
    "Time": {
        "seconds (⏳)": 1,
        "minutes (⌛)": 60,
        "hours (⏰)": 3600,
        "days (📆)": 86400
    },
    "Area": {
        "square meters (📐)": 1,
        "square feet (🏠)": 0.092903,
        "acres (🌿)": 4046.86
    },
    "Pressure": {
        "Pascals (💨)": 1,
        "Bar (🏗️)": 100000,
        "PSI (⚙️)": 6894.76
    },
    "Speed": {
        "m/s (🏃‍♂️)": 1,
        "km/h (🚗💨)": 1000 / 3600,     # = 0.277778
        "mph (🏎️💨)": 1609.34 / 3600   # = 0.44704
    },
    "Energy": {
        "Joules (⚡)": 1,
        "Calories (🍕)": 4.184,
        "kWh (🔋)": 3.6e6
    },
}

# Temperature conversion map
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius (🌡️)":
        if to_unit == "Fahrenheit (🔥)":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin (❄️)":
            return value + 273.15
    elif from_unit == "Fahrenheit (🔥)":
        if to_unit == "Celsius (🌡️)":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin (❄️)":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin (❄️)":
        if to_unit == "Celsius (🌡️)":
            return value - 273.15
        elif to_unit == "Fahrenheit (🔥)":
            return (value - 273.15) * 9/5 + 32
    return "Unsupported conversion"

# Custom CSS
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
    input[type="number"] {
        color: white !important;
        background-color: #1f1f1f !important;
        border: 1px solid #FFA500 !important;
        padding: 8px 12px !important;
        border-radius: 5px !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    input[type="number"]:focus {
        outline: none !important;
        border-color: #FFA500 !important;
        box-shadow: 0 0 8px 2px #FFA500;
        color: white !important;
        background-color: #121212 !important;
    }
    div[role="combobox"] > div > div > div > select {
        color: white !important;
        background-color: #1f1f1f !important;
        border: 1px solid #FFA500 !important;
        border-radius: 5px !important;
        font-size: 16px !important;
        padding: 8px 12px !important;
        transition: 0.3s;
    }
    div[role="combobox"] > div > div > div > select:focus {
        outline: none !important;
        border-color: #FFA500 !important;
        box-shadow: 0 0 8px 2px #FFA500;
        background-color: #121212 !important;
        color: white !important;
    }
    label {
        color: white !important;
        font-weight: 600;
        font-size: 16px;
    }
    input::placeholder {
        color: #ccc !important;
    }
    div.stButton > button {
        background-color: #FF8C00 !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 5px !important;
        border: none !important;
        transition: 0.3s !important;
        padding: 10px 20px !important;
        width: 100% !important;
        margin-top: 14px !important;
    }
    div.stButton > button:hover {
        background-color: #FFA500 !important;
        transform: scale(1.05) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def unit_convert(value, category, unit_from, unit_to):
    if category == "Temperature":
        return convert_temperature(value, unit_from, unit_to)
    try:
        factor_from = conversion_factors[category][unit_from]
        factor_to = conversion_factors[category][unit_to]
        return value * (factor_from / factor_to)
    except Exception as e:
        return f"Conversion error: {e}"

# UI rendering
st.markdown(f"<div class='custom-title'>Unit Converter App</div>", unsafe_allow_html=True)
st.markdown(f"<div class='custom-subheader'>Convert between different units easily! 🟠</div>", unsafe_allow_html=True)

category = st.selectbox("Select Conversion Type", list(conversion_factors.keys()))

col1, col2 = st.columns(2)

if category == "Temperature":
    temp_units = list(conversion_factors["Temperature"].keys())
    with col1:
        unit_from = st.selectbox("Convert from", temp_units)
    with col2:
        unit_to = st.selectbox("Convert to", [u for u in temp_units if u != unit_from])
else:
    units = list(conversion_factors[category].keys())
    with col1:
        unit_from = st.selectbox("Convert from", units)
    with col2:
        unit_to = st.selectbox("Convert to", [u for u in units if u != unit_from])

value = st.number_input("Enter a value to convert", min_value=1.0, step=1.0)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🔄 Convert"):
    result = unit_convert(value, category, unit_from, unit_to)
    if isinstance(result, str):
        st.error(result)
    else:
        precision = 2 if category == "Temperature" else 5
        st.markdown(f"<div class='custom-result'>Converted Value: {result:.{precision}f} {unit_to}</div>", unsafe_allow_html=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{timestamp} | {value} {unit_from} → {result:.{precision}f} {unit_to} ({category})"
        st.session_state.history.append(record)

st.markdown(f"<div class='Conversion_history'>Conversion History</div>", unsafe_allow_html=True)
if st.session_state.history:
    for record in st.session_state.history[-5:]:
        st.markdown(f"<div class='record_history'>{record}</div>", unsafe_allow_html=True)
    if st.button("❌ Clear History"):
        st.session_state.history.clear()
else:
    st.markdown("<div class='empty_msg'>Your conversion history is empty.</div>", unsafe_allow_html=True)

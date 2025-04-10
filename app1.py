import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import random
import datetime

# ---------- Page Config ----------
st.set_page_config(page_title="Transit E-Ticket", page_icon="🚌", layout="centered")

# ---------- Styles ----------
st.markdown("""
    <style>
        body {
            background-color: #f2f2f2;
        }
        .ticket-box {
            background-color: white;
            padding: 2rem;
            width: 420px;
            margin: auto;
            border-radius: 25px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
            background-image: url('https://cdn.pixabay.com/photo/2017/03/01/22/14/bus-2116072_1280.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center center;
            color: #000;
            position: relative;
        }
        .fare-box {
            font-size: 22px;
            font-weight: bold;
            color: #2a9d8f;
            margin-top: 1rem;
            text-align: center;
        }
        .route-button {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            background-color: #1d3557;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }
        .center {
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Helper Function ----------
def generate_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return Image.open(buffer)

# ---------- Input Form ----------
st.title("🎟️ Appealing Smart Transit E-Ticket")

with st.form("ticket_form"):
    booking_date = st.date_input("📅 Booking Date", datetime.date.today())
    name = st.text_input("👤 Passenger Name")
    num_passengers = st.number_input("👥 Number of Passengers", min_value=1, max_value=10, value=1)
    source = st.text_input("🚌 Source")
    destination = st.text_input("📍 Destination")
    submit = st.form_submit_button("Generate Ticket")

if submit:
    if all([name.strip(), source.strip(), destination.strip()]):
        # Auto fare calculation
        fare = random.randint(15, 30) * num_passengers

        qr_data = f"Passenger: {name}\nFrom: {source}\nTo: {destination}\nFare: ₹{fare}"
        qr_img = generate_qr(qr_data)

        # Display Ticket
        st.markdown(f"""
            <div class='ticket-box'>
                <a class='route-button' href='https://your-route-optimizer-link.com' target='_blank'>View Routes</a>
                <h2 style='text-align:center;'>🚌 E-Ticket</h2>
                <p><strong>Date:</strong> {booking_date}</p>
                <p><strong>Passenger:</strong> {name}</p>
                <p><strong>Passengers:</strong> {num_passengers}</p>
                <p><strong>From:</strong> {source}</p>
                <p><strong>To:</strong> {destination}</p>
                <p class='fare-box'>Auto Fare Detected: ₹{fare}</p>
            </div>
        """, unsafe_allow_html=True)

        # QR Code Display
        st.markdown("<div class='center'>", unsafe_allow_html=True)
        st.image(qr_img, caption="Scan for Ticket Info", width=180)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download Option
        ticket_text = f"""
E-Ticket Receipt
------------------
Date: {booking_date}
Passenger Name: {name}
Number of Passengers: {num_passengers}
From: {source}
To: {destination}
Fare: ₹{fare}
Status: Paid
"""
        buffer = BytesIO()
        buffer.write(ticket_text.encode())
        buffer.seek(0)
        st.download_button("📥 Download E-Ticket", data=buffer, file_name=f"ticket_{name}.txt", mime="text/plain")
    else:
        st.error("⚠️ Please fill in all fields before generating your ticket.")

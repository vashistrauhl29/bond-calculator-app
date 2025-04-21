import streamlit as st
import numpy as np
from scipy.optimize import newton

st.title("📈 Bond Valuation Calculator")

# --- Inputs ---
face_value = st.number_input("Face Value ($)", value=1000)
maturity_years = st.number_input("Maturity Period (Years)", value=10)
annual_coupon_rate = st.number_input("Annual Coupon Rate (%)", value=4.0)
market_rate = st.number_input("Opportunity Cost of Capital (%)", value=5.0)
payments_per_year = st.number_input("Number of Payments per Year", value=2)

# --- PV Calculation ---
def bond_pv(face_value, maturity_years, annual_coupon_rate, market_rate, payments_per_year):
    n = payments_per_year
    T = maturity_years * n
    cpn = (annual_coupon_rate / 100) * face_value / n
    r = (1 + market_rate / 100) ** (1 / n) - 1
    pv_coupons = sum([cpn / ((1 + r) ** t) for t in range(1, T + 1)])
    pv_face = face_value / ((1 + r) ** T)
    return round(pv_coupons + pv_face, 2)

bond_price = bond_pv(face_value, maturity_years, annual_coupon_rate, market_rate, payments_per_year)
st.success(f"📌 Present Value (Bond Price): ${bond_price}")

# --- YTM Calculation ---
def bond_price_given_ytm(face_value, maturity_years, annual_coupon_rate, ytm_rate, payments_per_year):
    n = payments_per_year
    T = maturity_years * n
    cpn = (annual_coupon_rate / 100) * face_value / n
    r = ytm_rate / n
    pv_coupons = sum([cpn / ((1 + r) ** t) for t in range(1, T + 1)])
    pv_face = face_value / ((1 + r) ** T)
    return pv_coupons + pv_face

def calculate_ytm(face_value, maturity_years, annual_coupon_rate, current_price, payments_per_year):
    def f(ytm):
        return bond_price_given_ytm(face_value, maturity_years, annual_coupon_rate, ytm, payments_per_year) - current_price
    ytm = newton(f, x0=0.05)
    return round(ytm * 100, 2)

if st.checkbox("🔍 Calculate YTM from Bond Price"):
    market_price = st.number_input("Enter Bond Price", value=923.0)
    ytm = calculate_ytm(face_value, maturity_years, annual_coupon_rate, market_price, payments_per_year)
    st.info(f"📌 Yield to Maturity (YTM): {ytm}%")

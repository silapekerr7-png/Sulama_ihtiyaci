import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('irrigation_model.pkl')
df = pd.read_csv('ornek.csv')

def ozellik(d):
    d = d.copy()
    d['ET0'] = d['Temperature_C'] * d['Wind_Speed_kmh'] * d['Sunlight_Hours'] / d['Humidity']
    d['Water_Balance'] = d['Rainfall_mm'] + d['Previous_Irrigation_mm'] - d['ET0']
    d['Moisture_Stress'] = d['Temperature_C'] * (100 - d['Humidity']) / d['Soil_Moisture']
    return d.replace([np.inf, -np.inf], 0).fillna(0)

st.title(':droplet: Sulama İhtiyacı Tahmini')

col1, col2 = st.columns(2)

with col1:
    soil = st.selectbox('Toprak tipi', sorted(df['Soil_Type'].unique()))
    crop = st.selectbox('Ürün', sorted(df['Crop_Type'].unique()))
    stage = st.selectbox('Büyüme aşaması', sorted(df['Crop_Growth_Stage'].unique()))
    season = st.selectbox('Mevsim', sorted(df['Season'].unique()))
    irr = st.selectbox('Sulama tipi', sorted(df['Irrigation_Type'].unique()))
    water = st.selectbox('Su kaynağı', sorted(df['Water_Source'].unique()))
    region = st.selectbox('Bölge', sorted(df['Region'].unique()))
    mulch = st.radio('Malç kullanıldı mı?', sorted(df['Mulching_Used'].unique()))

with col2:
    ph = st.number_input('Toprak pH', value=float(df['Soil_pH'].median()))
    moist = st.number_input('Toprak nemi (%)', min_value=1.0, value=float(df['Soil_Moisture'].median()))
    carbon = st.number_input('Organik karbon', value=float(df['Organic_Carbon'].median()))
    ec = st.number_input('Elektriksel iletkenlik', value=float(df['Electrical_Conductivity'].median()))
    temp = st.number_input('Sıcaklık (°C)', value=float(df['Temperature_C'].median()))
    hum = st.number_input('Nem (%)', min_value=1.0, value=float(df['Humidity'].median()))
    rain = st.number_input('Yağış (mm)', value=float(df['Rainfall_mm'].median()))
    sun = st.number_input('Güneşlenme (saat)', value=float(df['Sunlight_Hours'].median()))
    wind = st.number_input('Rüzgar hızı (km/h)', value=float(df['Wind_Speed_kmh'].median()))
    area = st.number_input('Tarla alanı (hektar)', value=float(df['Field_Area_hectare'].median()))
    prev = st.number_input('Önceki sulama (mm)', value=float(df['Previous_Irrigation_mm'].median()))

if st.button('Tahmin Et'):
    veri = pd.DataFrame([{'Soil_Type': soil, 'Soil_pH': ph, 'Soil_Moisture': moist, 'Organic_Carbon': carbon,
                          'Electrical_Conductivity': ec, 'Temperature_C': temp, 'Humidity': hum, 'Rainfall_mm': rain,
                          'Sunlight_Hours': sun, 'Wind_Speed_kmh': wind, 'Crop_Type': crop, 'Crop_Growth_Stage': stage,
                          'Season': season, 'Irrigation_Type': irr, 'Water_Source': water, 'Field_Area_hectare': area,
                          'Mulching_Used': mulch, 'Previous_Irrigation_mm': prev, 'Region': region}])
    tahmin = model.predict(ozellik(veri))[0]
    st.success(f"Sulama ihtiyacı: {['Low', 'Medium', 'High'][tahmin]}")
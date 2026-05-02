import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# FUNCIÓN PDF
# =========================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    pdf = FPDF()
    pdf.add_page()

    # =========================
    # FUENTES
    # =========================
    pdf.set_font("Arial", "B", 16)

    # =========================
    # HEADER IZQUIERDA
    # =========================
    x_left = 10
    y_start = 10

    pdf.set_xy(x_left, y_start)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(90, 8, "SI AL MERITO", ln=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)

    pdf.set_x(x_left)
    pdf.cell(90, 6, "NIT: 7379694", ln=1)

    pdf.set_x(x_left)
    pdf.cell(90, 6, "Talleres, Cursos y Asesorias Especializadas", ln=1)

    pdf.set_text_color(0, 102, 0)
    pdf.set_x(x_left)
    pdf.cell(90, 6, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=1)

    pdf.set_x(x_left)
    pdf.cell(90, 6, "Correo: si.al.merito2026@gmail.com", ln=1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_x(x_left)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(90, 6, f"Fecha de generacion: {fecha}", ln=1)

    # =========================
    # HEADER DERECHA
    # =========================
    x_right = 110
    y_right = y_start

    pdf.set_xy(x_right, y_right)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 6, "INFORMACION DEL CONCURSO", ln=1)

    pdf.set_font("Arial", "", 11)

    pdf.set_x(x_right)
    pdf.cell(80, 6, f"Entidad: {entidad}", ln=1)

    pdf.set_x(x_right)
    pdf.cell(80, 6, f"Convocatoria: {convocatoria}", ln=1)

    pdf.set_x(x_right)
    pdf.cell(80, 6, f"Nivel: {nivel}", ln=1)

    pdf.set_x(x_right)
    pdf.cell(80, 6, f"Cargo: {cargo}", ln=1)

    pdf.set_x(x_right)
    pdf.cell(80, 6, f"OPEC: {opec}", ln=1)

    # =========================
    # LÍNEA VERTICAL
    # =========================
    pdf.line(105, 10, 105, 45)

    # =========================
    # LÍNEA HORIZONTAL
    # =========================
    pdf.line(10, 50, 200, 50)

    pdf.ln(10)

    # =========================
    # TEMAS
    # =========================
    pdf.set_font("Arial", "B", 12)

    temas = []
    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = [line.strip() for line in f if line.strip()]

    for i, tema in enumerate(temas, 1):
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"{i}. Tema: {tema}", ln=1)

        query = tema.replace(" ", "+")
        link = f"https://www.youtube.com/results?search_query={query}"

        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "", 10)

        for _ in range(3):
            pdf.cell(0, 6, f"- {link}", ln=1)

        pdf.ln(3)
        pdf.set_font("Arial", "B", 12)

    # =========================
    # GUARDAR PDF
    # =========================
    nombre = f"{OUTPUT_DIR}/{opec}_{cargo.replace(' ', '_')}.pdf"
    pdf.output(nombre)

    return nombre

# =========================
# INTERFAZ STREAMLIT
# =========================
st.set_page_config(page_title="SI AL MERITO", layout="centered")

st.title("📄 SI AL MÉRITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("🚀 Generar PDF"):

    if not all([entidad, convocatoria, nivel, opec, cargo]):
        st.warning("Por favor completa todos los campos")
    else:
        ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
        st.success(f"PDF generado en: {ruta}")

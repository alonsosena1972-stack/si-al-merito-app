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
# CLASE PDF
# =========================
class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

# =========================
# GENERAR PDF
# =========================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    pdf = PDF()
    pdf.add_page()

    # 🔥 FUENTE UNICODE (SOLUCIÓN REAL)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)

    # =========================
    # HEADER IZQUIERDA
    # =========================
    pdf.set_xy(10, 10)

    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(90, 8, "SI AL MERITO", ln=1)

    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(0, 0, 0)

    pdf.set_x(10)
    pdf.cell(90, 6, "NIT: 7379694", ln=1)

    pdf.set_x(10)
    pdf.cell(90, 6, "Talleres, Cursos y Asesorias Especializadas", ln=1)

    pdf.set_text_color(0, 102, 0)
    pdf.set_x(10)
    pdf.cell(90, 6, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=1)

    pdf.set_x(10)
    pdf.cell(90, 6, "Correo: si.al.merito2026@gmail.com", ln=1)

    pdf.set_text_color(0, 0, 0)
    fecha = datetime.now().strftime("%d/%m/%Y")

    pdf.set_x(10)
    pdf.cell(90, 6, f"Fecha de generación: {fecha}", ln=1)

    # =========================
    # HEADER DERECHA
    # =========================
    pdf.set_xy(110, 10)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(80, 6, "INFORMACIÓN DEL CONCURSO", ln=1)

    pdf.set_font("DejaVu", "", 11)

    pdf.set_x(110)
    pdf.cell(80, 6, f"Entidad: {entidad}", ln=1)

    pdf.set_x(110)
    pdf.cell(80, 6, f"Convocatoria: {convocatoria}", ln=1)

    pdf.set_x(110)
    pdf.cell(80, 6, f"Nivel: {nivel}", ln=1)

    pdf.set_x(110)
    pdf.cell(80, 6, f"Cargo: {cargo}", ln=1)

    pdf.set_x(110)
    pdf.cell(80, 6, f"OPEC: {opec}", ln=1)

    # =========================
    # LÍNEAS
    # =========================
    pdf.line(105, 10, 105, 45)   # línea vertical
    pdf.line(10, 50, 200, 50)    # línea horizontal

    pdf.ln(10)

    # =========================
    # TEMAS
    # =========================
    pdf.set_font("DejaVu", "B", 12)

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
        pdf.set_font("DejaVu", "", 10)

        for _ in range(3):
            pdf.cell(0, 6, f"- {link}", ln=1)

        pdf.ln(3)
        pdf.set_font("DejaVu", "B", 12)

    # =========================
    # GUARDAR PDF
    # =========================
    nombre = f"{OUTPUT_DIR}/{opec}_{cargo.replace(' ', '_')}.pdf"
    pdf.output(nombre)

    return nombre

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="SI AL MÉRITO", layout="centered")

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

import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

st.set_page_config(page_title="SI AL MÉRITO", layout="centered")

# =========================
# PDF PROFESIONAL
# =========================
class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 10, f"Página {self.page_no()} | SI AL MÉRITO", align="C")

def generar_pdf(entidad, convocatoria, nivel, opec, cargo):
    pdf = PDF()
    pdf.add_page()

    # =========================
    # HEADER
    # =========================
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 10, "SI AL MÉRITO", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "NIT: 7379694", ln=True)
    pdf.cell(0, 6, "Cursos y Asesorías Especializadas", ln=True)

    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 6, "WhatsApp: 3146715497", ln=True)
    pdf.cell(0, 6, "Correo: si.al.merito2026@gmail.com", ln=True)

    pdf.set_text_color(0, 0, 0)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 6, f"Fecha: {fecha}", ln=True)

    pdf.ln(5)

    # =========================
    # INFO CONCURSO
    # =========================
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "INFORMACIÓN DEL CONCURSO", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    pdf.ln(5)

    # =========================
    # TEMAS
    # =========================
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    pdf.set_font("Helvetica", "", 10)

    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = f.readlines()

        for i, tema in enumerate(temas, 1):
            tema = tema.strip()
            if tema:
                pdf.cell(0, 6, f"{i}. {tema}", ln=True)
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 6, f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)

    # =========================
    # GUARDAR
    # =========================
    os.makedirs("output", exist_ok=True)
    nombre = f"OPEC_{opec}_{cargo}.pdf".replace(" ", "_")
    ruta = os.path.join("output", nombre)

    pdf.output(ruta)

    return ruta

# =========================
# UI
# =========================
st.title("SI AL MÉRITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):
    if entidad and convocatoria and nivel and opec and cargo:
        ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)

        st.success(f"PDF generado en: {ruta}")

        with open(ruta, "rb") as f:
            st.download_button(
                "Descargar PDF",
                f,
                file_name=os.path.basename(ruta)
            )
    else:
        st.warning("Completa todos los campos")

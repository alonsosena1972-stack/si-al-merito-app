import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN BASE
# =========================
st.set_page_config(page_title="SI AL MÉRITO", layout="centered")

# =========================
# FUNCIÓN PDF PROFESIONAL
# =========================
class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Página {self.page_no()} | SI AL MÉRITO", 0, 0, "C")

def generar_pdf(entidad, convocatoria, nivel, opec, cargo):
    pdf = PDF()
    pdf.add_page()

    base_dir = os.path.dirname(__file__)

    # Rutas fuentes
    font_regular = os.path.join(base_dir, "DejaVuSans.ttf")
    font_bold = os.path.join(base_dir, "DejaVuSans-Bold.ttf")

    # Cargar fuentes
    pdf.add_font("DejaVu", "", font_regular, uni=True)
    pdf.add_font("DejaVu", "B", font_bold, uni=True)

    # =========================
    # HEADER NIVEL DIOS
    # =========================

    # IZQUIERDA
    pdf.set_xy(10, 10)
    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(90, 8, "SI AL MÉRITO", 0, 1)

    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(90, 6, "NIT: 7379694", 0, 1)
    pdf.cell(90, 6, "Cursos y Asesorías Especializadas", 0, 1)

    pdf.set_text_color(0, 100, 0)
    pdf.cell(90, 6, "WhatsApp: 3146715497", 0, 1)
    pdf.cell(90, 6, "Correo: si.al.merito2026@gmail.com", 0, 1)

    pdf.set_text_color(0, 0, 0)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(90, 6, f"Fecha: {fecha}", 0, 1)

    # LÍNEA VERTICAL
    pdf.line(105, 10, 105, 50)

    # DERECHA
    pdf.set_xy(110, 10)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(90, 8, "INFORMACIÓN DEL CONCURSO", 0, 1)

    pdf.set_font("DejaVu", "", 10)
    pdf.set_x(110)
    pdf.cell(90, 6, f"Entidad: {entidad}", 0, 1)

    pdf.set_x(110)
    pdf.cell(90, 6, f"Convocatoria: {convocatoria}", 0, 1)

    pdf.set_x(110)
    pdf.cell(90, 6, f"Nivel: {nivel}", 0, 1)

    pdf.set_x(110)
    pdf.cell(90, 6, f"Cargo: {cargo}", 0, 1)

    pdf.set_x(110)
    pdf.cell(90, 6, f"OPEC: {opec}", 0, 1)

    # Línea horizontal
    pdf.line(10, 55, 200, 55)

    # =========================
    # TEMAS
    # =========================
    pdf.set_xy(10, 65)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", 0, 1)

    pdf.set_font("DejaVu", "", 10)

    temas_path = os.path.join(base_dir, "temas.txt")

    if os.path.exists(temas_path):
        with open(temas_path, "r", encoding="utf-8") as f:
            temas = f.readlines()

        for i, tema in enumerate(temas, 1):
            tema = tema.strip()
            if tema:
                pdf.cell(0, 6, f"{i}. {tema}", 0, 1)
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 6, f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}", 0, 1)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)

    # =========================
    # GUARDAR EN OUTPUT
    # =========================
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    nombre_archivo = f"OPEC_{opec}_{cargo}.pdf".replace(" ", "_")
    ruta = os.path.join(output_dir, nombre_archivo)

    pdf.output(ruta)

    return ruta

# =========================
# INTERFAZ STREAMLIT
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
                label="Descargar PDF",
                data=f,
                file_name=os.path.basename(ruta),
                mime="application/pdf"
            )
    else:
        st.warning("Completa todos los campos")

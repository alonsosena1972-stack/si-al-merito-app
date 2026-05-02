import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

st.set_page_config(page_title="SI AL MÉRITO")

# =========================
# PDF PROFESIONAL
# =========================
class PDF(FPDF):

    def header(self):
        # Título
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 100, 0)
        self.cell(0, 8, "SI AL MÉRITO", ln=True)

        # Info empresa
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, "NIT: 7379694", ln=True)
        self.cell(0, 6, "Cursos y Asesorías Especializadas", ln=True)

        self.set_text_color(0, 100, 0)
        self.cell(0, 6, "WhatsApp: 3146715497", ln=True)
        self.cell(0, 6, "Correo: si.al.merito2026@gmail.com", ln=True)

        self.set_text_color(0, 0, 0)
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 6, f"Fecha de generación: {fecha}", ln=True)

        # Línea
        self.line(10, 45, 200, 45)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)

        # Número de página
        self.cell(0, 5, f"Página {self.page_no()}", 0, 1, "C")

        # Derechos
        self.cell(0, 5, "© SI AL MÉRITO - Uso exclusivo educativo", 0, 0, "C")


def limpiar(texto):
    return texto.encode("latin-1", "ignore").decode("latin-1")


def generar_pdf(entidad, convocatoria, nivel, opec, cargo):
    pdf = PDF()
    pdf.add_page()

    # =========================
    # BLOQUE INFORMACIÓN
    # =========================
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "INFORMACIÓN DEL CONCURSO", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.ln(2)

    pdf.cell(0, 6, limpiar(f"Entidad: {entidad}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Convocatoria: {convocatoria}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Nivel: {nivel}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Cargo: {cargo}"), ln=True)
    pdf.cell(0, 6, limpiar(f"OPEC: {opec}"), ln=True)

    # Línea separación
    pdf.ln(4)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # =========================
    # TEMAS
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    pdf.set_font("Arial", "", 10)

    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = f.readlines()

        for i, tema in enumerate(temas, 1):
            tema = limpiar(tema.strip())
            if tema:
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, f"{i}. Tema: {tema}", ln=True)

                pdf.set_font("Arial", "", 10)
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 6, f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}", ln=True)
                pdf.set_text_color(0, 0, 0)

                pdf.ln(2)

    # =========================
    # GUARDAR EN OUTPUT
    # =========================
    os.makedirs("output", exist_ok=True)

    nombre = f"OPEC_{opec}_{cargo}.pdf".replace(" ", "_")
    ruta = os.path.join("output", nombre)

    pdf.output(ruta)

    return ruta


# =========================
# INTERFAZ
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

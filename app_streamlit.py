import streamlit as st
from fpdf import FPDF
import re

# ==============================
# LIMPIAR TEXTO (ANTI-UNICODE)
# ==============================
def limpiar(texto):
    texto = str(texto)
    return re.sub(r'[^\x00-\xFF]+', '', texto)

# ==============================
# LEER TEMAS
# ==============================
def leer_temas():
    try:
        with open("temas.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Control fiscal", "Funcion publica"]

# ==============================
# PDF
# ==============================
class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 12)

        self.set_text_color(0, 128, 0)
        self.cell(0, 6, "SI AL MERITO - ASESORIAS", ln=True, align="C")

        self.set_text_color(0, 0, 0)
        self.cell(0, 5, "CONCURSOS DE CARRERA ADMINISTRATIVA", ln=True, align="C")

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

# ==============================
# GENERAR PDF
# ==============================
def generar_pdf_bytes(entidad, convocatoria, nivel, opec, cargo):

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "", 11)

    pdf.cell(0, 6, f"Entidad: {limpiar(entidad)}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {limpiar(convocatoria)}", ln=True)
    pdf.cell(0, 6, f"Nivel: {limpiar(nivel)}", ln=True)
    pdf.cell(0, 6, f"OPEC: {limpiar(opec)}", ln=True)   # ✔ OPEC correcto
    pdf.cell(0, 6, f"Cargo: {limpiar(cargo)}", ln=True) # ✔ CARGO correcto

    pdf.ln(5)

    temas = leer_temas()

    for i, tema in enumerate(temas, start=1):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"{i}. Tema: {limpiar(tema)}", ln=True)

        pdf.set_font("Arial", "", 11)
        link = f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}"
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 6, link, ln=True, link=link)

        pdf.ln(3)

    contenido = pdf.output(dest="S")
    pdf_bytes = contenido.encode("latin-1", "ignore")

    return pdf_bytes

# ==============================
# STREAMLIT
# ==============================
st.set_page_config(page_title="SI AL MERITO", layout="centered")

st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")      # ✔ OPEC correcto
cargo = st.text_input("Cargo")    # ✔ CARGO correcto

if st.button("Generar PDF"):
    if entidad and convocatoria and nivel and opec and cargo:

        pdf_bytes = generar_pdf_bytes(entidad, convocatoria, nivel, opec, cargo)

        nombre_archivo = f"OPEC_{opec}_{cargo}.pdf"

        st.download_button(
            label="Descargar PDF",
            data=pdf_bytes,
            file_name=nombre_archivo,
            mime="application/pdf"
        )

    else:
        st.warning("Completa todos los campos")
  

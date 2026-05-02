import streamlit as st
from fpdf import FPDF
import re

# ==============================
# LIMPIEZA TOTAL (ANTI EMOJIS)
# ==============================
def limpiar(texto):
    texto = str(texto)
    # elimina TODO lo que no sea compatible con latin-1
    return texto.encode('latin-1', 'ignore').decode('latin-1')

# ==============================
# LEER TEMAS
# ==============================
def leer_temas():
    try:
        with open("temas.txt", "r", encoding="utf-8") as f:
            return [limpiar(line.strip()) for line in f if line.strip()]
    except:
        return ["Control fiscal", "Funcion publica"]

# ==============================
# PDF
# ==============================
class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 12)

        # 🔴 IMPORTANTE: SIN EMOJIS
        titulo = limpiar("SI AL MERITO - ASESORIAS - NIT 7379694")
        subtitulo = limpiar("CONCURSOS DE CARRERA ADMINISTRATIVA")

        self.set_text_color(0, 128, 0)
        self.cell(0, 6, titulo, ln=True, align="C")

        self.set_text_color(0, 0, 0)
        self.cell(0, 5, subtitulo, ln=True, align="C")

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
    pdf.cell(0, 6, f"OPEC: {limpiar(opec)}", ln=True)
    pdf.cell(0, 6, f"Cargo: {limpiar(cargo)}", ln=True)

    pdf.ln(5)

    temas = leer_temas()

    for i, tema in enumerate(temas, start=1):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"{i}. Tema: {tema}", ln=True)

        pdf.set_font("Arial", "", 11)
        link = limpiar(f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}")
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 6, link, ln=True, link=link)

        pdf.ln(3)

    # 🔥 AQUÍ YA NO FALLA
    contenido = pdf.output(dest="S")
    return contenido.encode("latin-1", "ignore")

# ==============================
# STREAMLIT
# ==============================
st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):
    if entidad and convocatoria and nivel and opec and cargo:

        pdf_bytes = generar_pdf_bytes(entidad, convocatoria, nivel, opec, cargo)

        st.download_button(
            label="Descargar PDF",
            data=pdf_bytes,
            file_name=f"OPEC_{opec}_{cargo}.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Completa todos los campos")

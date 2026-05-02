import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

OUTPUT_DIR = "output"
CONTADOR_FILE = "contador.txt"

# ===============================
# CONTADOR DE ARCHIVOS
# ===============================
def obtener_numero():
    if not os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "w") as f:
            f.write("1")
        return 1

    with open(CONTADOR_FILE, "r") as f:
        numero = int(f.read().strip())

    with open(CONTADOR_FILE, "w") as f:
        f.write(str(numero + 1))

    return numero


# ===============================
# LEER TEMAS
# ===============================
def leer_temas():
    if not os.path.exists("temas.txt"):
        return ["CONTROL INTERNO", "MECI"]

    with open("temas.txt", "r", encoding="utf-8") as f:
        return [t.strip() for t in f.readlines() if t.strip()]


# ===============================
# PDF PERSONALIZADO
# ===============================
class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 100, 0)
        self.cell(0, 10, "SI AL MERITO", ln=True)

        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, "NIT: 7379694", ln=True)
        self.cell(0, 6, "Cursos y Asesorias Especializadas", ln=True)

        self.set_text_color(0, 120, 0)
        self.cell(0, 6, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=True)

        self.set_text_color(0, 0, 0)
        self.cell(0, 6, "Correo: si.al.merito2026@gmail.com", ln=True)

        self.cell(0, 6, f"Fecha de generacion: {datetime.now().strftime('%d/%m/%Y')}", ln=True)

        self.ln(2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()} | SI AL MERITO", align="C")


# ===============================
# GENERAR PDF
# ===============================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    numero = obtener_numero()

    entidad_clean = entidad.replace(" ", "_").upper()
    cargo_clean = cargo.replace(" ", "_").upper()

    nombre_archivo = f"{OUTPUT_DIR}/{numero}_OPEC_{opec}_{cargo_clean}_{entidad_clean}_{convocatoria}.pdf"

    pdf = PDF()
    pdf.add_page()

    # INFO DEL CONCURSO
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "INFORMACION DEL CONCURSO", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # TEMAS
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    temas = leer_temas()

    for i, tema in enumerate(temas, 1):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{i}. Tema: {tema}", ln=True)

        # 4 enlaces por tema
        enlaces = [
            f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}",
            f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}+clase",
            f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}+explicacion",
            f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}+ejemplos",
        ]

        for url in enlaces:
            bullet = chr(149)

            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 5, bullet)

            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 5, url, ln=True)

        pdf.ln(2)

    pdf.output(nombre_archivo)

    return nombre_archivo


# ===============================
# STREAMLIT UI
# ===============================
st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):
    ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
    st.success(f"PDF generado en: {ruta}")

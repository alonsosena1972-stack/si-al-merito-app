import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

OUTPUT_DIR = "output"
CONTADOR_FILE = "contador.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===== LIMPIADOR DE TEXTO (CLAVE) =====
def limpiar_texto(texto):
    return texto.encode("latin-1", "ignore").decode("latin-1")


# ===== CONTADOR =====
def obtener_numero():
    if not os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "w") as f:
            f.write("1")

    with open(CONTADOR_FILE, "r") as f:
        numero = int(f.read().strip())

    with open(CONTADOR_FILE, "w") as f:
        f.write(str(numero + 1))

    return numero


# ===== PDF =====
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    pdf = FPDF()
    pdf.add_page()

    # limpiar inputs
    entidad = limpiar_texto(entidad)
    convocatoria = limpiar_texto(convocatoria)
    nivel = limpiar_texto(nivel)
    opec = limpiar_texto(opec)
    cargo = limpiar_texto(cargo)

    # ===== HEADER =====
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 10, "SI AL MERITO", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "NIT: 7379694", ln=True)
    pdf.cell(0, 6, "Cursos y Asesorias Especializadas", ln=True)

    pdf.set_text_color(0, 102, 0)
    pdf.cell(0, 6, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "Correo: si.al.merito2026@gmail.com", ln=True)

    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 6, f"Fecha de generacion: {fecha}", ln=True)

    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    # ===== INFO =====
    pdf.ln(5)
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

    # ===== TEMAS =====
    pdf.ln(5)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    pdf.set_font("Arial", "", 11)

    temas = []
    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = [limpiar_texto(t.strip()) for t in f if t.strip()]

    for i, tema in enumerate(temas, 1):
        pdf.ln(2)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{i}. Tema: {tema}", ln=True)

        pdf.set_font("Arial", "", 10)
        url = f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}"
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 5, f"- {url}", ln=True)

    # ===== FOOTER =====
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Pagina {pdf.page_no()} | SI AL MERITO", align="C")

    # ===== GUARDAR =====
    numero = obtener_numero()
    nombre = f"{OUTPUT_DIR}/{numero}_OPEC_{opec}_{cargo.replace(' ', '_')}.pdf"

    pdf.output(nombre)

    return nombre


# ===== INTERFAZ =====
st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):
    ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
    st.success(f"PDF generado en: {ruta}")

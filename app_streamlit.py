import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="SI AL MÉRITO")

# =========================
# FUNCIÓN SEGURA (SIN ERRORES)
# =========================
def limpiar(texto):
    return texto.encode("latin-1", "ignore").decode("latin-1")

def generar_pdf(entidad, convocatoria, nivel, opec, cargo):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, limpiar("SI AL MÉRITO"), ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, limpiar("NIT: 7379694"), ln=True)
    pdf.cell(0, 6, limpiar("Cursos y Asesorías Especializadas"), ln=True)
    pdf.cell(0, 6, limpiar("WhatsApp: 3146715497"), ln=True)
    pdf.cell(0, 6, limpiar("Correo: si.al.merito2026@gmail.com"), ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, limpiar("INFORMACIÓN DEL CONCURSO"), ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, limpiar(f"Entidad: {entidad}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Convocatoria: {convocatoria}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Nivel: {nivel}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Cargo: {cargo}"), ln=True)
    pdf.cell(0, 6, limpiar(f"OPEC: {opec}"), ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, limpiar("TEMAS DE ESTUDIO"), ln=True)

    pdf.set_font("Arial", "", 10)

    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = f.readlines()

        for i, tema in enumerate(temas, 1):
            tema = limpiar(tema.strip())
            if tema:
                pdf.cell(0, 6, f"{i}. {tema}", ln=True)
                pdf.cell(0, 6, f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}", ln=True)
                pdf.ln(2)

    os.makedirs("output", exist_ok=True)

    ruta = f"output/OPEC_{opec}_{cargo}.pdf".replace(" ", "_")
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
            st.download_button("Descargar PDF", f, file_name=os.path.basename(ruta))
    else:
        st.warning("Completa todos los campos")

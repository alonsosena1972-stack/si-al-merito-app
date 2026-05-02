import streamlit as st
from fpdf import FPDF
import io

# ==============================
# 🧠 LIMPIAR TEXTO (EVITA ERRORES UTF)
# ==============================
def limpiar_pdf(texto):
    return texto.encode('latin-1', 'replace').decode('latin-1')

# ==============================
# 📂 LEER TEMAS
# ==============================
def leer_temas():
    try:
        with open("temas.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Control fiscal en Colombia", "Función pública Colombia"]

# ==============================
# 📄 CLASE PDF (HEADER PRO)
# ==============================
class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 12)

        texto1 = "SÍ AL MÉRITO"
        texto2 = " - ASESORIAS - NIT. 7.379.694"

        ancho_total = self.get_string_width(texto1 + texto2)
        self.set_x((210 - ancho_total) / 2)

        self.set_text_color(0, 128, 0)
        self.cell(self.get_string_width(texto1), 6, texto1)

        self.set_text_color(0, 0, 0)
        self.cell(self.get_string_width(texto2), 6, texto2, ln=True)

        self.set_font("Arial", "", 9)
        self.multi_cell(
            0,
            5,
            "CONCURSOS DE CARRERA ADMINISTRATIVA PARA BACHILLERES, TECNICOS, TECNOLOGOS Y PROFESIONALES",
            align="C"
        )

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

# ==============================
# 📄 GENERAR PDF EN MEMORIA
# ==============================
def generar_pdf_bytes(entidad, convocatoria, nivel, opec, cargo):

    temas = leer_temas()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Entidad: {limpiar_pdf(entidad)}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {limpiar_pdf(convocatoria)}", ln=True)
    pdf.cell(0, 6, f"Nivel: {limpiar_pdf(nivel)}", ln=True)
    pdf.cell(0, 6, f"OPEC: {limpiar_pdf(opec)}", ln=True)

    pdf.ln(5)

    for idx, tema in enumerate(temas, start=1):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"{idx}. Tema: {limpiar_pdf(tema)}", ln=True)

        for _ in range(3):
            link = f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}"
            pdf.set_font("Arial", "", 11)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 6, link, ln=True, link=link)

        pdf.ln(4)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes

# ==============================
# 🖥️ INTERFAZ STREAMLIT
# ==============================
st.set_page_config(page_title="SI AL MÉRITO", layout="centered")

st.title("📚 SI AL MÉRITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo (nombre del empleo)")

if st.button("🚀 Generar PDF"):
    if entidad and convocatoria and nivel and opec and cargo:

        pdf_bytes = generar_pdf_bytes(entidad, convocatoria, nivel, opec, cargo)

        nombre = f"OPEC_{opec}_{cargo}.pdf"

        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_bytes,
            file_name=nombre,
            mime="application/pdf"
        )

    else:
        st.warning("⚠️ Completa todos los campos")

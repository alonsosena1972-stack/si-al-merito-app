import streamlit as st
from fpdf import FPDF
import os

# ==============================
# 🧠 FUNCIONES BASE
# ==============================

def limpiar_texto(texto):
    return texto.upper().replace(" ", "_").replace(",", "").replace(".", "")

def obtener_consecutivo():
    if not os.path.exists("contador.txt"):
        with open("contador.txt", "w") as f:
            f.write("1")

    with open("contador.txt", "r") as f:
        numero = int(f.read())

    with open("contador.txt", "w") as f:
        f.write(str(numero + 1))

    return numero

def leer_temas():
    try:
        with open("temas.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

# ==============================
# 📄 CLASE PDF (HEADER PODEROSO)
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

        texto1 = "LÍNEAS DE ATENCIÓN "
        texto2 = "WhatsApp"
        texto3 = ": 3146715497 - 3001892130 - 3004417737"

        ancho_total = self.get_string_width(texto1 + texto2 + texto3)
        self.set_x((210 - ancho_total) / 2)

        self.set_text_color(0, 0, 0)
        self.cell(self.get_string_width(texto1), 5, texto1)

        self.set_text_color(0, 128, 0)
        self.cell(self.get_string_width(texto2), 5, texto2)

        self.set_text_color(0, 0, 0)
        self.cell(self.get_string_width(texto3), 5, texto3, ln=True)

        self.cell(0, 5, "Correo: si.al.merito2026@gmail.com", ln=True, align="C")

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


# ==============================
# 📄 GENERAR PDF
# ==============================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    temas = leer_temas()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 🔹 BLOQUE DE IDENTIFICACIÓN
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    pdf.ln(5)

    # 🔹 TEMAS + LINKS
    for idx, tema in enumerate(temas, start=1):

        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"{idx}. Tema: {tema}", ln=True)

        for _ in range(3):
            link = f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}"

            pdf.set_font("Arial", "", 11)

            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 6, "-")

            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 6, link, ln=True, link=link)

        pdf.ln(4)

    # 🔹 DERECHOS
    pdf.ln(5)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(80, 80, 80)

    pdf.multi_cell(
        0,
        5,
        "© SI AL MÉRITO. Material de uso educativo. Prohibida su reproducción total o parcial."
    )

    # 🔹 CARPETA
    if not os.path.exists("output"):
        os.makedirs("output")

    # 🔹 NOMBRE ARCHIVO
    consecutivo = obtener_consecutivo()

    nombre_archivo = f"output/{consecutivo}_OPEC_{opec}_{limpiar_texto(cargo)}_{limpiar_texto(entidad)}_{convocatoria}.pdf"

    pdf.output(nombre_archivo)

    return nombre_archivo


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
        archivo = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
        st.success(f"✅ PDF generado correctamente")
        st.write(f"📂 {archivo}")
    else:
        st.warning("⚠️ Por favor completa todos los campos")
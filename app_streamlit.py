import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# =========================
# CONTADOR
# =========================
def obtener_consecutivo():
    archivo = "contador.txt"

    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            f.write("1")

    with open(archivo, "r") as f:
        num = int(f.read().strip())

    with open(archivo, "w") as f:
        f.write(str(num + 1))

    return num


# =========================
# CLASE PDF
# =========================
class PDF(FPDF):

    def header(self):

        # LOGO SEGURO (NO ROMPE NADA)
        try:
            if os.path.exists("logo.png"):
                self.image("logo.png", x=175, y=8, w=18)
        except:
            pass

        # TITULO
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 100, 0)
        self.cell(0, 8, "SI AL MERITO", ln=True)

        # DATOS
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 10)
        self.cell(0, 5, "NIT: 7379694", ln=True)
        self.cell(0, 5, "Cursos y Asesorias Especializadas", ln=True)
        self.cell(0, 5, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=True)
        self.cell(0, 5, "Correo: si.al.merito2026@gmail.com", ln=True)

        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 5, f"Fecha de generacion: {fecha}", ln=True)

        self.ln(1)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "", 9)
        self.cell(0, 5, f"Pagina {self.page_no()} - SI AL MERITO", align="C")


# =========================
# GENERAR PDF
# =========================
def generar_pdf(aspirante, entidad, convocatoria, nivel, opec, cargo):

    pdf = PDF()
    pdf.add_page()

    # TITULO SECCION
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "INFORMACION DEL CONCURSO", ln=True)

    pdf.ln(1)

    # ASPIRANTE (SIN ESPACIO EXTRA)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, f"Aspirante: {aspirante.upper()}", ln=True)

    # RESTO
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    pdf.ln(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    # TEMAS
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "TEMAS DE ESTUDIO", ln=True)

    pdf.ln(2)

    temas = []
    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = [t.strip() for t in f if t.strip()]

    for i, tema in enumerate(temas, 1):

        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, f"{i}. Tema: {tema}", ln=True)

        variantes = [
            tema,
            tema + " clase",
            tema + " explicacion",
            tema + " ejemplos"
        ]

        for v in variantes:
            url = "https://www.youtube.com/results?search_query=" + v.replace(" ", "+")

            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 4, chr(149))  # viñeta segura

            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 4, url, ln=True)

        pdf.ln(1)

    # GUARDAR
    if not os.path.exists("output"):
        os.makedirs("output")

    numero = obtener_consecutivo()

    nombre_archivo = f"output/{numero}_OPEC_{opec}_{cargo}_{entidad}_{convocatoria}.pdf"

    pdf.output(nombre_archivo)

    return nombre_archivo


# =========================
# STREAMLIT
# =========================
st.title("SI AL MERITO - Generador de PDFs")

aspirante = st.text_input("Nombre del aspirante")
entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
cargo = st.text_input("Cargo")
opec = st.text_input("OPEC")

if st.button("Generar PDF"):

    if aspirante and entidad:
        ruta = generar_pdf(aspirante, entidad, convocatoria, nivel, opec, cargo)
        st.success(f"PDF generado en: {ruta}")
    else:
        st.error("Faltan datos")

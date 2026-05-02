import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# =========================
# CONFIGURACION PDF
# =========================
class PDF(FPDF):

    def header(self):
        # TITULO
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 100, 0)
        self.cell(0, 10, "SI AL MERITO", ln=True)

        # LOGO A LA DERECHA
        if os.path.exists("logo.png"):
            self.image("logo.png", x=170, y=8, w=25)

        # DATOS EMPRESA
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 11)
        self.cell(0, 6, "NIT: 7379694", ln=True)
        self.cell(0, 6, "Cursos y Asesorias Especializadas", ln=True)
        self.cell(0, 6, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=True)
        self.cell(0, 6, "Correo: si.al.merito2026@gmail.com", ln=True)

        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 6, f"Fecha de generacion: {fecha}", ln=True)

        # LINEA
        self.ln(2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "", 9)
        self.cell(0, 8, f"Pagina {self.page_no()} - SI AL MERITO", align="C")

# =========================
# FUNCION PDF
# =========================
def generar_pdf(nombre, entidad, convocatoria, nivel, opec, cargo):

    pdf = PDF()
    pdf.add_page()

    # TITULO SECCION
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "INFORMACION DEL CONCURSO", ln=True)

    pdf.ln(2)

    # NOMBRE USUARIO
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, f"Nombre: {nombre.upper()}", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.ln(2)

    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    # LINEA
    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # TEMAS
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    pdf.ln(3)

    temas = [
        "CONTROL INTERNO",
        "MECI",
        "AUDITORIA INTERNA",
        "CONTROL FISCAL"
    ]

    pdf.set_font("Arial", "", 11)

    for i, tema in enumerate(temas, 1):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{i}. Tema: {tema}", ln=True)

        pdf.set_font("Arial", "", 10)

        base = tema.replace(" ", "+")

        links = [
            f"https://www.youtube.com/results?search_query={base}",
            f"https://www.youtube.com/results?search_query={base}+clase",
            f"https://www.youtube.com/results?search_query={base}+explicacion",
            f"https://www.youtube.com/results?search_query={base}+ejemplos",
        ]

        for link in links:
            pdf.cell(5)
            pdf.cell(0, 5, "- " + link, ln=True)

        pdf.ln(2)

    # =========================
    # GUARDAR EN OUTPUT NUMERADO
    # =========================
    if not os.path.exists("output"):
        os.makedirs("output")

    archivos = os.listdir("output")
    numero = len(archivos) + 1

    nombre_archivo = f"output/{numero}_OPEC_{opec}_{cargo}_{entidad}_{convocatoria}.pdf"

    pdf.output(nombre_archivo)

    return nombre_archivo

# =========================
# STREAMLIT UI
# =========================
st.title("Generador PDF - SI AL MERITO")

nombre = st.text_input("Nombre completo")
entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
cargo = st.text_input("Cargo")
opec = st.text_input("OPEC")

if st.button("Generar PDF"):

    if nombre and entidad:
        ruta = generar_pdf(nombre, entidad, convocatoria, nivel, opec, cargo)

        st.success("PDF generado correctamente")
        st.write(ruta)
    else:
        st.error("Faltan datos")

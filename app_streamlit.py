import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime


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


class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 102, 0)
        self.cell(0, 8, "SI AL MERITO", ln=True)

        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)

        self.cell(0, 5, "NIT: 7379694", ln=True)
        self.cell(0, 5, "Cursos y Asesorias Especializadas", ln=True)

        self.set_text_color(0, 128, 0)
        self.cell(0, 5, "WhatsApp: 3146715497 - 3153838792 - 3004417737", ln=True)
        self.cell(0, 5, "Correo: si.al.merito2026@gmail.com", ln=True)

        self.set_text_color(0, 0, 0)
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 5, "Fecha de generacion: " + fecha, ln=True)

        self.ln(2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 8)
        self.cell(0, 5, "Pagina " + str(self.page_no()) + " - SI AL MERITO", align="C")


def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    os.makedirs("output", exist_ok=True)
    consecutivo = obtener_consecutivo()

    nombre = "output/" + str(consecutivo) + "_OPEC_" + opec + "_" + cargo.upper() + "_" + entidad.upper() + "_" + convocatoria + ".pdf"

    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "INFORMACION DEL CONCURSO", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.ln(1)

    pdf.cell(0, 5, "Entidad: " + entidad, ln=True)
    pdf.cell(0, 5, "Convocatoria: " + convocatoria, ln=True)
    pdf.cell(0, 5, "Nivel: " + nivel, ln=True)
    pdf.cell(0, 5, "Cargo: " + cargo, ln=True)
    pdf.cell(0, 5, "OPEC: " + opec, ln=True)

    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "TEMAS DE ESTUDIO", ln=True)

    pdf.ln(1)

    temas = []
    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = [t.strip() for t in f if t.strip()]

    for i, tema in enumerate(temas, 1):

        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, str(i) + ". Tema: " + tema, ln=True)

        variantes = [
            tema,
            tema + " clase",
            tema + " explicacion",
            tema + " ejemplos"
        ]

        for v in variantes:
            url = "https://www.youtube.com/results?search_query=" + v.replace(" ", "+")

            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 4, "-")

            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 4, url, ln=True)

        pdf.ln(1)

    pdf.output(nombre)
    return nombre


st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):

    if not entidad or not convocatoria or not nivel or not opec or not cargo:
        st.warning("Completa todos los campos")
    else:
        try:
            ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
            st.success("PDF generado en: " + ruta)
        except Exception as e:
            st.error(str(e))

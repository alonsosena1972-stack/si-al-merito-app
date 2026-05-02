import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# ==============================
# 🧹 LIMPIAR TEXTO (ANTI ERRORES)
# ==============================
def limpiar(texto):
    return str(texto).encode("latin-1", "ignore").decode("latin-1")


# ==============================
# 🔢 CONTADOR AUTOMATICO
# ==============================
def obtener_consecutivo():
    if not os.path.exists("contador.txt"):
        with open("contador.txt", "w") as f:
            f.write("1")

    with open("contador.txt", "r") as f:
        numero = int(f.read())

    with open("contador.txt", "w") as f:
        f.write(str(numero + 1))

    return numero


# ==============================
# 📂 LEER TEMAS
# ==============================
def leer_temas():
    if not os.path.exists("temas.txt"):
        return []

    with open("temas.txt", "r", encoding="utf-8") as f:
        return [limpiar(line.strip()) for line in f if line.strip()]


# ==============================
# 📄 CLASE PDF PROFESIONAL
# ==============================
class PDF(FPDF):

    def header(self):

        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 128, 0)
        self.cell(0, 10, limpiar("SI AL MERITO"), ln=True)

        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)

        self.cell(0, 6, limpiar("NIT: 7379694"), ln=True)
        self.cell(0, 6, limpiar("Talleres, Cursos y Asesorias Especializadas"), ln=True)

        self.set_text_color(0, 128, 0)
        self.cell(0, 6, limpiar("WhatsApp: 3146715497 - 3153838792 - 3004417737"), ln=True)
        self.cell(0, 6, limpiar("Correo: si.al.merito2026@gmail.com"), ln=True)

        self.set_text_color(0, 0, 0)
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 6, f"Fecha de generacion: {fecha}", ln=True)

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)


    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)

        self.cell(0, 5, f"Pagina {self.page_no()}", align="C")
        self.ln(4)
        self.cell(
            0,
            5,
            limpiar("SI AL MERITO - Material de uso educativo y preparacion de concursos"),
            align="C"
        )


# ==============================
# 📄 GENERAR PDF
# ==============================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    temas = leer_temas()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 🔹 INFORMACION DEL CONCURSO
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, limpiar("INFORMACION DEL CONCURSO"), ln=True)

    pdf.ln(3)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, limpiar(f"Entidad: {entidad}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Convocatoria: {convocatoria}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Nivel: {nivel}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Cargo: {cargo}"), ln=True)
    pdf.cell(0, 6, limpiar(f"OPEC: {opec}"), ln=True)

    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # 🔹 TEMAS
    for i, tema in enumerate(temas, start=1):

        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, limpiar(f"{i}. Tema: {tema}"), ln=True)

        link = f"https://www.youtube.com/results?search_query={tema.replace(' ', '+')}"

        pdf.set_font("Arial", "", 11)

        for _ in range(3):
            pdf.set_text_color(0, 0, 0)
            pdf.cell(5, 6, "-")

            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 6, limpiar(link), ln=True, link=link)

        pdf.ln(3)

    # 📁 GUARDAR
    if not os.path.exists("output"):
        os.makedirs("output")

    consecutivo = obtener_consecutivo()

    nombre_archivo = f"{consecutivo}_OPEC_{opec}_{cargo.replace(' ', '_')}.pdf"
    ruta = os.path.join("output", nombre_archivo)

    pdf.output(ruta)

    return ruta


# ==============================
# 🚀 INTERFAZ STREAMLIT
# ==============================
st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):

    if entidad and convocatoria and nivel and opec and cargo:

        ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)

        st.success(f"PDF generado en: {ruta}")

    else:
        st.warning("Por favor completa todos los campos")

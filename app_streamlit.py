import streamlit as st
from fpdf import FPDF
import os

# ==============================
# 🧹 LIMPIAR TEXTO (CLAVE DEL FIX)
# ==============================
def limpiar(texto):
    return texto.encode("latin-1", "ignore").decode("latin-1")


# ==============================
# 📌 CONTADOR
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
# 📌 TEMAS
# ==============================
def leer_temas():
    if not os.path.exists("temas.txt"):
        return []

    with open("temas.txt", "r", encoding="utf-8") as f:
        return [limpiar(line.strip()) for line in f if line.strip()]


# ==============================
# 📄 PDF
# ==============================
class PDF(FPDF):

    def header(self):

        self.set_font("Arial", "B", 12)

        t1 = limpiar("SI AL MERITO")
        t2 = limpiar(" - ASESORIAS - NIT 7379694")

        ancho = self.get_string_width(t1 + t2)
        self.set_x((210 - ancho) / 2)

        self.set_text_color(0, 128, 0)
        self.cell(self.get_string_width(t1), 6, t1)

        self.set_text_color(0, 0, 0)
        self.cell(self.get_string_width(t2), 6, t2, ln=True)

        self.set_font("Arial", "", 9)
        self.multi_cell(
            0,
            5,
            limpiar("CONCURSOS DE CARRERA ADMINISTRATIVA PARA BACHILLERES, TECNICOS, TECNOLOGOS Y PROFESIONALES"),
            align="C"
        )

        self.cell(0, 5, limpiar("Correo: si.al.merito2026@gmail.com"), ln=True, align="C")

        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)


# ==============================
# 📄 GENERAR PDF
# ==============================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    temas = leer_temas()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "", 11)

    pdf.cell(0, 6, limpiar(f"Entidad: {entidad}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Convocatoria: {convocatoria}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Nivel: {nivel}"), ln=True)
    pdf.cell(0, 6, limpiar(f"OPEC: {opec}"), ln=True)
    pdf.cell(0, 6, limpiar(f"Cargo: {cargo}"), ln=True)

    pdf.ln(8)

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

    # 📁 OUTPUT
    if not os.path.exists("output"):
        os.makedirs("output")

    consecutivo = obtener_consecutivo()

    nombre = f"{consecutivo}_OPEC_{opec}_{cargo.replace(' ', '_')}.pdf"
    ruta = os.path.join("output", nombre)

    pdf.output(ruta)

    return ruta


# ==============================
# 🚀 STREAMLIT
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
        st.warning("Completa todos los campos")

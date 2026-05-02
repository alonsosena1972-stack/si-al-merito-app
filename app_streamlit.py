import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# ===== CONFIG =====
OUTPUT_DIR = "output"
CONTADOR_FILE = "contador.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===== UTIL =====
def limpiar_texto(texto: str) -> str:
    # Elimina caracteres que rompen FPDF (latin-1)
    return (texto or "").encode("latin-1", "ignore").decode("latin-1")


def obtener_numero() -> int:
    if not os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "w") as f:
            f.write("1")

    with open(CONTADOR_FILE, "r") as f:
        numero = int(f.read().strip())

    with open(CONTADOR_FILE, "w") as f:
        f.write(str(numero + 1))

    return numero


def normalizar_tema(tema: str) -> str:
    # Convierte "control_interno" -> "Control Interno"
    t = tema.replace("_", " ").strip()
    return t.title()


def generar_busquedas(tema: str):
    # 4 variaciones útiles por tema
    base = tema.replace("_", " ").strip()
    return [
        base,
        base + " Colombia",
        base + " explicacion",
        base + " ejemplos",
    ]


# ===== PDF =====
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    # limpiar inputs
    entidad = limpiar_texto(entidad)
    convocatoria = limpiar_texto(convocatoria)
    nivel = limpiar_texto(nivel)
    opec = limpiar_texto(opec)
    cargo = limpiar_texto(cargo)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

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

    # línea superior (compacta)
    pdf.ln(2)
    y = pdf.get_y()
    pdf.line(10, y, 200, y)

    # ===== INFO CONCURSO =====
    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "INFORMACION DEL CONCURSO", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 6, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 6, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 6, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 6, f"OPEC: {opec}", ln=True)

    # línea inferior (compacta)
    pdf.ln(2)
    y = pdf.get_y()
    pdf.line(10, y, 200, y)

    # ===== TEMAS =====
    pdf.ln(4)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "TEMAS DE ESTUDIO", ln=True)

    pdf.set_font("Arial", "", 11)

    temas = []
    if os.path.exists("temas.txt"):
        with open("temas.txt", "r", encoding="utf-8") as f:
            temas = [limpiar_texto(t.strip()) for t in f if t.strip()]

    for i, tema in enumerate(temas, 1):
        pdf.ln(2)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 11)

        titulo = normalizar_tema(tema)
        pdf.cell(0, 6, f"{i}. Tema: {titulo}", ln=True)

        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 255)

        busquedas = generar_busquedas(tema)

        for b in busquedas:
            query = b.replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={query}"
            pdf.cell(0, 5, f"- {url}", ln=True)

    # ===== FOOTER =====
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Pagina {pdf.page_no()} | SI AL MERITO", align="C")

    # ===== GUARDAR =====
    numero = obtener_numero()
    nombre_archivo = f"{OUTPUT_DIR}/{numero}_OPEC_{opec}_{cargo.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)

    return nombre_archivo


# ===== UI =====
st.title("SI AL MERITO - Generador de PDFs")

entidad = st.text_input("Entidad")
convocatoria = st.text_input("Convocatoria")
nivel = st.text_input("Nivel")
opec = st.text_input("OPEC")
cargo = st.text_input("Cargo")

if st.button("Generar PDF"):
    ruta = generar_pdf(entidad, convocatoria, nivel, opec, cargo)
    st.success(f"PDF generado en: {ruta}")

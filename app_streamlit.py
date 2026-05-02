import os
from fpdf import FPDF
from datetime import datetime

# =========================
# CONTADOR PDF
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
        self.cell(0, 5, f"Fecha de generacion: {fecha}", ln=True)

        self.ln(2)  # 🔥 espacio mínimo
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)  # 🔥 pegado fino

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "I", 8)
        self.cell(0, 5, f"Pagina {self.page_no()} - SI AL MERITO", align="C")


# =========================
# GENERAR PDF
# =========================
def generar_pdf(entidad, convocatoria, nivel, opec, cargo):

    os.makedirs("output", exist_ok=True)
    consecutivo = obtener_consecutivo()

    nombre_archivo = f"output/{consecutivo}_OPEC_{opec}_{cargo.upper()}_{entidad.upper()}_{convocatoria}.pdf"

    pdf = PDF()
    pdf.add_page()

    # =========================
    # INFORMACION DEL CONCURSO
    # =========================
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "INFORMACION DEL CONCURSO", ln=True)

    pdf.ln(1)  # 🔥 reducido

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 5, f"Entidad: {entidad}", ln=True)
    pdf.cell(0, 5, f"Convocatoria: {convocatoria}", ln=True)
    pdf.cell(0, 5, f"Nivel: {nivel}", ln=True)
    pdf.cell(0, 5, f"Cargo: {cargo}", ln=True)
    pdf.cell(0, 5, f"OPEC: {opec}", ln=True)

    pdf.ln(2)  # 🔥 antes era 5 → ahora fino
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)  # 🔥 pegado correcto

    # =========================
    # TEMAS
    # =========================
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 6, "TEMAS DE ESTUDIO", ln=True)

    pdf.ln(1)

    temas = []
    with open("temas.txt", "r", encoding="utf-8") as f:
        temas = [t.strip() for t in f if t.strip()]

    for i, tema in enumerate(temas, 1):

        # 🔥 TITULO NEGRO
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, f"{i}. Tema: {tema}", ln=True)

        # 🔥 LINKS (4 VARIANTES)
        variantes = [
            tema,
            f"{tema} clase",
            f"{tema} explicacion",
            f"{tema} ejemplos"
        ]

        for v in variantes:
            url = f"https://www.youtube.com/results?search_query={v.replace(' ', '+')}"

            # viñeta negra
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 10)
            pdf.cell(5, 4, chr(149))

            # link azul
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 4, url, ln=True)

        pdf.ln(1)  # 🔥 compacto entre temas

    pdf.output(nombre_archivo)

    return nombre_archivo

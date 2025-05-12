import PyPDF2

def extraer_texto_pdf(pdf_path):
    """Extrae y devuelve el texto de un archivo PDF."""
    texto = ""
    with open(pdf_path, "rb") as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        for pagina in lector_pdf.pages:
            if pagina.extract_text():
                texto += pagina.extract_text() + "\n"
    return texto

from io import BytesIO
from pypdf import PdfReader

MAX_CARACTERES = 12000

def extraer_texto(contenido: bytes) -> str:
    lector = PdfReader(BytesIO(contenido))
    paginas = [(p.extract_text() or "") for p in lector.pages]
    return "\n".join(paginas).strip()[:MAX_CARACTERES]
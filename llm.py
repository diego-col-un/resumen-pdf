from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# num_ctx amplía el contexto: por defecto Ollama usa uno pequeño
# y recortaría el PDF en silencio.
modelo = ChatOllama(model="llama3.2", num_ctx=8192, temperature=0.3)

def resumir(texto: str) -> str:
    prompt = (
        "Por favor genera un resumen de máximo 250 palabras "
        f"del siguiente documento:\n\n{texto}"
    )
    return modelo.invoke([HumanMessage(content=prompt)]).content


if __name__ == "__main__":
    print(resumir("Python es un lenguaje de alto nivel muy usado en ciencia de datos."))
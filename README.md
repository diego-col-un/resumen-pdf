# Resumen de PDF con IA

Aplicación web que recibe un PDF, genera un resumen de máximo 250 palabras con un modelo de lenguaje local (**Ollama + llama3.2**) y lo guarda en **Firebase Firestore**. El frontend lee el resumen directamente desde Firestore y lo muestra en pantalla.

Proyecto del curso **Ciencia de los Datos**, Universidad Nacional de Colombia.

## Cómo funciona

```
Frontend (HTML + JS + CSS)
   │  sube el PDF
   ▼
Backend (Flask)
   │  extrae el texto del PDF (pypdf)
   │  lo envía a llama3.2 con la instrucción de resumir (Ollama)
   │  guarda el resumen en Firestore (firebase-admin)
   ▼
Firebase Firestore  ──►  Frontend muestra el resumen
```

1. El usuario selecciona un PDF en la página.
2. Flask recibe el archivo en `/upload` y extrae su texto.
3. El texto se envía a llama3.2 con la instrucción: *"Por favor genera un resumen de máximo 250 palabras"*.
4. El resumen se guarda en la colección `resumenes` de Firestore.
5. Flask responde con el ID del documento y el frontend lo lee desde Firestore.

## Tecnologías

- **Frontend:** HTML, CSS y JavaScript (SDK web de Firebase por CDN)
- **Backend:** Python, Flask
- **Modelo:** Ollama con llama3.2, usado a través de `langchain-ollama`
- **Extracción de texto:** pypdf
- **Base de datos:** Firebase Firestore (`firebase-admin` en el backend)

## Estructura del proyecto

```
resumen-pdf/
├── app.py                  # Servidor Flask y ruta /upload
├── llm.py                  # Conexión con Ollama y prompt de resumen
├── pdf_utils.py            # Extracción de texto del PDF
├── firebase_db.py          # Guardado del resumen en Firestore
├── templates/
│   └── index.html
├── static/
│   ├── app.js              # Subida del PDF y lectura desde Firestore
│   └── style.css
├── requirements.txt
└── .gitignore
```

## Requisitos previos

- Python 3
- [Ollama](https://ollama.com) instalado, con el modelo descargado:
  ```bash
  ollama pull llama3.2
  ```
- Un proyecto de Firebase con **Firestore** creado (ver más abajo)

## Instalación

```bash
git clone https://github.com/diego-col-un/resumen-pdf.git
cd resumen-pdf

python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell)
# source .venv/bin/activate   # Linux / macOS

pip install -r requirements.txt
```

## Configuración de Firebase

1. Crea un proyecto en la [consola de Firebase](https://console.firebase.google.com) y activa **Firestore Database** en modo producción.
2. **Clave del backend:** en *Configuración del proyecto → Cuentas de servicio → Generar nueva clave privada*. Guarda el archivo como `serviceAccountKey.json` en la raíz del proyecto.
   > Este archivo da acceso de administrador a tu proyecto. Está en `.gitignore` y **nunca debe subirse al repositorio**.
3. **Permisos:** la cuenta de servicio necesita el rol **Cloud Datastore User** en IAM para escribir en Firestore.
4. **Configuración del frontend:** registra una app web en *Configuración del proyecto → Tus apps* y copia el objeto `firebaseConfig` dentro de `static/app.js`.
5. **Reglas de Firestore** (pestaña *Reglas*): el navegador solo puede leer; únicamente el backend escribe.
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /resumenes/{id} {
         allow read: if true;
         allow write: if false;
       }
     }
   }
   ```

## Ejecución

Con Ollama corriendo (`ollama serve` si no se inició solo):

```bash
python app.py
```

Abre `http://localhost:5000`, selecciona un PDF y pulsa **Generar resumen**. El modelo corre en tu equipo, así que puede tardar entre 10 y 60 segundos.

## Prueba rápida del backend

```powershell
curl.exe -F "file=@tu_archivo.pdf" http://localhost:5000/upload
```

Respuesta esperada: `{"id": "..."}` con el ID del documento creado en Firestore.

## Limitaciones conocidas

- Solo funciona con PDFs que tengan **texto seleccionable**. Un PDF escaneado (solo imágenes) devuelve error, porque no hay OCR.
- Se procesan como máximo los primeros **12 000 caracteres** del documento (`MAX_CARACTERES` en `pdf_utils.py`), para no desbordar el contexto del modelo. En PDFs largos el resumen cubre solo el inicio.
- llama3.2 es un modelo pequeño y a veces se pasa un poco del límite de 250 palabras.

## Seguridad

- `serviceAccountKey.json` y `.venv/` están en `.gitignore`.
- El `firebaseConfig` del frontend es público por diseño; la protección de los datos la dan las reglas de Firestore.
- Si una clave privada se sube por error, hay que eliminarla en Google Cloud (IAM → Cuentas de servicio → Claves) y generar una nueva.

## Autor

Diego, estudiante de la Universidad Nacional de Colombia ([@diego-col-un](https://github.com/diego-col-un)).
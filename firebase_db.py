import firebase_admin
from firebase_admin import credentials, firestore

firebase_admin.initialize_app(credentials.Certificate("serviceAccountKey.json"))
db = firestore.client()

def guardar_resumen(nombre: str, resumen: str) -> str:
    _, ref = db.collection("resumenes").add({
        "nombre": nombre,
        "resumen": resumen,
        "creado": firestore.SERVER_TIMESTAMP,
    })
    return ref.id
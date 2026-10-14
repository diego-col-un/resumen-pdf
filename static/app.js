import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";

const firebaseConfig = {
   apiKey: "AIzaSyAzMuLGLw8i6ziRSxiS1JIAy9puslDCYLg",
  authDomain: "resumen-pdf-e6bfa.firebaseapp.com",
  databaseURL: "https://resumen-pdf-e6bfa-default-rtdb.firebaseio.com",
  projectId: "resumen-pdf-e6bfa",
  storageBucket: "resumen-pdf-e6bfa.firebasestorage.app",
  messagingSenderId: "401742110790",
  appId: "1:401742110790:web:4cd23f6f17c8f9b1226a47"
};
const db = getFirestore(initializeApp(firebaseConfig));

const form = document.getElementById("form");
const boton = document.getElementById("boton");
const estado = document.getElementById("estado");
const resultado = document.getElementById("resultado");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const archivo = document.getElementById("archivo").files[0];
  if (!archivo) return;

  const datos = new FormData();
  datos.append("file", archivo);

  boton.disabled = true;
  resultado.hidden = true;
  estado.textContent = "Procesando... el modelo puede tardar un minuto.";

  try {
    const resp = await fetch("/upload", { method: "POST", body: datos });
    const json = await resp.json();
    if (!resp.ok) throw new Error(json.error || "Error desconocido");

    const snap = await getDoc(doc(db, "resumenes", json.id));
    document.getElementById("titulo").textContent = snap.data().nombre;
    document.getElementById("texto").textContent = snap.data().resumen;
    resultado.hidden = false;
    estado.textContent = "";
  } catch (err) {
    estado.textContent = "Error: " + err.message;
  } finally {
    boton.disabled = false;
  }
});
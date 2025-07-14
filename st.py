import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from db import (
    crear_tabla_si_no_existe,
    guardar_interaccion,
    cargar_historial,
    borrar_historial
)

import random

def sugerencia_bienestar():
    opciones = [
        "🧘 Haz 3 respiraciones profundas con los ojos cerrados.",
        "📝 Escribe 3 cosas buenas que te pasaron hoy.",
        "🎵 Pon una canción que te guste y escúchala sin interrupciones.",
        "☀️ Sal a la calle y deja que el sol te dé en la cara por 5 minutos.",
        "📱 Apaga las notificaciones durante media hora.",
        "💧 Toma un vaso de agua con calma, y agradece ese momento.",
        "📖 Lee un párrafo de algo que te inspire.",
        "✋ Coloca la mano en el pecho y siente tu respiración por 60 segundos.",
        "🛌 Acuéstate un momento sin hacer nada y simplemente respira."
    ]
    return random.choice(opciones)


crear_tabla_si_no_existe()

st.set_page_config(page_title="Chatbot Motivacional Diario", page_icon="🌈")
st.title("🌈 Chatbot Motivacional Diario")
st.markdown("Marca tu estado de ánimo y recibe un mensaje motivador 💖")

# Selección de emoción
emocion = st.selectbox(
    "Selecciona tu estado emocional:",
    ["😃 Alegre", "😞 Triste", "😰 Ansioso", "😴 Cansado", "😠 Frustrado", "🤯 Saturado"]
)

# Texto adicional
detalle = st.text_area("¿Quieres añadir algo más?", placeholder="Es opcional")

# Envío
if st.button("Enviar"):
    mensaje_estado = f"{emocion} {detalle}"
    try:
        response = requests.post("http://localhost:5000/motivacion", json={"estado": mensaje_estado})
        if response.status_code == 200:
            mensaje = response.json()["respuesta"]
            st.success(f"✨ Tu mensaje motivacional:\n\n{mensaje}")
            # 💡 Sugerencia adicional
            st.markdown("💡 ¿Qué puedes hacer ahora?")
            st.info(sugerencia_bienestar())
            guardar_interaccion(mensaje_estado, mensaje)
        else:
            st.error("⚠️ Error al obtener la respuesta del modelo.")
    except Exception as e:
        st.error(f"💥 No se pudo conectar con el backend: {e}")

# 🧠 Historial emocional
st.divider()
st.subheader("📈 Frecuencia de emociones")

registros = cargar_historial()
df = pd.DataFrame(registros, columns=["fecha", "estado", "respuesta"])
df["fecha"] = pd.to_datetime(df["fecha"])

def extraer_emocion(texto):
    if "😃" in texto: return "Alegre"
    if "😞" in texto: return "Triste"
    if "😰" in texto: return "Ansioso"
    if "😴" in texto: return "Cansado"
    if "😠" in texto: return "Frustrado"
    if "🤯" in texto: return "Saturado"
    return "Otro"

df["emocion"] = df["estado"].apply(extraer_emocion)

fig = px.histogram(
    df,
    x="emocion",
    title="Estados emocionales registrados",
    color="emocion",
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig, use_container_width=True)

# 📚 Historial en columnas
st.subheader("🧠 Historial emocional detallado")

st.subheader("🧠 Historial emocional detallado")
for fecha, estado, respuesta in registros:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**🗓️ {fecha[:19]}**\n{estado}")
    with col2:
        st.markdown(f"_💬 {respuesta}_")
    st.markdown("---")

# 🗑️ Borrar historial
if st.button("🗑️ Borrar historial completo"):
    borrar_historial()
    st.success("✅ Historial borrado correctamente.")
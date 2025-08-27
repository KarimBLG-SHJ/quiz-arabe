import random
import streamlit as st
from gtts import gTTS
import base64

QUESTIONS = [
    {"ar": "انتهيت", "fr": "j’ai fini"},
    {"ar": "كتاب", "fr": "livre"},
    {"ar": "قلم", "fr": "stylo"},
]

st.title("📚 Quiz Arabe – Mode QCM")

# Choisir une question au hasard
q = random.choice(QUESTIONS)
ar, fr = q["ar"], q["fr"]

# Préparer l’audio
tts = gTTS(ar, lang="ar")
tts.save("mot.mp3")
with open("mot.mp3", "rb") as f:
    audio_bytes = f.read()
audio_b64 = base64.b64encode(audio_bytes).decode()

st.write("👉 Que signifie ce mot arabe ?")
st.markdown(f"<h1 style='font-size:70px;'>{ar}</h1>", unsafe_allow_html=True)
st.audio(audio_bytes, format="audio/mp3")

# Générer faux choix
faux = [fr + "e", "autre mot"]
choix = [fr] + faux
random.shuffle(choix)

reponse = st.radio("Choisis la traduction :", choix)

if st.button("Valider"):
    if reponse == fr:
        st.success("✅ Correct !")
    else:
        st.error(f"❌ Faux. La bonne réponse était : {fr}")

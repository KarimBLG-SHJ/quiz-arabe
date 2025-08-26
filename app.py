import streamlit as st
import random
from arabe import CATEGORIES, bonne_reponse

st.set_page_config(page_title="Quiz Arabe", page_icon="📚", layout="centered")

# ---------------------------
# ÉTAT PERSISTANT
# ---------------------------
if "started" not in st.session_state:
    st.session_state.started = False
if "questions" not in st.session_state:
    st.session_state.questions = []

# ---------------------------
# EN-TÊTE
# ---------------------------
st.title("📚 Quiz d’arabe – Cours 1→3")
st.markdown("**Choisis ta catégorie et teste tes connaissances !**")

# Choix de catégorie (actif même si le quiz est lancé)
categorie = st.selectbox("👉 Choisis une catégorie :", list(CATEGORIES.keys()) + ["Mix"])

def build_banque(cat: str):
    if cat == "Mix":
        # Concatène toutes les listes de questions
        banque = []
        for lst in CATEGORIES.values():
            banque.extend(lst)
        return banque
    return CATEGORIES[cat]

# ---------------------------
# BOUTON DE LANCEMENT
# ---------------------------
if st.button("🚀 Lancer le quiz", use_container_width=True):
    banque = build_banque(categorie)
    # Tire jusqu'à 10 questions (ou moins si la banque est petite)
    st.session_state.questions = random.sample(banque, min(10, len(banque)))
    st.session_state.started = True
    # Nettoie d'éventuelles anciennes réponses
    for i in range(1, len(st.session_state.questions) + 1):
        st.session_state.pop(f"rep{i}", None)
    st.rerun()  # relance pour afficher directement le quiz

# ---------------------------
# AFFICHAGE DU QUIZ
# ---------------------------
if st.session_state.started and st.session_state.questions:
    questions = st.session_state.questions
    total = len(questions)
    score = 0
    repondu = 0

    st.markdown("---")
    st.subheader("📝 Réponds aux questions :")
    progress = st.progress(0)

    for i, item in enumerate(questions, start=1):
        st.markdown(f"### ✏️ Question {i} : {item['q']}")
        # Un key unique par question pour mémoriser la saisie
        reponse = st.text_input(f"💬 Ta réponse {i}", key=f"rep{i}")

        if reponse:  # feedback immédiat quand quelque chose est saisi
            repondu += 1
            if bonne_reponse(reponse, item['a']):
                st.success("✅ Correct !")
                score += 1
            else:
                st.error(f"❌ Faux. La bonne réponse était : {item['a']}")

    # Barre de progression = nb de réponses remplies / total
    progress.progress(repondu / total if total else 0.0)

    st.markdown("---")
    if repondu == total:
        st.subheader(f"🎯 Résultat final : {score}/{total}")
    else:
        st.subheader(f"📈 Résultat provisoire : {score}/{total}")

    if score < 5:
        st.warning("👉 Pas terrible… continue les révisions !")
    elif score < 8:
        st.info("👉 Bravo, tu es sur la bonne voie !")
    else:
        st.success("🌟 Magnifique ! Tu progresses à vue d’œil 💫")

    # Bouton de reset
    if st.button("🔁 Recommencer"):
        for i in range(1, total + 1):
            st.session_state.pop(f"rep{i}", None)
        st.session_state.started = False
        st.session_state.questions = []
        st.rerun()

else:
    st.caption("Appuie sur « Lancer le quiz » pour commencer.")

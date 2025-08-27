# qcm.py
# Quiz en mode QCM (3 choix), sans saisie libre.

import random

# Mini-banque (on branchera avec arabe.py ensuite)
QUESTIONS = [
    {"ar": "انتهيت", "fr": "j’ai fini"},
    {"ar": "كتاب", "fr": "livre"},
    {"ar": "قلم", "fr": "stylo"},
]

def poser_qcm(q):
    ar = q["ar"]
    fr = q["fr"]

    # Faux choix "pièges"
    faux = [fr + "e", "autre mot"]
    choix = [fr] + faux
    random.shuffle(choix)

    print(f"\n👉 Que signifie : {ar} ?")
    for i, c in enumerate(choix, 1):
        print(f"{i}. {c}")

    rep = input("Ton choix (1-3): ").strip()
    if choix[int(rep)-1] == fr:
        print("✅ Correct !")
    else:
        print(f"❌ Faux. La bonne réponse était: {fr}")

def quiz():
    qs = random.sample(QUESTIONS, len(QUESTIONS))
    for q in qs:
        poser_qcm(q)

if __name__ == "__main__":
    quiz()

# arabe.py
# =====================
# Banque de vocabulaire + utilitaire de vérification

import re
import unicodedata

# --- Normalisation / comparaison tolérante ---
_ARABIC_DIACRITICS = re.compile(r"[\u064B-\u0652\u0670\u06D6-\u06ED]")  # tashkīl et signes Koran
_TATWEEL = "\u0640"

def _normalize_arabic(s: str) -> str:
    s = s.strip()
    # supprime tatweel + voyelles brèves
    s = s.replace(_TATWEEL, "")
    s = _ARABIC_DIACRITICS.sub("", s)
    # unifie quelques lettres
    s = (s.replace("أ", "ا")
           .replace("إ", "ا")
           .replace("آ", "ا")
           .replace("ؤ", "و")
           .replace("ئ", "ي")
           .replace("ى", "ي")
           .replace("ة", "ه"))  # on accepte "ه" pour "ة"
    # retire tout sauf lettres/ chiffres arabes
    s = re.sub(r"[^\u0600-\u06FF0-9]", "", s)
    return s

def _normalize_latin(s: str) -> str:
    # pour accepter une saisie au clavier latin (optionnel)
    s = s.strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

def bonne_reponse(user_input: str, attendu) -> bool:
    """
    Compare la saisie à la/aux réponse(s) attendue(s).
    - tolère les voyelles brèves/diacritiques
    - accepte variations (أ/ا/إ/آ, ة/ه, ى/ي, etc.)
    - accepte aussi une éventuelle translittération simple en lettres latines
    `attendu` peut être une chaîne ou une liste de chaînes.
    """
    if not user_input:
        return False

    candidats = attendu if isinstance(attendu, list) else [attendu]

    def norm_all(s: str) -> tuple[str, str]:
        # retourne (norm_arabe, norm_latin) pour élargir l'acceptation
        return _normalize_arabic(s), _normalize_latin(s)

    ui_ar, ui_lat = norm_all(user_input)
    for ans in candidats:
        ans_ar, ans_lat = norm_all(ans)
        if ui_ar and ui_ar == ans_ar:
            return True
        if ui_lat and ui_lat == ans_lat:
            return True
    return False

# --- BANQUE DE QUESTIONS (Cours 1, 2 et 3) ---
# Chaque item: {"q": "...", "a": "..." OU ["...", "..."]}

CATEGORIES = {
    # ====== COURS 1 : OBJETS & PHRASES DE CLASSE ======
    "Cours 1 – Objets de classe": [
        {"q": "Comment dit-on « livre » en arabe ?", "a": "كتاب"},
        {"q": "Comment dit-on « cahier » en arabe ?", "a": "دفتر"},
        {"q": "Comment dit-on « tableau (de classe) » en arabe ?", "a": "سبورة"},
        {"q": "Comment dit-on « stylo » en arabe ?", "a": "قلم"},
        {"q": "Que signifie en français « كتاب » ?", "a": "livre"},
        {"q": "Que signifie en français « قلم » ?", "a": ["stylo", "un stylo"]},
    ],
    "Cours 1 – Phrases utiles (classe)": [
        {"q": "Traduire en arabe : « Je ne comprends pas »", "a": "لا أفهم"},
        {"q": "Traduire en arabe : « Répète s’il te plaît »", "a": "مرة أخرى"},
        {"q": "Traduire en arabe : « J’ai fini »", "a": "انتهيت"},
        {"q": "Traduire en arabe : « Comment t’appelles-tu ? »", "a": "ما اسمك"},
        {"q": "Traduire en arabe : « Quel âge as-tu ? »", "a": "كم عمرك"},
        {"q": "Traduire en arabe : « Es-tu marié ? »", "a": "هل أنت متزوج"},
        {"q": "Que signifie en français « نعم، فهمت » ?", "a": ["oui j’ai compris", "oui, j’ai compris", "j’ai compris"]},
        {"q": "Que signifie en français « مفهوم » ?", "a": ["c’est compris", "compris"]},
    ],
    "Cours 1 – Sons & notions": [
        {"q": "Quelle voyelle brève correspond à « ـَ » ?", "a": ["a", "fatha", "fatha a", "fatḥa"]},
        {"q": "Quelle voyelle brève correspond à « ـِ » ?", "a": ["i", "kasra", "kasra i"]},
        {"q": "Quelle voyelle brève correspond à « ـُ » ?", "a": ["u", "ou", "damma", "ḍamma"]},
        {"q": "Voyelle longue : quelle lettre donne le son « ā » ?", "a": ["ا", "alif"]},
        {"q": "Voyelle longue : quelle lettre donne le son « ū » ?", "a": ["و", "waw"]},
        {"q": "Voyelle longue : quelle lettre donne le son « ī » ?", "a": ["ي", "ya", "yaa"]},
        {"q": "Traduire en arabe : « au début »", "a": "في البداية"},
        {"q": "Traduire en arabe : « au milieu »", "a": "في الوسط"},
        {"q": "Traduire en arabe : « à la fin »", "a": "في النهاية"},
        {"q": "Que signifie en français « جملة » ?", "a": ["phrase", "une phrase"]},
        {"q": "Que signifie en français « كلمة » ?", "a": ["mot", "un mot"]},
        {"q": "Que signifie en français « حرف » ?", "a": ["lettre", "une lettre"]},
        {"q": "Dans « الشمس », la lettre initiale est… (solaire/lunaire) ?", "a": ["solaire", "lettre solaire", "shamsiya", "shamsiyya"]},
        {"q": "Dans « القمر », la lettre initiale est… (solaire/lunaire) ?", "a": ["lunaire", "lettre lunaire", "qamariya", "qamariyya"]},
    ],

    # ====== COURS 2 : FAMILLE & MÉTIERS ======
    "Cours 2 – Famille": [
        {"q": "Comment dit-on « père » en arabe ?", "a": "أب"},
        {"q": "Comment dit-on « mère » en arabe ?", "a": "أم"},
        {"q": "Comment dit-on « frère » en arabe ?", "a": "أخ"},
        {"q": "Comment dit-on « sœur » en arabe ?", "a": ["أخت", "اخت"]},
        {"q": "Comment dit-on « fils » en arabe ?", "a": "ابن"},
        {"q": "Comment dit-on « fille (enfant) » en arabe ?", "a": "بنت"},
        {"q": "Comment dit-on « grand-père » en arabe ?", "a": "جد"},
        {"q": "Comment dit-on « grand-mère » en arabe ?", "a": "جدة"},
        {"q": "Que signifie « هذا أبي » en français ?", "a": ["c’est mon père", "voici mon père", "ceci est mon père"]},
        {"q": "Que signifie « هذه أمي » en français ?", "a": ["c’est ma mère", "voici ma mère", "ceci est ma mère"]},
        {"q": "Que signifie « أنا أحب أسرتي » en français ?", "a": ["j’aime ma famille", "j aime ma famille"]},
    ],
    "Cours 2 – Métiers": [
        {"q": "Comment dit-on « professeur (masc.) » en arabe ?", "a": "مدرس"},
        {"q": "Comment dit-on « médecin (m/f) » en arabe ?", "a": ["طبيب", "طبيبة"]},
        {"q": "Comment dit-on « ingénieur » en arabe ?", "a": "مهندس"},
        {"q": "Comment dit-on « chauffeur » en arabe ?", "a": "سائق"},
        {"q": "Comment dit-on « directeur / gérant » en arabe ?", "a": "مدير"},
        {"q": "Comment dit-on « infirmier » en arabe ?", "a": "ممرض"},
        {"q": "Comment dit-on « agriculteur » en arabe ?", "a": "مزارع"},
        {"q": "Comment dit-on « étudiant » en arabe ?", "a": "طالب"},
    ],

    # ====== COURS 3 : FRUITS & LÉGUMES ======
    "Cours 3 – Fruits & Légumes": [
        {"q": "Comment dit-on « pomme » en arabe ?", "a": "تفاح"},
        {"q": "Comment dit-on « banane » en arabe ?", "a": "موز"},
        {"q": "Comment dit-on « orange » en arabe ?", "a": "برتقال"},
        {"q": "Comment dit-on « fraise » en arabe ?", "a": ["فراولة", "فراوله"]},
        {"q": "Comment dit-on « raisin » en arabe ?", "a": "عنب"},
        {"q": "Comment dit-on « grenade (fruit) » en arabe ?", "a": "رمان"},
        {"q": "Comment dit-on « pastèque » en arabe ?", "a": "بطيخ"},
        {"q": "Comment dit-on « melon » en arabe ?", "a": "شمام"},
        {"q": "Comment dit-on « tomate » en arabe ?", "a": ["طماطم", "بندورة"]},
        {"q": "Comment dit-on « concombre » en arabe ?", "a": "خيار"},
        {"q": "Comment dit-on « carotte » en arabe ?", "a": "جزر"},
        {"q": "Que signifie en français « خيار » ?", "a": "concombre"},
        {"q": "Que signifie en français « رمان » ?", "a": "grenade"},
    ],
}

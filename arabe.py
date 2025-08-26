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

# --- BANQUE DE QUESTIONS ---
# Chaque item: {"q": "...", "a": "..." OU ["...", "..."]}

CATEGORIES = {
    # ====== FRUITS ======
    "Bases – Fruits": [
        {"q": "Comment dit-on « pomme » en arabe ?", "a": "تفاح"},
        {"q": "Comment dit-on « banane » en arabe ?", "a": "موز"},
        {"q": "Comment dit-on « orange » en arabe ?", "a": "برتقال"},
        {"q": "Comment dit-on « citron » en arabe ?", "a": "ليمون"},
        {"q": "Comment dit-on « fraise » en arabe ?", "a": ["فراولة", "فريز"]},
        {"q": "Comment dit-on « raisin » en arabe ?", "a": "عنب"},
        {"q": "Comment dit-on « pastèque » en arabe ?", "a": "بطيخ"},
        {"q": "Comment dit-on « melon » en arabe ?", "a": "شمام"},
        {"q": "Comment dit-on « ananas » en arabe ?", "a": "أناناس"},
        {"q": "Comment dit-on « pêche » en arabe ?", "a": "خوخ"},
        {"q": "Comment dit-on « poire » en arabe ?", "a": ["إجاص", "كمثرى"]},
        {"q": "Comment dit-on « mangue » en arabe ?", "a": "مانجو"},
        {"q": "Comment dit-on « cerise » en arabe ?", "a": "كرز"},
    ],

    # ====== LÉGUMES ======
    "Bases – Légumes": [
        {"q": "Comment dit-on « tomate » en arabe ?", "a": ["طماطم", "بندورة"]},
        {"q": "Comment dit-on « concombre » en arabe ?", "a": "خيار"},
        {"q": "Comment dit-on « carotte » en arabe ?", "a": "جزر"},
        {"q": "Comment dit-on « pomme de terre » en arabe ?", "a": "بطاطا"},
        {"q": "Comment dit-on « oignon » en arabe ?", "a": "بصل"},
        {"q": "Comment dit-on « ail » en arabe ?", "a": "ثوم"},
        {"q": "Comment dit-on « salade / laitue » en arabe ?", "a": "خس"},
        {"q": "Comment dit-on « aubergine » en arabe ?", "a": "باذنجان"},
        {"q": "Comment dit-on « poivron » en arabe ?", "a": "فلفل"},
        {"q": "Comment dit-on « épinards » en arabe ?", "a": "سبانخ"},
    ],

    # ====== COULEURS ======
    "Bases – Couleurs": [
        {"q": "Comment dit-on « blanc » en arabe ?", "a": "أبيض"},
        {"q": "Comment dit-on « noir » en arabe ?", "a": "أسود"},
        {"q": "Comment dit-on « rouge » en arabe ?", "a": "أحمر"},
        {"q": "Comment dit-on « bleu » en arabe ?", "a": "أزرق"},
        {"q": "Comment dit-on « vert » en arabe ?", "a": "أخضر"},
        {"q": "Comment dit-on « jaune » en arabe ?", "a": "أصفر"},
        {"q": "Comment dit-on « orange (couleur) » en arabe ?", "a": "برتقالي"},
        {"q": "Comment dit-on « rose » en arabe ?", "a": "وردي"},
        {"q": "Comment dit-on « violet / pourpre » en arabe ?", "a": "بنفسجي"},
        {"q": "Comment dit-on « marron / brun » en arabe ?", "a": "بني"},
        {"q": "Comment dit-on « gris » en arabe ?", "a": "رمادي"},
    ],

    # ====== NOMBRES ======
    "Bases – Nombres 0→10": [
        {"q": "Comment dit-on « zéro » en arabe ?", "a": "صفر"},
        {"q": "Comment dit-on « un » en arabe ?", "a": "واحد"},
        {"q": "Comment dit-on « deux » en arabe ?", "a": ["اثنان", "إثنان", "اتنين"]},
        {"q": "Comment dit-on « trois » en arabe ?", "a": "ثلاثة"},
        {"q": "Comment dit-on « quatre » en arabe ?", "a": "أربعة"},
        {"q": "Comment dit-on « cinq » en arabe ?", "a": "خمسة"},
        {"q": "Comment dit-on « six » en arabe ?", "a": "ستة"},
        {"q": "Comment dit-on « sept » en arabe ?", "a": "سبعة"},
        {"q": "Comment dit-on « huit » en arabe ?", "a": "ثمانية"},
        {"q": "Comment dit-on « neuf » en arabe ?", "a": "تسعة"},
        {"q": "Comment dit-on « dix » en arabe ?", "a": "عشرة"},
    ],

    # ====== JOURS ======
    "Bases – Jours de la semaine": [
        {"q": "Comment dit-on « samedi » en arabe ?", "a": "السبت"},
        {"q": "Comment dit-on « dimanche » en arabe ?", "a": "الأحد"},
        {"q": "Comment dit-on « lundi » en arabe ?", "a": "الاثنين"},
        {"q": "Comment dit-on « mardi » en arabe ?", "a": "الثلاثاء"},
        {"q": "Comment dit-on « mercredi » en arabe ?", "a": "الأربعاء"},
        {"q": "Comment dit-on « jeudi » en arabe ?", "a": "الخميس"},
        {"q": "Comment dit-on « vendredi » en arabe ?", "a": "الجمعة"},
    ],

    # ====== FAMILLE ======
    "Bases – Famille": [
        {"q": "Comment dit-on « mère » en arabe ?", "a": "أم"},
        {"q": "Comment dit-on « père » en arabe ?", "a": "أب"},
        {"q": "Comment dit-on « fils » en arabe ?", "a": "ابن"},
        {"q": "Comment dit-on « fille (enfant) » en arabe ?", "a": "ابنة"},
        {"q": "Comment dit-on « frère » en arabe ?", "a": "أخ"},
        {"q": "Comment dit-on « sœur » en arabe ?", "a": "أخت"},
        {"q": "Comment dit-on « grand-père » en arabe ?", "a": "جد"},
        {"q": "Comment dit-on « grand-mère » en arabe ?", "a": "جدة"},
        {"q": "Comment dit-on « oncle (paternel/maternel) » en arabe ?", "a": ["عم", "خال"]},
        {"q": "Comment dit-on « tante (paternelle/maternelle) » en arabe ?", "a": ["عمة", "خالة"]},
    ],

    # ====== PRONOMS ======
    "Bases – Pronoms": [
        {"q": "Comment dit-on « je » en arabe ?", "a": "أنا"},
        {"q": "Comment dit-on « tu (masc.) » en arabe ?", "a": "أنتَ"},
        {"q": "Comment dit-on « tu (fém.) » en arabe ?", "a": "أنتِ"},
        {"q": "Comment dit-on « il » en arabe ?", "a": "هو"},
        {"q": "Comment dit-on « elle » en arabe ?", "a": "هي"},
        {"q": "Comment dit-on « nous » en arabe ?", "a": "نحن"},
        {"q": "Comment dit-on « vous » en arabe ?", "a": "أنتم"},
        {"q": "Comment dit-on « ils/elles » en arabe ?", "a": "هم"},
    ],

    # ====== ANIMAUX ======
    "Bases – Animaux": [
        {"q": "Comment dit-on « chat » en arabe ?", "a": ["قط", "قطة"]},
        {"q": "Comment dit-on « chien » en arabe ?", "a": "كلب"},
        {"q": "Comment dit-on « oiseau » en arabe ?", "a": "طائر"},
        {"q": "Comment dit-on « cheval » en arabe ?", "a": "حصان"},
        {"q": "Comment dit-on « vache » en arabe ?", "a": "بقرة"},
        {"q": "Comment dit-on « mouton » en arabe ?", "a": "خروف"},
        {"q": "Comment dit-on « poisson » en arabe ?", "a": "سمك"},
        {"q": "Comment dit-on « chameau » en arabe ?", "a": "جمل"},
        {"q": "Comment dit-on « lapin » en arabe ?", "a": "أرنب"},
        {"q": "Comment dit-on « lion » en arabe ?", "a": "أسد"},
    ],

    # ====== VERBES DE BASE (présent) ======
    "Bases – Verbes (présent)": [
        {"q": "Comment dit-on « je mange » en arabe standard ?", "a": "أنا آكل"},
        {"q": "Comment dit-on « je bois » en arabe standard ?", "a": "أنا أشرب"},
        {"q": "Comment dit-on « je vais » en arabe standard ?", "a": "أنا أذهب"},
        {"q": "Comment dit-on « je veux » en arabe standard ?", "a": "أنا أريد"},
        {"q": "Comment dit-on « je comprends » en arabe standard ?", "a": "أنا أفهم"},
        {"q": "Comment dit-on « je lis » en arabe standard ?", "a": "أنا أقرأ"},
        {"q": "Comment dit-on « je parle » en arabe standard ?", "a": "أنا أتحدث"},
        {"q": "Comment dit-on « je travaille » en arabe standard ?", "a": "أنا أعمل"},
        {"q": "Comment dit-on « j’étudie » en arabe standard ?", "a": "أنا أدرس"},
        {"q": "Comment dit-on « j’habite à… » en arabe standard ?", "a": "أنا أسكن"},
    ],
}

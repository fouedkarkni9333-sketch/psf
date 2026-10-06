from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)

TRANSLATIONS = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "PSF - الملاذ الآمن",
        "subtitle": "الملاذ الآمن للفضول والهدوء اللامتناهي",
        "next_btn": "اكتشف التالي",
        "share_btn": "نسخ",
        "copied": "تم نسخ النص بنجاح!",
        "settings": "الإعدادات واللغات",
        "cats": {"all": "الكل", "calm": "تأملات", "curiosity": "فضول", "wisdom": "حكم", "mystery": "أسرار"},
        "messages": [
            "الهدوء الحقيقي يبدأ عندما تتوقف عن البحث وتترك العقل يتنفس.",
            "توقف لثانية... ودع صخب العالم يختفي خلف هذه الشاشة.",
            "ما هي الفكرة الصغيرة التي تنتظر أن تكتشفها اليوم وتغير مجرى تفكيرك؟",
            "الكلمة الطيبة في الوقت المناسب تساوي عمراً كاملاً من الطمأنينة."
        ]
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "PSF - Safe Haven",
        "subtitle": "The safe haven for endless curiosity and peace",
        "next_btn": "Discover Next",
        "share_btn": "Copy",
        "copied": "Text copied successfully!",
        "settings": "Settings & Languages",
        "cats": {"all": "All", "calm": "Calm", "curiosity": "Curiosity", "wisdom": "Wisdom", "mystery": "Mystery"},
        "messages": [
            "True calm begins when you stop searching and let your mind breathe.",
            "Pause for a second... and let the noise of the world fade behind this screen.",
            "What small idea is waiting to be discovered by you today?",
            "A kind word at the right time is worth a lifetime of peace."
        ]
    },
    "fr": {
        "name": "Français",
        "dir": "ltr",
        "title": "PSF - Haven Sûr",
        "subtitle": "Le havre de paix pour la curiosité infinie",
        "next_btn": "Découvrir Suivant",
        "share_btn": "Copier",
        "copied": "Texte copié avec succès !",
        "settings": "Paramètres et Langues",
        "cats": {"all": "Tout", "calm": "Calme", "curiosity": "Curiosité", "wisdom": "Sagesse", "mystery": "Mystère"},
        "messages": [
            "Le vrai calme commence lorsque vous arrêtez de chercher.",
            "Faites une pause... et laissez le bruit du monde s'effacer.",
            "Quelle petite idée attend d'être découverte par vous aujourd'hui ?",
            "Un mot gentil au bon moment vaut une vie de sérénité."
        ]
    },
    "es": {
        "name": "Español",
        "dir": "ltr",
        "title": "PSF - Refugio Seguro",
        "subtitle": "El refugio seguro para la curiosidad infinita",
        "next_btn": "Descubrir Siguiente",
        "share_btn": "Copiar",
        "copied": "¡Texto copiado con éxito!",
        "settings": "Ajustes e Idiomas",
        "cats": {"all": "Todo", "calm": "Calma", "curiosity": "Curiosidad", "wisdom": "Sabiduría", "mystery": "Misterio"},
        "messages": [
            "La verdadera calma comienza cuando dejas de buscar.",
            "Detente un segundo... y deja que el ruido del mundo desaparezca.",
            "¿Qué pequeña idea espera ser descubierta por ti hoy?",
            "Una palabra amable en el momento adecuado vale toda una vida."
        ]
    },
    "de": {
        "name": "Deutsch",
        "dir": "ltr",
        "title": "PSF - Zufluchtsort",
        "subtitle": "Der sichere Hafen für endlose Neugier und Ruhe",
        "next_btn": "Nächstes entdecken",
        "share_btn": "Kopieren",
        "copied": "Text erfolgreich kopiert!",
        "settings": "Einstellungen & Sprachen",
        "cats": {"all": "Alle", "calm": "Ruhe", "curiosity": "Neugier", "wisdom": "Weisheit", "mystery": "Mysterium"},
        "messages": [
            "Wahre Ruhe beginnt, wenn man aufhört zu suchen.",
            "Haltet kurz inne... und lasst den Lärm der Welt verblassen.",
            "Welche kleine Idee wartet darauf, von Ihnen entdeckt zu werden?"
        ]
    },
    "it": {
        "name": "Italiano",
        "dir": "ltr",
        "title": "PSF - Rifugio",
        "subtitle": "Il rifugio sicuro per curiosità e pace",
        "next_btn": "Scopri il Prossimo",
        "share_btn": "Copia",
        "copied": "Testo copiato con successo!",
        "settings": "Impostazioni",
        "cats": {"all": "Tutti", "calm": "Calma", "curiosity": "Curiosità", "wisdom": "Saggezza", "mystery": "Mistero"},
        "messages": [
            "La vera calma inizia quando smetti di cercare.",
            "Fermati un secondo... e lascia che il rumore del mondo svanisca."
        ]
    },
    "tr": {
        "name": "Türkçe",
        "dir": "ltr",
        "title": "PSF - Sığınak",
        "subtitle": "Sonsuz merak ve huzur için güvenli sığınak",
        "next_btn": "Sonrakini Keşfet",
        "share_btn": "Kopyala",
        "copied": "Metin başarıyla kopyalandı!",
        "settings": "Ayarlar",
        "cats": {"all": "Tümü", "calm": "Sakinlik", "curiosity": "Merak", "wisdom": "Bilgelik", "mystery": "Gizem"},
        "messages": [
            "Gerçek sakinlik aramayı bıraktığında başlar.",
            "Bir saniye dur... ve dünyanın gürültüsünün kaybolmasına izin ver."
        ]
    },
    "ar-TN": {
        "name": "تونسية (Tunisian)",
        "dir": "rtl",
        "title": "PSF - البلاصة الآمنة",
        "subtitle": "الاستراحة الهادئة للفضول والروقان",
        "next_btn": "اكتشف الجاي",
        "share_btn": "نسخ",
        "copied": "تم النسخ بنجاح!",
        "settings": "الإعدادات واللغات",
        "cats": {"all": "الكل", "calm": "روقان", "curiosity": "فضول", "wisdom": "حكم", "mystery": "أسرار"},
        "messages": [
            "الروقان الحقيقي يبدأ كيف تبطل تحوس وتخلي عقلك يرتاح.",
            "اقفز بثانية... وخلي دوشة الدنيا الكل تتخبى وراء هاليزران.",
            "أشنوه الفكرة الصغيرة اللي تستنى فيك اليوم باش تبدل مخك؟",
            "كلمة طيبة في وقتها تسوى الدنيا وماحوي."
        ]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang_code }}" dir="{{ lang_dir }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.title }}</title>
    <style>
        body {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
            padding: 20px;
        }
        .header-bar {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .menu-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            font-size: 1.3rem;
            padding: 8px 14px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .menu-btn:hover { background: #30363d; color: white; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 25px;
            border-radius: 20px

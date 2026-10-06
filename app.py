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
            "Haltet kurz inne... und lasst den Lärm der Welt verblassen."
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

HTML_PART_1 = """<!DOCTYPE html>
<html lang="""

HTML_PART_2 = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""

HTML_PART_3 = """</title>
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
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
            max-height: 80vh;
            overflow-y: auto;
            text-align: center;
        }
        .modal-content h3 { color: #58a6ff; margin-top: 0; }
        .lang-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        .lang-option {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            padding: 10px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }
        .lang-option:hover, .lang-option.active {
            background: #1f6feb;
            color: white;
            border-color: #388bfd;
        }
        .close-modal {
            margin-top: 20px;
            background: #30363d;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 10px;
            cursor: pointer;
        }

        .container {
            text-align: center;
            padding: 20px;
            max-width: 500px;
            width: 100%;
        }
        .logo {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: #58a6ff;
            margin-bottom: 0;
            text-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
        }
        .subtitle {
            color: #8b949e;
            font-size: 0.95rem;
            margin-bottom: 20px;
        }
        .categories {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .cat-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 6px 12px;
            font-size: 0.85rem;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .cat-btn.active, .cat-btn:hover {
            background: #1f6feb;
            color: white;
            border-color: #388bfd;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 35px 25px;
            border-radius: 20px;
            margin-bottom: 25px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        #mystery-text {
            font-size: 1.25rem;
            color: #f0f6fc;
            line-height: 1.7;
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        .actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }
        .pulse-btn {
            background: linear-gradient(135deg, #1f6feb, #388bfd);
            color: white;
            border: none;
            padding: 14px 30px;
            font-size: 1.05rem;
            border-radius: 35px;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(31, 111, 235, 0.4);
            transition: all 0.3s ease;
            font-weight: bold;
            flex: 2;
        }
        .pulse-btn:hover { transform: scale(1.03); }
        .share-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            padding: 14px 20px;
            font-size: 0.95rem;
            border-radius: 35px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
        }
        .share-btn:hover { background: #30363d; color: white; }
        .toast {
            margin-top: 15px;
            font-size: 0.85rem;
            color: #3fb950;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="header-bar">
        <button class="menu-btn" onclick="openSettings()">⚙️ ≡</button>
    </div>

    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <h3>"""

HTML_PART_4 = """</h3>
            <div class="lang-grid">
                {% for code, data in languages.items() %}
                <div class="lang-option {% if code == lang_code %}active{% endif %}" onclick="changeLang('{{ code }}')">
                    {{ data.name }}
                </div>
                {% endfor %}
            </div>
            <button class="close-modal" onclick="closeSettings()">✕</button>
        </div>
    </div>

    <div class="container">
        <div class="logo">PSF</div>
        <div class="subtitle">"""

HTML_PART_5 = """</div>
        
        <div class="categories">
            <button class="cat-btn active" onclick="setCategory('all', this)">"""

HTML_PART_6 = """</button>
            <button class="cat-btn" onclick="setCategory('calm', this)">"""

HTML_PART_7 = """</button>
            <button class="cat-btn" onclick="setCategory('curiosity', this)">"""

HTML_PART_8 = """</button>
            <button class="cat-btn" onclick="setCategory('wisdom', this)">"""

HTML_PART_9 = """</button>
            <button class="cat-btn" onclick="setCategory('mystery', this)">"""

HTML_PART_10 = """</button>
        </div>

        <div class="card" id="card-box">
            <div id="mystery-text">"""

HTML_PART_11 = """</div>
        </div>

        <div class="actions">
            <button class="pulse-btn" onclick="fetchNext()">"""

HTML_PART_12 = """</button>
            <button class="share-btn" onclick="shareText()">"""

HTML_PART_13 = """</button>
        </div>
        <div id="toast" class="toast">"""

HTML_PART_14 = """</div>
    </div>

    <script>
        let currentCategory = 'all';
        let currentLang = '"""

HTML_PART_15 = """';

        function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
        function closeSettings() { document.getElementById('settingsModal').style.display = 'none'; }
        
        function changeLang(lang) {
            window.location.href = `/?lang=${lang}`;
        }

        function setCategory(category, btn) {
            currentCategory = category;
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            fetchNext();
        }

        function fetchNext() {
            const textElem = document.getElementById('mystery-text');
            textElem.style.opacity = '0';
            textElem.style.transform = 'translateY(10px)';
            
            fetch(`/next?cat=${currentCategory}&lang=${currentLang}`)
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        textElem.innerText = data.message;
                        textElem.style.opacity = '1';
                        textElem.style.transform = 'translateY(0)';
                    }, 200);
                });
        }

        function shareText() {
            const text = document.getElementById('mystery-text').innerText;
            navigator.clipboard.writeText(text + " \\n- PSF").then(() => {
                const toast = document.getElementById('toast');
                toast.style.opacity = '1';
                setTimeout(() => { toast.style.opacity = '0'; }, 2000);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    lang = request.args.get('lang', 'ar')
    if lang not in TRANSLATIONS:
        lang = 'ar'
    
    t = TRANSLATIONS[lang]
    msgs = t.get("messages", TRANSLATIONS["ar"]["messages"])
    
    full_html = (
        HTML_PART_1 + f'"{lang}" dir="{t["dir"]}"' +
        HTML_PART_2 + t["title"] +
        HTML_PART_3 + t["settings"] +
        HTML_PART_4 + t["subtitle"] +
        HTML_PART_5 + t["cats"]["all"] +
        HTML_PART_6 + t["cats"]["calm"] +
        HTML_PART_7 + t["cats"]["curiosity"] +
        HTML_PART_8 + t["cats"]["wisdom"] +
        HTML_PART_9 + t["cats"]["mystery"] +
        HTML_PART_10 + random.choice(msgs) +
        HTML_PART_11 + t["next_btn"] +
        HTML_PART_12 + t["share_btn"] +
        HTML_PART_13 + t["copied"] +
        HTML_PART_14 + lang +
        HTML_PART_15
    )
    
    return render_template_string(full_html, languages=TRANSLATIONS, lang_code=lang)

@app.route("/next")
def next_message():
    lang = request.args.get('lang', 'ar')
    if lang not in TRANSLATIONS:
        lang = 'ar'
        
    t = TRANSLATIONS[lang]
    messages = t.get("messages", TRANSLATIONS["ar"]["messages"])
        
    return jsonify({"message": random.choice(messages)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

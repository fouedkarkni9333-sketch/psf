from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)

# قاعدة بيانات مهيكلة بالكامل بالعربية الفصحى لتطبيق PSF
PSF_DB = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "PSF - الملاذ الآمن",
        "subtitle": "الملاذ الآمن للفضول والهدوء اللامتناهي",
        "next_btn": "اكتشف التالي ✨",
        "share_btn": "نسخ",
        "copied": "تم نسخ النص بنجاح!",
        "settings": "الإعدادات واللغات",
        "cats": {
            "all": "الكل", 
            "calm": "تأملات هادئة", 
            "curiosity": "عالم الفضول", 
            "wisdom": "حكم وأعماق", 
            "mystery": "أسرار الخفاء"
        },
        "messages": {
            "calm": [
                "الهدوء الحقيقي يبدأ عندما تتوقف عن البحث وتترك العقل يتنفس بسلام.",
                "توقف لثانية واحدة... ودع صخب العالم يختفي خلف هذه الشاشة بهدوء تام.",
                "أحياناً يكون الصمت أبلغ رد على تفاصيل الحياة المتسارعة.",
                "السكينة ليست عدم وجود الضجيج، بل هي السلام وسط الصخب."
            ],
            "curiosity": [
                "ما هي الفكرة الصغيرة التي تنتظر أن تكتشفها اليوم لتغير مجرى تفكيرك بالكامل؟",
                "ما تخفيه اللحظة القادمة قد يكون هو الإجابة الدقيقة التي بحثت عنها طويلاً.",
                "العقل البشري يبتكر أسراراً مذهلة عندما يُمنح مساحة كافية للتأمل الفردي.",
                "خلف كل سؤال بسيط، عالم متكامل من الحقائق التي تنتظر من يكتشفها."
            ],
            "wisdom": [
                "الكلمة الطيبة في الوقت المناسب تساوي عمراً كاملاً من الطمأنينة واليقين.",
                "من أمعن النظر في عواقب الأمور، سلم من عثرات البدايات.",
                "الأيام تذهب ولا تعود، فاجعل لخطاك أثراً جميلاً يخلده الزمن.",
                "الحكمة الحقيقية أن تعلم متى تتحدث ومتى يكون الصمت هو البلاغة كلها."
            ],
            "mystery": [
                "خلف كل كبسة زر، سر جديد وخاص ينتظر أن يتم الكشف عنه الآن.",
                "هناك دائماً زوايا خفية في هذا الكون لم تصل إليها أفكارك بعد.",
                "التجارب الغامضة تصنع العقول العظيمة التي لا تشبه الآخرين.",
                "استعد لما هو غير متوقع، فالصفحة التالية تحمل طابعاً فريداً."
            ]
        }
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "PSF - Safe Haven",
        "subtitle": "The safe haven for endless curiosity and peace",
        "next_btn": "Discover Next ✨",
        "share_btn": "Copy",
        "copied": "Text copied successfully!",
        "settings": "Settings & Languages",
        "cats": {
            "all": "All", 
            "calm": "Calm", 
            "curiosity": "Curiosity", 
            "wisdom": "Wisdom", 
            "mystery": "Mystery"
        },
        "messages": {
            "calm": [
                "True calm begins when you stop searching and let your mind breathe.",
                "Pause for a second... and let the noise of the world fade behind this screen."
            ],
            "curiosity": [
                "What small idea is waiting to be discovered by you today?",
                "What the next moment hides might be the exact answer you sought."
            ],
            "wisdom": [
                "A kind word at the right time is worth a lifetime of peace."
            ],
            "mystery": [
                "Every tap unlocks a completely new dimension of surprise."
            ]
        }
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
            background-color: #080c14;
            color: #f3f4f6;
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
            justify-content: flex-end;
            align-items: center;
        }
        .menu-btn {
            background: #111827;
            border: 1px solid #1f2937;
            color: #60a5fa;
            font-size: 1.2rem;
            padding: 10px 16px;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .menu-btn:hover { background: #1f2937; transform: scale(1.05); color: #fff; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            justify-content: center;
            align-items: center;
            z-index: 1000;
            backdrop-filter: blur(8px);
        }
        .modal-content {
            background: #111827;
            border: 1px solid #1f2937;
            padding: 30px;
            border-radius: 24px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 15px 50px rgba(0,0,0,0.9);
        }
        .modal-content h3 { color: #60a5fa; margin-top: 0; font-size: 1.3rem; }
        .lang-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-top: 20px;
        }
        .lang-option {
            background: #1f2937;
            border: 1px solid #374151;
            color: #d1d5db;
            padding: 12px;
            border-radius: 14px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.2s;
        }
        .lang-option:hover, .lang-option.active {
            background: #2563eb;
            color: white;
            border-color: #60a5fa;
        }
        .close-modal {
            margin-top: 20px;
            background: #374151;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .close-modal:hover { background: #4b5563; }

        .container {
            text-align: center;
            padding: 20px;
            max-width: 520px;
            width: 100%;
        }
        .logo {
            font-size: 3.8rem;
            font-weight: 900;
            letter-spacing: 4px;
            background: linear-gradient(135deg, #60a5fa, #3b82f6, #93c5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
            text-shadow: 0 0 35px rgba(59, 130, 246, 0.4);
        }
        .subtitle {
            color: #9ca3af;
            font-size: 0.95rem;
            margin-bottom: 25px;
            letter-spacing: 0.5px;
        }
        .categories {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }
        .cat-btn {
            background: #111827;
            border: 1px solid #1f2937;
            color: #9ca3af;
            padding: 8px 16px;
            font-size: 0.85rem;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .cat-btn.active, .cat-btn:hover {
            background: #2563eb;
            color: white;
            border-color: #60a5fa;
            box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
            transform: translateY(-2px);
        }
        .card {
            background: #111827;
            border: 1px solid #1f2937;
            padding: 45px 30px;
            border-radius: 28px;
            margin-bottom: 25px;
            box-shadow: 0 15px 45px rgba(0,0,0,0.8);
            min-height: 130px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        .card::after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 28px;
            border: 1px solid rgba(96, 165, 250, 0.08);
            pointer-events: none;
        }
        #mystery-text {
            font-size: 1.3rem;
            color: #f9fafb;
            line-height: 1.8;
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.35s ease, transform 0.35s ease;
        }
        .actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }
        .pulse-btn {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border: none;
            padding: 16px 36px;
            font-size: 1.15rem;
            border-radius: 40px;
            cursor: pointer;
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: bold;
            flex: 2;
        }
        .pulse-btn:hover { 
            transform: translateY(-3px) scale(1.02); 
            box-shadow: 0 12px 35px rgba(37, 99, 235, 0.8); 
        }
        .share-btn {
            background: #111827;
            border: 1px solid #1f2937;
            color: #e5e7eb;
            padding: 16px 24px;
            font-size: 1rem;
            border-radius: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
        }
        .share-btn:hover { background: #1f2937; color: white; border-color: #4b5563; }
        .toast {
            margin-top: 15px;
            font-size: 0.9rem;
            color: #4ade80;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="header-bar">
        <button class="menu-btn" onclick="openSettings()">⚙️ ≡</button>
    </div>

    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <h3>{{ t.settings }}</h3>
            <div class="lang-grid">
                {% for code, data in languages.items() %}
                <div class="lang-option {% if code == lang_code %}active{% endif %}" onclick="changeLang('{{ code }}')">
                    {{ data.name }}
                </div>
                {% endfor %}
            </div>
            <button class="close-modal" onclick="closeSettings()">إغلاق</button>
        </div>
    </div>

    <div class="container">
        <div class="logo">PSF</div>
        <div class="subtitle">{{ t.subtitle }}</div>
        
        <div class="categories">
            <button class="cat-btn active" onclick="setCategory('all', this)">{{ t.cats.all }}</button>
            <button class="cat-btn" onclick="setCategory('calm', this)">{{ t.cats.calm }}</button>
            <button class="cat-btn" onclick="setCategory('curiosity', this)">{{ t.cats.curiosity }}</button>
            <button class="cat-btn" onclick="setCategory('wisdom', this)">{{ t.cats.wisdom }}</button>
            <button class="cat-btn" onclick="setCategory('mystery', this)">{{ t.cats.mystery }}</button>
        </div>

        <div class="card">
            <div id="mystery-text">{{ initial_message }}</div>
        </div>

        <div class="actions">
            <button class="pulse-btn" onclick="fetchNext()">{{ t.next_btn }}</button>
            <button class="share-btn" onclick="shareText()">{{ t.share_btn }}</button>
        </div>
        <div id="toast" class="toast">{{ t.copied }}</div>
    </div>

    <script>
        let currentCategory = 'all';
        let currentLang = '{{ lang_code }}';
        let lastMessage = '';

        function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
        function closeSettings() { document.getElementById('settingsModal').style.display = 'none'; }
        
        function changeLang(lang) { window.location.href = `/?lang=${lang}`; }

        function setCategory(category, btn) {
            currentCategory = category;
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            fetchNext();
        }

        function fetchNext() {
            const textElem = document.getElementById('mystery-text');
            textElem.style.opacity = '0';
            textElem.style.transform = 'translateY(15px)';
            
            fetch(`/next?cat=${currentCategory}&lang=${currentLang}&last=${encodeURIComponent(lastMessage)}`)
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        lastMessage = data.message;
                        textElem.innerText = data.message;
                        textElem.style.opacity = '1';
                        textElem.style.transform = 'translateY(0)';
                    }, 250);
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

def get_messages_pool(t, cat_key):
    if cat_key == 'all':
        pool = []
        for cat in t["messages"].values():
            pool.extend(cat)
        return pool
    return t["messages"].get(cat_key, t["messages"]["calm"])

@app.route("/")
def home():
    lang = request.args.get('lang', 'ar')
    if lang not in PSF_DB:
        lang = 'ar'
    t = PSF_DB[lang]
    pool = get_messages_pool(t, 'all')
    initial = random.choice(pool)
    return render_template_string(HTML_TEMPLATE, t=t, languages=PSF_DB, lang_code=lang, lang_dir=t["dir"], initial_message=initial)

@app.route("/next")
def next_message():
    lang = request.args.get('lang', 'ar')
    cat_key = request.args.get('cat', 'all')
    last_msg = request.args.get('last', '')
    
    if lang not in PSF_DB:
        lang = 'ar'
    t = PSF_DB[lang]
    pool = get_messages_pool(t, cat_key)
    
    # محرك عشوائي ذكي يمنع تكرار نفس النص وراء بعضه مباشرة
    filtered_pool = [m for m in pool if m != last_msg]
    if not filtered_pool:
        filtered_pool = pool
        
    chosen = random.choice(filtered_pool)
    return jsonify({"message": chosen})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, jsonify, render_template_string, request
import random
import time

app = Flask(__name__)

# المحرك النفسي العاطفي لتطبيق PSF - هندسة الدوبامين والتشويق المستمر
PSF_PSYCHOLOGICAL_DB = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "PSF - النبض الخفي",
        "subtitle": "حيث تبحث عن صدى ما يدور في عمق روحك",
        "next_btn": "اكشف الإشارة التالية ⚡",
        "share_btn": "احتفظ باللحظة",
        "copied": "تم حفظ الأثر بنجاح!",
        "settings": "تخصيص التجربة",
        "modes": {
            "validation": "الصدى الشخصي",
            "mystery": "الترقب المجهول",
            "escape": "الهروب الواعي",
            "mirror": "مرآة الحقيقة"
        },
        "signals": {
            "validation": [
                "أنت لست صامتاً عبثاً، العالم هو الذي أصبح أصمّ عن سماعك.",
                "هناك تفصيل صغير في شخصيتك يلاحظه الجميع، لكن لا تجرؤ أحدهم على قوله بصوت عالٍ.",
                "أنت تتأقلم مع ما لا يناسبك كل يوم، وهذا هو سر قوتك المتعبة.",
                "كنت تتوقع رداً مختلفاً تماماً عما حصّلت عليه اليوم، أليس كذلك؟"
            ],
            "mystery": [
                "شخص ما كان يفكر بك قبل خمس دقائق بالذات، والصدفة ستكشفه قريباً.",
                "هناك إشعار أو رسالة تنتظرك في مكان ما، وكأنها ستغير مزاجك فوراً.",
                "اللحظة القادمة تحمل تغييراً طفيفاً في مسار يومك، انتبه جيداً لما سيتغير.",
                "وراء كل صمت عشته هذا الأسبوع، قصة كاملة لم تروَ بعد."
            ],
            "escape": [
                "تخلص من كل هذا الثقل المؤقت، أنت لست مطاداً لإرضاء هذا العالم اليوم.",
                "تخيل لو أنك غادرت كل شيء الآن واختفيت في مكان لا يعرفك فيه أحد.",
                "الشاشة هذه هي نافذتك الوحيدة لتهرب من ضغط تكرار الأيام المألوفة.",
                "امنح عقلك الحق في التوقف عن التفكير، العالم سيسير بشكل طبيعي دون قلقك."
            ],
            "mirror": [
                "أنت تبحث في هذا التطبيق عن جملة تشرح ما تعجز عن بوحه لنفسك.",
                "تعلم جيداً أن ما يزعجك ليس الحدث، بل الطريقة التي تفهم بها نوايا من حولك.",
                "أنت تظهر صلابة أمامهم، بينما تفاصيلك الصغيرة تهتز من أقل كلمة.",
                "توقف عن محاولة إثبات أنك بخير، مسموح لك أن تتعب بصمت."
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
            background-color: #05070a;
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
            top: 25px;
            left: 25px;
            right: 25px;
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
        .menu-btn {
            background: #0f172a;
            border: 1px solid #1e293b;
            color: #38bdf8;
            font-size: 1.2rem;
            padding: 10px 18px;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .menu-btn:hover { background: #1e293b; transform: scale(1.05); color: #fff; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            justify-content: center;
            align-items: center;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }
        .modal-content {
            background: #0f172a;
            border: 1px solid #1e293b;
            padding: 30px;
            border-radius: 24px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0,0,0,0.9);
        }
        .modal-content h3 { color: #38bdf8; margin-top: 0; font-size: 1.3rem; }
        .close-modal {
            margin-top: 20px;
            background: #1e293b;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .close-modal:hover { background: #334155; }

        .container {
            text-align: center;
            padding: 20px;
            max-width: 540px;
            width: 100%;
        }
        .logo {
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 6px;
            background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
            text-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
        }
        .subtitle {
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 30px;
            letter-spacing: 0.5px;
        }
        .modes-container {
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }
        .mode-btn {
            background: #0f172a;
            border: 1px solid #1e293b;
            color: #94a3b8;
            padding: 9px 18px;
            font-size: 0.85rem;
            border-radius: 22px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .mode-btn.active, .mode-btn:hover {
            background: #0284c7;
            color: white;
            border-color: #38bdf8;
            box-shadow: 0 0 20px rgba(2, 132, 199, 0.4);
            transform: translateY(-2px);
        }
        .card {
            background: #0f172a;
            border: 1px solid #1e293b;
            padding: 50px 30px;
            border-radius: 32px;
            margin-bottom: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
            min-height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.05), transparent);
            transition: 0.5s;
        }
        .card.loading::before {
            left: 100%;
        }
        #psych-text {
            font-size: 1.35rem;
            color: #f8fafc;
            line-height: 1.85;
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        .actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }
        .pulse-btn {
            background: linear-gradient(135deg, #0284c7, #4f46e5);
            color: white;
            border: none;
            padding: 16px 36px;
            font-size: 1.15rem;
            border-radius: 40px;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(2, 132, 199, 0.5);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: bold;
            flex: 2;
        }
        .pulse-btn:hover { 
            transform: translateY(-3px) scale(1.02); 
            box-shadow: 0 15px 35px rgba(2, 132, 199, 0.7); 
        }
        .share-btn {
            background: #0f172a;
            border: 1px solid #1e293b;
            color: #cbd5e1;
            padding: 16px 24px;
            font-size: 1rem;
            border-radius: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
        }
        .share-btn:hover { background: #1e293b; color: white; border-color: #475569; }
        .toast {
            margin-top: 15px;
            font-size: 0.9rem;
            color: #38bdf8;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="header-bar">
        <button class="menu-btn" onclick="openSettings()">⚡ نظام الإشارات</button>
    </div>

    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <h3>{{ t.settings }}</h3>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6;">تطبيق PSF مصمم ليعكس ما يدور في عمق شعورك عبر نبضات نفسية متجددة ولا نهائية.</p>
            <button class="close-modal" onclick="closeSettings()">إغلاق ومتابعة</button>
        </div>
    </div>

    <div class="container">
        <div class="logo">PSF</div>
        <div class="subtitle">{{ t.subtitle }}</div>
        
        <div class="modes-container">
            <button class="mode-btn active" onclick="setMode('validation', this)">{{ t.modes.validation }}</button>
            <button class="mode-btn" onclick="setMode('mystery', this)">{{ t.modes.mystery }}</button>
            <button class="mode-btn" onclick="setMode('escape', this)">{{ t.modes.escape }}</button>
            <button class="mode-btn" onclick="setMode('mirror', this)">{{ t.modes.mirror }}</button>
        </div>

        <div class="card" id="cardBox">
            <div id="psych-text">{{ initial_message }}</div>
        </div>

        <div class="actions">
            <button class="pulse-btn" onclick="fetchNextSignal()">{{ t.next_btn }}</button>
            <button class="share-btn" onclick="shareSignal()">{{ t.share_btn }}</button>
        </div>
        <div id="toast" class="toast">{{ t.copied }}</div>
    </div>

    <script>
        let currentMode = 'validation';
        let currentLang = '{{ lang_code }}';
        let lastText = '';

        function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
        function closeSettings() { document.getElementById('settingsModal').style.display = 'none'; }

        function setMode(mode, btn) {
            currentMode = mode;
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            fetchNextSignal();
        }

        function fetchNextSignal() {
            const card = document.getElementById('cardBox');
            const textElem = document.getElementById('psych-text');
            
            textElem.style.opacity = '0';
            textElem.style.transform = 'translateY(15px)';
            card.classList.add('loading');
            
            fetch(`/next?mode=${currentMode}&lang=${currentLang}&last=${encodeURIComponent(lastText)}`)
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        lastText = data.message;
                        textElem.innerText = data.message;
                        textElem.style.opacity = '1';
                        textElem.style.transform = 'translateY(0)';
                        card.classList.remove('loading');
                    }, 200);
                });
        }

        function shareSignal() {
            const text = document.getElementById('psych-text').innerText;
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

def get_signals_pool(t, mode_key):
    if mode_key == 'all':
        pool = []
        for cat in t["signals"].values():
            pool.extend(cat)
        return pool
    return t["signals"].get(mode_key, t["signals"]["validation"])

@app.route("/")
def home():
    lang = request.args.get('lang', 'ar')
    if lang not in PSF_PSYCHOLOGICAL_DB:
        lang = 'ar'
    t = PSF_PSYCHOLOGICAL_DB[lang]
    pool = get_signals_pool(t, 'validation')
    initial = random.choice(pool)
    return render_template_string(HTML_TEMPLATE, t=t, lang_code=lang, lang_dir=t["dir"], initial_message=initial)

@app.route("/next")
def next_signal():
    lang = request.args.get('lang', 'ar')
    mode_key = request.args.get('mode', 'validation')
    last_msg = request.args.get('last', '')
    
    if lang not in PSF_PSYCHOLOGICAL_DB:
        lang = 'ar'
    t = PSF_PSYCHOLOGICAL_DB[lang]
    pool = get_signals_pool(t, mode_key)
    
    # ضمان عدم تكرار نفس التأثير النفسي مباشرة لتحافظ على عنصر الدهشة والترقب
    filtered = [m for m in pool if m != last_msg]
    if not filtered:
        filtered = pool
        
    chosen = random.choice(filtered)
    return jsonify({"message": chosen})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

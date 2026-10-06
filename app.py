from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

MYSTERY_MESSAGES = [
    "هناك فكرة صغيرة تنتظر أن تكتشفها الآن...",
    "أحياناً، كلمة واحدة في الوقت المناسب تغير شكل يومك بالكامل.",
    "الهدوء الحقيقي يبدأ عندما تتوقف عن البحث وتترك العقل يتنفس.",
    "ما تخفيه اللحظة القادمة قد يكون هو ما تبحث عنه طوال الوقت.",
    "توقف لثانية... ودع صخب العالم يختفي خلف هذه الشاشة.",
    "كل ضغطة تفتح لك نافذة على عالم هادئ لا يشبه غيره.",
    "لست بحاجة لأن تكون جاهزاً... فقط دع الفضول يأخذك."
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PSF - راحة نفسية</title>
    <style>
        body {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            text-align: center;
            padding: 30px;
            max-width: 450px;
        }
        .logo {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: #58a6ff;
            margin-bottom: 0;
        }
        .subtitle {
            color: #8b949e;
            font-size: 0.95rem;
            margin-bottom: 30px;
        }
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 30px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.4s ease;
        }
        #mystery-text {
            font-size: 1.25rem;
            color: #f0f6fc;
            line-height: 1.6;
        }
        .pulse-btn {
            background: linear-gradient(135deg, #1f6feb, #388bfd);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            border-radius: 35px;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(31, 111, 235, 0.4);
            transition: all 0.3s ease;
            font-weight: bold;
        }
        .pulse-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 25px rgba(56, 139, 253, 0.6);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">PSF</div>
        <div class="subtitle">الملاذ الآمن للفضول والهدوء</div>
        
        <div class="card" id="card-box">
            <div id="mystery-text">{{ initial_message }}</div>
        </div>

        <button class="pulse-btn" onclick="fetchNext()">اكتشف التالي</button>
    </div>

    <script>
        function fetchNext() {
            const card = document.getElementById('card-box');
            card.style.opacity = '0.3';
            
            fetch('/next')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mystery-text').innerText = data.message;
                    card.style.opacity = '1';
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, initial_message=random.choice(MYSTERY_MESSAGES))

@app.route("/next")
def next_message():
    return jsonify({"message": random.choice(MYSTERY_MESSAGES)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

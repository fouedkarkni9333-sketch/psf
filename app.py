from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

# دعم أكثر من 30 لغة مع محتوى مخصص لكل لغة
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
            "الكلمة الطيبة في الوقت المناسب تساوي عمراً كاملاً من الطمأنينة.",
            "ما تخفيه اللحظة القادمة قد يكون هو الإجابة التي بحثت عنها طويلاً."
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
            "A kind word at the right time is worth a lifetime of peace.",
            "What the next moment hides might be the answer you've long sought."
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
            "Un mot gentil au bon moment vaut une vie de sérénité.",
            "Ce que cache le moment suivant pourrait être la réponse cherchée."
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
            "Una palabra amable en el momento adecuado vale toda una vida.",
            "Lo que oculta el próximo momento podría ser la respuesta."
        ]
    },
    "de": {
        "name": "Deutsch",
        "dir": "ltr",
        "title": "PSF - Sicherer Zufluchtsort",
        "subtitle": "Der sichere Hafen für endlose Neugier und Ruhe",
        "next_btn": "Nächstes entdecken",
        "share_btn": "Kopieren",
        "copied": "Text erfolgreich kopiert!",
        "settings": "Einstellungen & Sprachen",
        "cats": {"all": "Alle", "calm": "Ruhe", "curiosity": "Neugier", "wisdom": "Weisheit", "mystery": "Mysterium"},
        "messages": [
            "Wahre Ruhe beginnt, wenn man aufhört zu suchen.",
            "Haltet kurz inne... und lasst den Lärm der Welt verblassen.",
            "Welche kleine Idee wartet darauf, von Ihnen entdeckt zu werden?",
            "Ein gutes Wort zur rechten Zeit ist ein ganzes Leben an Frieden wert.",
            "Was der nächste Moment verbirgt, könnte Ihre Antwort sein."
        ]
    },
    "it": {
        "name": "Italiano",
        "dir": "ltr",
        "title": "PSF - Rifugio Sicuro",
        "subtitle": "Il rifugio sicuro per curiosità e pace infinita",
        "next_btn": "Scopri il Prossimo",
        "share_btn": "Copia",
        "copied": "Testo copiato con successo!",
        "settings": "Impostazioni e Lingue",
        "cats": {"all": "Tutti", "calm": "Calma", "curiosity": "Curiosità", "wisdom": "Saggezza", "mystery": "Mistero"},
        "messages": [
            "La vera calma inizia quando smetti di cercare.",
            "Fermati un secondo... e lascia che il rumore del mondo svanisca.",
            "Quale piccola idea aspetta di essere scoperta oggi?",
            "Una parola gentile al momento giusto vale una vita di pace.",
            "Ciò che il prossimo momento nasconde potrebbe essere la risposta."
        ]
    },
    "tr": {
        "name": "Türkçe",
        "dir": "ltr",
        "title": "PSF - Güvenli Sığınak",
        "subtitle": "Sonsuz merak ve huzur için güvenli sığınak",
        "next_btn": "Sonrakini Keşfet",
        "share_btn": "Kopyala",
        "copied": "Metin başarıyla kopyalandı!",
        "settings": "Ayarlar ve Diller",
        "cats": {"all": "Tümü", "calm": "Sakinlik", "curiosity": "Merak", "wisdom": "Bilgelik", "mystery": "Gizem"},
        "messages": [
            "Gerçek sakinlik aramayı bıraktığında başlar.",
            "Bir saniye dur... ve dünyanın gürültüsünün kaybolmasına izin ver.",
            "Bugün seni keşfedilmeyi bekleyen hangi küçük fikir var?",
            "Doğru zamanda söylenen tatlı bir söz ömre bedeldir.",
            "Gelecek anın sakladığı şey aradığın cevap olabilir."
        ]
    },
    "pt": {
        "name": "Português",
        "dir": "ltr",
        "title": "PSF - Refúgio Seguro",
        "subtitle": "O refúgio seguro para curiosidade e paz infinita",
        "next_btn": "Descobrir Próximo",
        "share_btn": "Copiar",
        "copied": "Texto copiado com sucesso!",
        "settings": "Configurações e Idiomas",
        "cats": {"all": "Tudo", "calm": "Calma", "curiosity": "Curiosidade", "wisdom": "Sabedoria", "mystery": "Mistério"},
        "messages": [
            "A verdadeira calma começa quando você para de procurar.",
            "Pare um segundo... e deixe o barulho do mundo desaparecer.",
            "Que pequena ideia está esperando para ser descoberta por você hoje?",
            "Uma palavra gentil no momento certo vale uma vida de paz.",
            "O que o próximo momento esconde pode ser a resposta."
        ]
    },
    "ru": {
        "name": "Русский",
        "dir": "ltr",
        "title": "PSF - Безопасная гавань",
        "subtitle": "Безопасное прибежище для бесконечного любопытства",
        "next_btn": "Далее",
        "share_btn": "Копировать",
        "copied

from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)

# البنية التحتية الكاملة لتطبيق PSF - أكثر من 30 لغة عالمية مع محرك النفس والتشويق العميق
PSF_DB = {
    "ar": {
        "name": "العربية", "dir": "rtl",
        "title": "PSF - النبض الخفي", "subtitle": "الملاذ الحي للعمق والفضول اللامتناهي",
        "next_btn": "اكشف الإشارة التالية ⚡", "share_btn": "نسخ الأثر", "copied": "تم الاحتفاظ بالأثر بنجاح!",
        "settings": "إعدادات اللغات العالمية",
        "messages": [
            "أنت لست صامتاً عبثاً، العالم هو الذي أصبح عاجزاً عن قراءة تفاصيلك.",
            "هناك فكرة صغيرة تعبث بعقلك الآن، وتنتظر الشجاعة لتخرج إلى النور.",
            "اللحظة القادمة تحمل تغييراً طفيفاً في مزاجك، انتبه جيداً لما سيتغير.",
            "أنت تتأقلم مع ما لا يناسبك كل يوم، وهذا هو سر قوتك المتعبة.",
            "خلف كل صمت عشناه هذا الأسبوع، قصة كاملة لم تروَ لأحد بعد."
        ]
    },
    "en": {
        "name": "English", "dir": "ltr",
        "title": "PSF - Hidden Pulse", "subtitle": "The living sanctuary for depth and endless curiosity",
        "next_btn": "Discover Next Signal ⚡", "share_btn": "Copy Trace", "copied": "Trace saved successfully!",
        "settings": "Global Languages Settings",
        "messages": [
            "You are not silent by chance; the world has simply grown deaf to your depth.",
            "A subtle thought is playing in your mind right now, waiting for the courage to emerge.",
            "The next moment holds a quiet shift in your rhythm; pay close attention.",
            "You adapt to what doesn't fit every single day, and that is your exhausted strength.",
            "Behind every silence this week lies a complete story yet unsaid."
        ]
    },
    "fr": {
        "name": "Français", "dir": "ltr",
        "title": "PSF - Le Pouls Caché", "subtitle": "Le sanctuaire vivant de la curiosité infinie",
        "next_btn": "Révéler le Suivant ⚡", "share_btn": "Copier la Trace", "copied": "Trace enregistrée avec succès !",
        "settings": "Paramètres des Langues",
        "messages": [
            "Tu n'es pas silencieux par hasard, c'est le monde qui est devenu sourd.",
            "Une idée subtile traverse ton esprit en ce moment, attendant d'éclore.",
            "Le prochain instant porte un changement subtil dans ton humeur, observe bien.",
            "Tu t'adaptes à ce qui ne te convient pas chaque jour, c'est ta force cachée.",
            "Derrière chaque silence de cette semaine se cache une histoire non dite."
        ]
    },
    "es": {
        "name": "Español", "dir": "ltr",
        "title": "PSF - Pulso Oculto", "subtitle": "El santuario vivo para la curiosidad infinita",
        "next_btn": "Descubrir Siguiente ⚡", "share_btn": "Copiar", "copied": "¡Copiado con éxito!",
        "settings": "Configuración de Idiomas",
        "messages": [
            "No estás en silencio por casualidad, el mundo se ha vuelto sordo a tu profundidad.",
            "Una pequeña idea ronda tu mente ahora mismo, esperando el valor para salir.",
            "El próximo momento trae un cambio sutil en tu día; presta atención.",
            "Te adaptas a lo que no encaja cada día, y esa es tu fuerza cansada.",
            "Detrás de cada silencio hay una historia completa que aún no ha sido contada."
        ]
    },
    "de": {
        "name": "Deutsch", "dir": "ltr",
        "title": "PSF - Versteckter Puls", "subtitle": "Das lebendige Zufluchtsort für endlose Neugier",
        "next_btn": "Nächstes Signal ⚡", "share_btn": "Kopieren", "copied": "Erfolgreich kopiert!",
        "settings": "Spracheinstellungen",
        "messages": [
            "Du bist nicht grundlos still; die Welt ist einfach taub für deine Tiefe geworden.",
            "Ein kleiner Gedanke kreist gerade in deinem Kopf und wartet auf den Mut.",
            "Der nächste Moment bringt eine subtile Veränderung in deinen Tag.",
            "Du passt dich jeden Tag an das an, was nicht passt – das ist deine Stärke.",
            "Hinter jedem Schweigen dieser Woche verbirgt sich eine unzählige Geschichte."
        ]
    },
    "it": {
        "name": "Italiano", "dir": "ltr",
        "title": "PSF - Polso Nascosto", "subtitle": "Il santuario vivente della curiosità infinita",
        "next_btn": "Scopri il Segnale ⚡", "share_btn": "Copia", "copied": "Copiato con successo!",
        "settings": "Impostazioni Lingue",
        "messages": [
            "Non sei in silenzio per caso, è il mondo che è diventato sordo alla tua profondità.",
            "Un piccolo pensiero sta giocando nella tua mente, in attesa di coraggio.",
            "Il prossimo momento porta un leggero cambiamento nel tuo umore.",
            "Ti adatti a ciò che non ti appartiene ogni giorno; questa è la tua forza.",
            "Dietro ogni silenzio c'è una storia intera non ancora raccontata."
        ]
    },
    "pt": {
        "name": "Português", "dir": "ltr",
        "title": "PSF - Pulso Oculto", "subtitle": "O santuário vivo para a curiosidade infinita",
        "next_btn": "Revelar Próximo ⚡", "share_btn": "Copiar", "copied": "Copiado com sucesso!",
        "settings": "Configurações de Idiomas",
        "messages": [
            "Você não está em silêncio por acaso; o mundo é que ficou surdo à sua profundidade.",
            "Uma pequena ideia está rondando sua mente agora, esperando coragem.",
            "O próximo momento traz uma mudança sutil no seu dia; preste atenção.",
            "Você se adapta ao que não se encaixa todos os dias, e essa é sua força.",
            "Por trás de cada silêncio desta semana existe uma história inteira."
        ]
    },
    "ru": {
        "name": "Русский", "dir": "ltr",
        "title": "PSF - Скрытый Пульс", "subtitle": "Живое убежище для бесконечного любопытства",
        "next_btn": "Следующий сигнал ⚡", "share_btn": "Копировать", "copied": "Успешно скопировано!",
        "settings": "Настройки языков",
        "messages": [
            "Ты молчишь не случайно; это мир разучился слышать твою глубину.",
            "Какая-то мысль крутится у тебя в голове прямо сейчас.",
            "Следующий момент принесет едва заметное изменение в твой день.",
            "Ты каждый день подстраиваешься под то, что тебе не подходит.",
            "За каждым твоим молчанием скрывается целая нерассказанная история."
        ]
    },
    "tr": {
        "name": "Türkçe", "dir": "ltr",
        "title": "PSF - Gizli Nabız", "subtitle": "Sonsuz merak ve derinlik için canlı sığınak",
        "next_btn": "Sonraki Sinyal ⚡", "share_btn": "Kopyala", "copied": "Başarıyla kopyalandı!",
        "settings": "Dil Ayarları",
        "messages": [
            "Tesadüfen sessiz değilsin; dünya derinliğine karşı sağırlaştı.",
            "Şu an zihninde dönüp duran küçük bir düşünce cesaretini bekliyor.",
            "Gelecek an, gününün akışında küçük bir değişim getirecek.",
            "Her gün uymayan şeylere uyum sağlıyorsun; yorgun gücün budur.",
            "Bu hafta yaşadığın her sessizliğin arkasında anlatılmamış bir hikaye var."
        ]
    },
    "zh": {
        "name": "中文", "dir": "ltr",
        "title": "PSF - 隐藏脉搏", "subtitle": "探索无尽好奇与深度的活体庇护所",
        "next_btn": "揭示下一个信号 ⚡", "share_btn": "复制", "copied": "复制成功！",
        "settings": "语言设置",
        "messages": [
            "你并不是无缘无故沉默，只是这个世界听不见你的深度。",
            "此刻有一个微小的想法正在你脑海盘旋，等待着勇气破土而出。",
            "接下来的时刻将为你的情绪带来微妙的转变。",
            "你每天都在适应那些不合适的事物，这就是你疲惫的力量。",
            "本周每一次沉默的背后，都藏着一段未曾讲述完的故事。"
        ]
    },
    "ja": {
        "name": "日本語", "dir": "ltr",
        "title": "PSF - 隠された鼓動", "subtitle": "無限の好奇心と深みのための生きた隠れ家",
        "next_btn": "次のシグナル ⚡", "share_btn": "コピー", "copied": "コピーしました！",
        "settings": "言語設定",
        "messages": [
            "あなたが黙っているのは偶然ではない。世界があなたの深さを聞き逃しているのだ。",
            "今、あなたの頭の中で小さなアイデアが形を求めている。",
            "次の瞬間は、あなたの日々に静かな変化をもたらす。",
            "あなたは毎日合わないものに適応している。それがあなたの疲れた強さだ。",
            "今週のすべての沈黙の背後には、まだ語られていない物語がある。"
        ]
    },
    "ko": {
        "name": "한국어", "dir": "ltr",
        "title": "PSF - 숨겨진 맥박", "subtitle": "끝없는 호기심과 깊이를 위한 살아있는 안식처",
        "next_btn": "다음 신호 보기 ⚡", "share_btn": "복사", "copied": "성공적으로 복사되었습니다!",
        "settings": "언어 설정",
        "messages": [
            "당신이 침묵하는 것은 우연이 아닙니다. 세상이 당신의 깊이를 듣지 못할 뿐입니다.",
            "지금 이 순간 당신의 머릿속을 스치는 작은 생각이 용기를 기다리고 있습니다.",
            "다음 순간은 당신의 하루에 미세한 변화를 가져올 것입니다.",
            "당신은 매일 어울리지 않는 것들에 적응하고 있으며, 그것이 당신의 지친 강인함입니다.",
            "이번 주 당신의 모든 침묵 뒤에는 아직 들려주지 못한 이야기가 숨어 있습니다."
        ]
    },
    "hi": {
        "name": "हिन्दी", "dir": "ltr",
        "title": "PSF - छिपी हुई नब्ज", "subtitle": "अंतहीन जिज्ञासा और गहराई का जीवंत आश्रय",
        "next_btn": "अगला संकेत देखें ⚡", "share_btn": "कॉपी करें", "copied": "सफलतापूर्वक कॉपी किया गया!",
        "settings": "भाषा सेटिंग्स",
        "messages": [
            "आप यूँ ही चुप नहीं हैं; यह दुनिया आपकी गहराई को सुनने में असमर्थ हो गई है.",
            "इस समय आपके दिमाग में एक छोटा सा विचार चल रहा है जो हिम्मत का इंतजार कर रहा है.",
            "अगला पल आपके दिन में एक सूक्ष्म बदलाव लाएगा, ध्यान दीजिए.",
            "आप हर दिन उन चीज़ों से तालमेल बिठाते हैं जो आपको फिट नहीं बैठतीं.",
            "इस हफ्ते की हर चुप्पी के पीछे एक पूरी अनकही कहानी छिपी है।"
        ]
    },
    "nl": {
        "name": "Nederlands", "dir": "ltr",
        "title": "PSF - Verborgen Polsslag", "subtitle": "Het levende toevluchtsoord voor eindeloze nieuwsgierigheid",
        "next_btn": "Ontdek Volgende ⚡", "share_btn": "Kopiëren", "copied": "Succesvol gekopieerd!",
        "settings": "Taalinstellingen",
        "messages": [
            "Je bent niet zomaar stil; de wereld is eenvoudig doof geworden voor je diepte.",
            "Er speelt een subtiele gedachte door je hoofd die wacht op moed.",
            "Het volgende moment brengt een lichte verschuiving in je dag.",
            "Je past je elke dag aan wat niet past, en dat is je vermoeide kracht.",
            "Achter elke stilte deze week schuilt een volledig onverteld verhaal."
        ]
    },
    "pl": {
        "name": "Polski", "dir": "ltr",
        "title": "PSF - Ukryty Puls", "subtitle": "Żywe schronienie dla nieskończonej ciekawości",
        "next_btn": "Odkryj następny ⚡", "share_btn": "Kopiuj", "copied": "Skopiowano pomyślnie!",
        "settings": "Ustawienia języka",
        "messages": [
            "Nie milczysz bez powodu; świat po prostu przestał słyszeć Twoją głębię.",
            "Jakaś subtelna myśl krąży teraz w Twojej głowie, czekając na odwagę.",
            "Następna chwila przyniesie subtelną zmianę w Twoim dniu.",
            "Codziennie dopasowujesz się do tego, co nie pasuje – to Twoja siła.",
            "Za każdym milczeniem kryje się nieopowiedziana historia."
        ]
    },
    "sv": {
        "name": "Svenska", "dir": "ltr",
        "title": "PSF - Dold Puls", "subtitle": "Den levande tillflyktsorten för oändlig nyfikenhet",
        "next_btn": "Upptäck Nästa ⚡", "share_btn": "Kopiera", "copied": "Kopierade framgångsrikt!",
        "settings": "Språkinställningar",
        "messages": [
            "Du är inte tyst av en slump; världen har blivit döv för ditt djup.",
            "En subtil tanke leker i ditt sinne just nu och väntar på mod.",
            "Nästa ögonblick för med sig en liten förändring i din dag.",
            "Du anpassar dig till det som inte passar varje dag, och det är din styrka.",
            "Bakom varje tystnad denna vecka finns en oerod historia."
        ]
    },
    "el": {
        "name": "Ελληνικά", "dir": "ltr",
        "title": "PSF - Κρυφός Παλμός", "subtitle": "Το ζωντανό καταφύγιο για την ατελείωτη περιέργεια",
        "next_btn": "Επόμενο Σήμα ⚡", "share_btn": "Αντιγραφή", "copied": "Αντιγράφηκε με επιτυχία!",
        "settings": "Ρυθμίσεις Γλωσσών",
        "messages": [
            "Δεν σιωπάς τυχαία. Ο κόσμος έχει γίνει κουφός στο βάθος σου.",
            "Μια μικρή σκέψη παίζει στο μυαλό σου τώρα, περιμένοντας θάρρος.",
            "Η επόμενη στιγμή φέρνει μια λεπτή αλλαγή στη μέρα σου.",
            "Προσαρμόζεσαι σε ό,τι δεν ταιριάζει κάθε μέρα, αυτή είναι η δύναμή σου.",
            "Πίσω από κάθε σιωπή κρύβεται μια ολόκληρη ιστορία."
        ]
    },
    "vi": {
        "name": "Tiếng Việt", "dir": "ltr",
        "title": "PSF - Nhịp Đập Ẩn Giấu", "subtitle": "Nơi trú ẩn sống động cho sự tò mò vô tận",
        "next_btn": "Khám Phá Tiếp Theo ⚡", "share_btn": "Sao Chép", "copied": "Đã sao chép thành công!",
        "settings": "Cài Đặt Ngôn Ngữ",
        "messages": [
            "Bạn không vô cωզ im lặng; thế giới chỉ đơn giản là đã điếc trước chiều sâu của bạn.",
            "Một suy nghĩ nhỏ đang lướt qua tâm trí bạn, chờ đợi lòng dũng cảm.",
            "Khoảnh khắc tiếp theo mang lại sự thay đổi tinh tế trong ngày của bạn.",
            "Bạn thích nghi với những điều không phù hợp mỗi ngày, đó là sức mạnh mệt mỏi.",
            "Đằng sau mỗi khoảng lặng tuần này là một câu chuyện chưa kể."
        ]
    },
    "id": {
        "name": "Bahasa Indonesia", "dir": "ltr",
        "title": "PSF - Denyut Tersembunyi", "subtitle": "Tempat perlindungan hidup untuk rasa ingin tahu",
        "next_btn": "Temukan Berikutnya ⚡", "share_btn": "Salin", "copied": "Berhasil disalin!",
        "settings": "Pengaturan Bahasa",
        "messages": [
            "Kamu tidak diam begitu saja; dunia ini telah menjadi tuli pada kedalamanmu.",
            "Sebuah pemikiran kecil sedang berputar di benakmu, menunggu keberanian.",
            "Momen berikutnya membawa perubahan kecil dalam harimu.",
            "Kamu beradaptasi dengan hal-hal yang tidak pas setiap hari, itulah kekuatanmu.",
            "Di balik setiap keheningan minggu ini ada cerita utuh yang belum terucap."
        ]
    },
    "ms": {
        "name": "Bahasa Melayu", "dir": "ltr",
        "title": "PSF - Denyutan Tersembunyi", "subtitle": "Tempat perlindungan hidup untuk rasa ingin tahu",
        "next_btn": "Seterusnya ⚡", "share_btn": "Salin", "copied": "Berjaya disalin!",
        "settings": "Tetapan Bahasa",
        "messages": [
            "Anda tidak berdiam diri secara kebetulan; dunia telah menjadi pekak kepada kedalaman anda.",
            "Satu fikiran halus sedang berlegar dalam minda anda sekarang.",
            "Detik seterusnya membawa sedikit perubahan pada hari anda.",
            "Anda menyesuaikan diri dengan perkara yang tidak sepadan setiap hari.",
            "Di sebalik setiap keheningan minggu ini terdapat kisah yang belum diceritakan."
        ]
    },
    "th": {
        "name": "ไทย", "dir": "ltr",
        "title": "PSF - ชีพจรซ่อนเร้น", "subtitle": "ที่หลบภัยที่มีชีวิตชีวาสำหรับความอยากรู้อยากเห็น",
        "next_btn": "สำรวจถัดไป ⚡", "share_btn": "คัดลอก", "copied": "คัดลอกสำเร็จ!",
        "settings": "การตั้งค่าภาษา",
        "messages": [
            "คุณไม่ได้เงียบโดยบังเอิญ แต่โลกต่างหากที่หูหนวกต่อความลึกซึ้งของคุณ",
            "มีความคิดเล็กๆ วิ่งวนอยู่ในหัวคุณตอนนี้ รอคอยความกล้าหาญ",
            "ช่วงเวลาถัดไปจะนำความเปลี่ยนแปลงเล็กๆ มาสู่วันของคุณ",
            "คุณปรับตัวเข้ากับสิ่งที่ไม่เข้ากันทุกวัน นั่นคือความแข็งแกร่งของคุณ",
            "เบื้องหลังความเงียบในสัปดาห์นี้มีเรื่องราวที่ยังไม่ได้เล่าซ่อนอยู่"
        ]
    },
    "ro": {
        "name": "Română", "dir": "ltr",
        "title": "PSF - Puls Ascuns", "subtitle": "Sanctuarul viu pentru curiozitate infinită",
        "next_btn": "Descoperă Următorul ⚡", "share_btn": "Copiază", "copied": "Copiat cu succes!",
        "settings": "Setări Limbi",
        "messages": [
            "Nu taci întâmplător; lumea a devenit surdă la profunzimea ta.",
            "Un gând subtil se joacă acum în mintea ta, așteptând curaj.",
            "Următorul moment aduce o schimbare fină în starea ta.",
            "Te adaptezi la ceea ce nu se potrivește în fiecare zi.",
            "În spatele fiecărei tăceri se ascunde o poveste nespusă."
        ]
    },
    "hu": {
        "name": "Magyar", "dir": "ltr",
        "title": "PSF - Rejtett Pulzus", "subtitle": "Az élő menedék a végtelen kíváncsisághoz",
        "next_btn": "Következő Jel ⚡", "share_btn": "Másolás", "copied": "Sikeresen másolva!",
        "settings": "Nyelvi Beállítások",
        "messages": [
            "Nem véletlenül hallgatsz; a világ egyszerűen süket lett a mélységedre.",
            "Egy apró gondolat kering a fejedben, bátorságra várva.",
            "A következő pillanat finom változást hoz a napodba.",
            "Minden nap alkalmazkodsz ahhoz, ami nem illik hozzád – ez az erőd.",
            "Minden csend mögött egy elmeséletlen történet rejlik."
        ]
    },
    "cs": {
        "name": "Čeština", "dir": "ltr",
        "title": "PSF - Skrytý Puls", "subtitle": "Živé útočiště pro nekonečnou zvědavost",
        "next_btn": "Objevit Další ⚡", "share_btn": "Kopírovat", "copied": "Úspěšně zkopírováno!",
        "settings": "Nastavení Jazyků",
        "messages": [
            "Nemelčíš náhodou; svět prostě zhluchl vůči tvé hloubce.",
            "V hlavě se ti teď honí drobná myšlenka a čeká na odvahu.",
            "Další okamžik přinese jemnou změnu do tvého dne.",
            "Každý den se přizpůsobuješ tomu, co se nehodí – to je tvá síla.",
            "Za každým tichem tohoto týdne se skrývá nevyprávěný příběh."
        ]
    },
    "uk": {
        "name": "Українська", "dir": "ltr",
        "title": "PSF - Прихований Пульс", "subtitle": "Живий притулок для нескінченної цікавості",
        "next_btn": "Наступний сигнал ⚡", "share_btn": "Копіювати", "copied": "Успішно скопійовано!",
        "settings": "Налаштування мов",
        "messages": [
            "Ти мовчиш не випадково; це світ просто оглух до твоєї глибини.",
            "Якась тонка думка крутиться в твоїй голові прямо зараз.",
            "Наступний момент принесе ледь помітні зміни у твій день.",
            "Ти щодня пристосовуєшся до того, що не підходить.",
            "За кожним мовчанням цього тижня ховається нерозказана історія."
        ]
    },
    "fi": {
        "name": "Suomi", "dir": "ltr",
        "title": "PSF - Piilotettu Pulssi", "subtitle": "Elävä turvasatama loputtomalle uteliaisuudelle",
        "next_btn": "Löydä Seuraava ⚡", "share_btn": "Kopioi", "copied": "Kopioitu onnistuneesti!",
        "settings": "Kieliasetukset",
        "messages": [
            "Et ole hiljaa sattumalta; maailma on vain kuuro syvyydellesi.",
            "Pieni ajatus pyörii mielessäsi juuri nyt ja odottaa rohkeutta.",
            "Seuraava hetki tuo pienen muutoksen päivääsi.",
            "Sopeudut siihen mikä ei sovi joka päivä – se on voimasi.",
            "Jokaisen hiljaisuuden takana on kertomaton tarina."
        ]
    },
    "da": {
        "name": "Dansk", "dir": "ltr",
        "title": "PSF - Skjult Puls", "subtitle": "Det levende tilflugtssted for uendelig nysgerrighed",
        "next_btn": "Opdag Næste ⚡", "share_btn": "Kopier", "copied": "Kopieret med succes!",
        "settings": "Sprogindstillinger",
        "messages":

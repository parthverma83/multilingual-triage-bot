"""
Single source of truth for all symptom vocabulary.

Structure:
    SYMPTOM_MAP[canonical_id] = {
        "english":  [...],   # English phrases
        "hindi":    [...],   # Devanagari Hindi
        "marathi":  [...],   # Devanagari Marathi
        "hinglish": [...],   # Romanised Hindi/Marathi (no script switch)
    }

Rules:
- All English phrases are lowercase.
- Hindi/Marathi phrases are in Devanagari.
- Hinglish covers common romanisation variants.
- No regex syntax here — just plain strings.
  The extractor turns these into patterns at import time.
"""

from typing import Dict, List

SymptomVocab = Dict[str, List[str]]
SymptomEntry = Dict[str, SymptomVocab]

SYMPTOM_MAP: Dict[str, SymptomEntry] = {

    # ── Respiratory ───────────────────────────────────────────────────────────

    "shortness_of_breath": {
        "english": [
            "shortness of breath", "difficulty breathing", "breathless",
            "can't breathe", "cannot breathe", "unable to breathe",
            "breathing problem", "breathing difficulty", "hard to breathe",
            "struggling to breathe", "out of breath", "gasping",
        ],
        "hindi": [
            "साँस लेने में दिक्कत", "सांस लेने में दिक्कत",
            "साँस फूल रही है", "सांस फूल रही है",
            "दम घुट रहा है", "साँस नहीं ले पा रहा",
            "सांस नहीं आ रही", "दम फूलना",
        ],
        "marathi": [
            "श्वास घेण्यास त्रास", "श्वास घेता येत नाही",
            "धाप लागली", "श्वास घेण्यास अडचण",
            "दम लागतो", "श्वास कमी पडतो",
        ],
        "hinglish": [
            "saans lene me dikkat", "saans nahi aa rahi",
            "saans phool rahi hai", "dam ghut raha hai",
            "saans nahi le pa raha", "breathing problem hai",
        ],
    },

    "cough": {
        "english": [
            "cough", "coughing", "dry cough", "wet cough",
            "persistent cough", "coughing up blood", "coughing blood",
            "whooping cough", "productive cough",
        ],
        "hindi": [
            "खांसी", "खाँसी", "सूखी खांसी", "बलगम वाली खांसी",
            "खून आ रहा है खांसी में", "काली खांसी",
        ],
        "marathi": [
            "खोकला", "कोरडा खोकला", "बलगम असलेला खोकला",
            "खोकला येतो", "खोकल्यात रक्त येते",
        ],
        "hinglish": [
            "khansi", "khasi", "sukhi khansi", "balgam wali khansi",
            "khansi ho rahi hai",
        ],
    },

    # ── Cardiac ───────────────────────────────────────────────────────────────

    "chest_pain": {
        "english": [
            "chest pain", "chest ache", "chest discomfort",
            "pain in chest", "tightness in chest", "chest tightness",
            "pressure in chest", "chest pressure", "heart pain",
            "pain radiating to arm", "pain radiating to left arm",
            "left arm pain", "jaw pain with chest pain",
            "chest pain radiating", "squeezing chest",
        ],
        "hindi": [
            "छाती में दर्द", "सीने में दर्द", "सीने में जकड़न",
            "दिल में दर्द", "छाती में भारीपन", "बाईं बांह में दर्द",
            "सीने में दबाव",
        ],
        "marathi": [
            "छातीत दुखणे", "छातीत वेदना", "छातीत जड वाटणे",
            "हृदयात दुखणे", "छातीत दाब जाणवणे",
            "छातीत दुखत आहे", "छातीत खूप दुखत आहे",
        ],
        "hinglish": [
            "chhaati mein dard", "seene mein dard", "dil mein dard",
            "chhaati mein dard ho raha hai", "seene mein jakdan",
            "bayi baah mein dard",
        ],
    },

    "heart_palpitations": {
        "english": [
            "palpitations", "heart racing", "fast heartbeat",
            "irregular heartbeat", "heart pounding", "heart fluttering",
            "skipped heartbeat", "heart beating fast",
        ],
        "hindi": [
            "दिल की धड़कन तेज है", "घबराहट", "दिल धड़क रहा है",
            "दिल की धड़कन अनियमित है",
        ],
        "marathi": [
            "हृदय जोरात धडधडते", "छाती धडधडते", "हृदयाची गती वाढली",
        ],
        "hinglish": [
            "dil ki dhadkan tej hai", "ghabrahat ho rahi hai",
            "dil bahut tez dhadak raha hai",
        ],
    },

    # ── Neurological ──────────────────────────────────────────────────────────

    "headache": {
        "english": [
            "headache", "head pain", "head ache", "migraine",
            "throbbing head", "severe headache", "splitting headache",
            "worst headache of my life", "sudden severe headache",
        ],
        "hindi": [
            "सिर दर्द", "सिरदर्द", "माइग्रेन", "सिर में दर्द",
            "सिर में असहनीय दर्द", "सिर में बहुत तेज दर्द",
            "सर में दर्द", "सर दर्द",
        ],
        "marathi": [
            "डोके दुखते", "डोकेदुखी", "डोक्यात दुखत आहे",
            "माझ्या डोक्यात दुखत आहे", "डोके जड वाटते",
            "डोके खूप दुखते", "डोळ्यांसमोर अंधारी येते",
        ],
        "hinglish": [
            "sir dard", "sar dard", "sir mein dard", "migraine hai",
            "bahut tej sir dard hai",
        ],
    },

    "dizziness": {
        "english": [
            "dizziness", "dizzy", "vertigo", "spinning",
            "room spinning", "lightheaded", "light headed",
            "feeling faint", "unsteady", "loss of balance",
        ],
        "hindi": [
            "चक्कर आना", "चक्कर", "सिर घूमना", "संतुलन खोना",
            "बेहोशी सी लग रही है",
        ],
        "marathi": [
            "चक्कर येतो", "डोळ्यांसमोर अंधारी येते",
            "तोल जातो", "चक्कर आली",
        ],
        "hinglish": [
            "chakkar aa raha hai", "chakkar", "sir ghoom raha hai",
            "balance nahi ban raha",
        ],
    },

    "seizure": {
        "english": [
            "seizure", "convulsion", "fits", "epilepsy attack",
            "shaking uncontrollably", "tremors", "twitching",
            "body shaking", "epileptic fit",
        ],
        "hindi": [
            "मिर्गी", "दौरा", "दौरे पड़ना", "झटके आना",
            "शरीर काँपना", "ऐंठन",
        ],
        "marathi": [
            "फेफरे येणे", "झटके येणे", "मिरगी", "अंग थरथरणे",
        ],
        "hinglish": [
            "mirgi", "daure pad rahe hain", "jhatke aa rahe hain",
            "body shake ho rahi hai", "fits aa rahe hain",
        ],
    },

    "loss_of_consciousness": {
        "english": [
            "loss of consciousness", "unconscious", "fainted", "faint",
            "passed out", "blacked out", "not responding",
            "unresponsive", "collapsed",
        ],
        "hindi": [
            "बेहोश", "बेहोशी", "होश खोना", "गिर पड़ना",
            "प्रतिक्रिया नहीं दे रहा",
        ],
        "marathi": [
            "शुद्ध हरपली", "बेशुद्ध", "बेशुद्धावस्था", "गुंगी आली",
        ],
        "hinglish": [
            "behosh", "behosh ho gaya", "hosh kho diya",
            "gir pada", "response nahi de raha",
        ],
    },

    "stroke_symptoms": {
        "english": [
            "face drooping", "facial droop", "arm weakness",
            "speech difficulty", "slurred speech", "sudden confusion",
            "sudden numbness", "vision loss suddenly", "stroke",
            "one side weakness", "one side paralysis", "facial numbness",
            "cannot speak", "trouble speaking",
        ],
        "hindi": [
            "मुंह टेढ़ा होना", "बोलने में दिक्कत", "लकवा",
            "एक तरफ कमजोरी", "अचानक बोलना बंद हो गया",
            "जुबान लड़खड़ाना",
        ],
        "marathi": [
            "तोंड वाकडे होणे", "बोलता न येणे", "पक्षघात",
            "एका बाजूला अशक्तपणा", "अचानक बोलणे बंद होणे",
        ],
        "hinglish": [
            "muh tedha ho gaya", "bolne mein dikkat",
            "lakwa", "ek taraf kamzori", "stroke ke symptoms",
        ],
    },

    # ── Gastrointestinal ──────────────────────────────────────────────────────

    "abdominal_pain": {
        "english": [
            "abdominal pain", "stomach pain", "stomach ache",
            "belly pain", "tummy ache", "pain in abdomen",
            "lower abdominal pain", "upper abdominal pain",
            "right side pain", "left side pain",
            "lower right pain", "lower left pain",
            "pain in stomach", "cramps",
        ],
        "hindi": [
            "पेट दर्द", "पेट में दर्द", "पेट में ऐंठन",
            "नीचे पेट में दर्द", "दाहिनी तरफ दर्द",
        ],
        "marathi": [
            "पोटात दुखणे", "पोटदुखी", "पोटात कळा येणे",
            "खालच्या भागात दुखणे",
        ],
        "hinglish": [
            "pet dard", "pet mein dard", "pet dard ho raha hai",
            "niche pet mein dard", "dayi taraf dard",
        ],
    },

    "vomiting": {
        "english": [
            "vomiting", "vomit", "nausea", "nauseous", "throwing up",
            "feeling sick", "want to vomit", "threw up",
            "puking", "retching",
        ],
        "hindi": [
            "उल्टी", "उलटी", "मतली", "जी मिचलाना", "मन मिचलाना",
            "उल्टी आना", "उल्टी हो रही है",
        ],
        "marathi": [
            "उलटी", "उलट्या होणे", "मळमळ", "जीव मळमळतो",
        ],
        "hinglish": [
            "ulti", "ulti ho rahi hai", "matli", "ji michilaana",
            "ji kharab hai",
        ],
    },

    "diarrhea": {
        "english": [
            "diarrhea", "diarrhoea", "loose motion", "loose stools",
            "frequent stools", "watery stools", "runny stools",
            "stomach running", "loose bowel",
        ],
        "hindi": [
            "दस्त", "पतले दस्त", "लूज मोशन", "पेचिश",
            "दस्त लगना", "बार बार मल आना",
        ],
        "marathi": [
            "जुलाब", "पातळ शौच", "वारंवार शौचास जाणे",
        ],
        "hinglish": [
            "dast", "loose motion", "patla dast", "baar baar toilet jana",
            "pait saaf nahi ho raha",
        ],
    },

    "constipation": {
        "english": [
            "constipation", "no bowel movement", "hard stools",
            "difficulty passing stool", "cannot pass stool",
            "bloating", "not able to pass motion",
        ],
        "hindi": [
            "कब्ज", "मल नहीं आना", "कब्जियत", "शौच में दिक्कत",
            "पेट साफ नहीं होना",
        ],
        "marathi": [
            "बद्धकोष्ठता", "शौच नाही होत", "पोट जड वाटते",
        ],
        "hinglish": [
            "kabz", "mal nahi aa raha", "shauchalay nahi ho raha",
            "pet saaf nahi hai",
        ],
    },

    "jaundice": {
        "english": [
            "jaundice", "yellow eyes", "yellow skin", "yellowing",
            "dark urine", "pale stools", "liver problem",
        ],
        "hindi": [
            "पीलिया", "आँखें पीली", "त्वचा पीली", "यकृत की समस्या",
        ],
        "marathi": [
            "काविळ", "डोळे पिवळे", "त्वचा पिवळी",
        ],
        "hinglish": [
            "piliya", "aankhein peeli", "skin peeli ho gayi",
        ],
    },

    # ── ENT ───────────────────────────────────────────────────────────────────

    "ear_pain": {
        "english": [
            "ear pain", "earache", "ear ache", "ear hurts",
            "pain in ear", "my ear hurts", "ear infection",
        ],
        "hindi": [
            "कान दर्द", "कान में दर्द", "कानों में दर्द",
        ],
        "marathi": [
            "कान दुखतो", "कानात दुखणे",
        ],
        "hinglish": [
            "kaan dard", "kaan mein dard", "kaan dard ho raha hai",
        ],
    },

    "ear_discharge": {
        "english": [
            "ear discharge", "fluid from ear", "pus from ear",
            "yellow discharge ear", "liquid coming from ear",
            "ear draining", "ear leaking",
        ],
        "hindi": [
            "कान से पानी आना", "कान से मवाद आना", "कान बहना",
        ],
        "marathi": [
            "कानातून पाणी येणे", "कानातून पू येणे",
        ],
        "hinglish": [
            "kaan se paani aa raha hai", "kaan se liquid nikal raha hai",
            "kaan beh raha hai",
        ],
    },

    "hearing_loss": {
        "english": [
            "hearing loss", "cannot hear", "hard of hearing",
            "deaf", "ringing in ear", "tinnitus",
            "muffled hearing", "hearing reduced",
        ],
        "hindi": [
            "सुनाई नहीं देना", "बहरापन", "कान में आवाज आना",
            "कम सुनाई देना",
        ],
        "marathi": [
            "ऐकू येत नाही", "बहिरेपणा", "कानात आवाज येतो",
        ],
        "hinglish": [
            "sunai nahi de raha", "bahra ho gaya",
            "kaan mein awaaz aa rahi hai",
        ],
    },

    "sore_throat": {
        "english": [
            "sore throat", "throat pain", "throat ache",
            "pain while swallowing", "difficulty swallowing",
            "throat infection", "tonsil pain", "tonsils swollen",
        ],
        "hindi": [
            "गले में दर्द", "गला दुखना", "निगलने में दिक्कत",
            "टॉन्सिल", "गला सूजा है",
        ],
        "marathi": [
            "घसा दुखतो", "घसा खवखवतो", "गिळताना दुखते",
        ],
        "hinglish": [
            "gale mein dard", "gala dukh raha hai",
            "nigalne mein dikkat", "tonsil dard",
        ],
    },

    "nosebleed": {
        "english": [
            "nosebleed", "nose bleed", "bleeding from nose",
            "blood from nose",
        ],
        "hindi": [
            "नाक से खून आना", "नाक से रक्त आना",
        ],
        "marathi": [
            "नाकातून रक्त येणे",
        ],
        "hinglish": [
            "naak se khoon aa raha hai", "naak se blood aa raha hai",
        ],
    },

    # ── Eye ───────────────────────────────────────────────────────────────────

    "eye_symptoms": {
        "english": [
            "eye pain", "red eye", "eye redness", "blurred vision",
            "vision loss", "cannot see", "double vision",
            "eye discharge", "watery eyes", "eye swelling",
            "eye infection", "pain in eye",
        ],
        "hindi": [
            "आँख दर्द", "आँखें लाल", "धुंधला दिखना",
            "दिखाई नहीं देता", "आँखों में सूजन",
        ],
        "marathi": [
            "डोळा दुखतो", "डोळे लाल", "अंधुक दिसते",
            "डोळ्यातून पाणी येते",
        ],
        "hinglish": [
            "aankh dard", "aankhein laal", "dhundhla dikhai de raha hai",
            "aankh mein dard",
        ],
    },

    # ── General / Systemic ────────────────────────────────────────────────────

    "fever": {
        "english": [
            "fever", "high temperature", "high fever", "temperature",
            "chills", "chills and fever", "shivering with fever",
            "running a fever", "feeling hot",
        ],
        "hindi": [
            "बुखार", "ताप", "तेज बुखार", "ठंड के साथ बुखार",
            "बदन गर्म है",
        ],
        "marathi": [
            "ताप", "जोराचा ताप", "थंडी ताप", "अंग गरम आहे",
        ],
        "hinglish": [
            "bukhar", "bukhaar", "tap", "tej bukhar",
            "thand ke saath bukhar", "body garam hai",
        ],
    },

    "weakness": {
        "english": [
            "weakness", "fatigue", "tired", "exhausted",
            "no energy", "body weakness", "feeling weak",
            "unable to stand", "cannot walk",
        ],
        "hindi": [
            "कमजोरी", "थकान", "बहुत थकान", "शरीर में कमजोरी",
            "खड़े नहीं हो पा रहे",
        ],
        "marathi": [
            "अशक्तपणा", "थकवा", "शरीर जड वाटते",
        ],
        "hinglish": [
            "kamzori", "thakan", "bahut thaka hua hun",
            "sharir mein kamzori hai",
        ],
    },

    "swelling": {
        "english": [
            "swelling", "swollen", "puffiness", "edema",
            "swollen feet", "swollen legs", "swollen face",
            "swollen hands",
        ],
        "hindi": [
            "सूजन", "सूजा हुआ", "पैरों में सूजन",
            "चेहरे पर सूजन",
        ],
        "marathi": [
            "सूज", "सूज आली", "पाय सुजले",
        ],
        "hinglish": [
            "sujan", "sooja hua", "pair mein sujan",
            "chehra sujan gaya",
        ],
    },

    # ── Musculoskeletal ───────────────────────────────────────────────────────

    "back_pain": {
        "english": [
            "back pain", "lower back pain", "upper back pain",
            "spine pain", "backache", "back ache",
        ],
        "hindi": [
            "पीठ दर्द", "कमर दर्द", "पीठ में दर्द",
        ],
        "marathi": [
            "पाठ दुखणे", "कंबर दुखणे",
        ],
        "hinglish": [
            "peeth dard", "kamar dard", "back mein dard",
        ],
    },

    "joint_pain": {
        "english": [
            "joint pain", "knee pain", "shoulder pain",
            "elbow pain", "wrist pain", "ankle pain",
            "hip pain", "arthritis", "joint swelling",
        ],
        "hindi": [
            "जोड़ों में दर्द", "घुटने में दर्द", "कंधे में दर्द",
            "जोड़ों में सूजन", "गठिया",
        ],
        "marathi": [
            "सांध्यात दुखणे", "गुडघा दुखतो",
        ],
        "hinglish": [
            "jodon mein dard", "ghutne mein dard",
            "kandhe mein dard", "gathiya",
        ],
    },

    "fracture": {
        "english": [
            "fracture", "broken bone", "broken arm", "broken leg",
            "bone pain", "fell down", "accident", "injury",
        ],
        "hindi": [
            "हड्डी टूटना", "फ्रैक्चर", "गिर गया",
            "चोट लगना", "दुर्घटना",
        ],
        "marathi": [
            "हाड मोडले", "फ्रॅक्चर", "पडलो", "दुखापत",
        ],
        "hinglish": [
            "haddi toot gayi", "fracture ho gaya", "gir gaya",
            "chot lagi", "accident hua",
        ],
    },

    # ── Skin ──────────────────────────────────────────────────────────────────

    "rash": {
        "english": [
            "rash", "skin rash", "itching", "itch", "hives",
            "skin eruption", "red spots", "blisters",
        ],
        "hindi": [
            "चकत्ते", "खुजली", "दाने", "त्वचा पर लाल धब्बे",
            "छाले",
        ],
        "marathi": [
            "पुरळ", "खाज येणे", "लाल चट्टे", "फोड",
        ],
        "hinglish": [
            "khujli", "daane", "skin rash", "laal daane",
            "chhale ho gaye",
        ],
    },

    "burns": {
        "english": [
            "burn", "burns", "burning skin", "scalded",
            "fire injury", "chemical burn",
        ],
        "hindi": [
            "जलना", "जलन", "आग से जलना", "जले हुए",
        ],
        "marathi": [
            "जळणे", "भाजणे",
        ],
        "hinglish": [
            "jal gaya", "jalan", "aag se jal gaya",
        ],
    },

    "skin_infection": {
        "english": [
            "skin infection", "wound infection", "abscess",
            "boil", "pus", "wound", "cut infected",
        ],
        "hindi": [
            "त्वचा संक्रमण", "घाव में मवाद", "फोड़ा", "फुंसी",
        ],
        "marathi": [
            "जखम", "जखमेत पू", "गळू",
        ],
        "hinglish": [
            "skin infection", "ghaav mein pus", "phoda",
        ],
    },

    # ── Emergency / Trauma ────────────────────────────────────────────────────

    "bleeding": {
        "english": [
            "bleeding", "blood", "hemorrhage", "heavy bleeding",
            "blood loss", "bleeding wound", "cut bleeding",
        ],
        "hindi": [
            "खून बहना", "रक्तस्राव", "खून", "घाव से खून बह रहा है",
        ],
        "marathi": [
            "रक्तस्राव", "रक्त वाहत आहे", "खून येतो",
        ],
        "hinglish": [
            "khoon beh raha hai", "blood nikal raha hai",
            "khoon", "bleeding ho rahi hai",
        ],
    },

    "allergic_reaction": {
        "english": [
            "allergic reaction", "allergy", "anaphylaxis",
            "throat swelling", "lips swelling", "tongue swelling",
            "hives after eating", "allergic to", "food allergy",
        ],
        "hindi": [
            "एलर्जी", "गले में सूजन", "होंठ सूजना",
            "खाने से एलर्जी",
        ],
        "marathi": [
            "ऍलर्जी", "घसा सुजणे", "ओठ सुजणे",
        ],
        "hinglish": [
            "allergy", "gale mein sujan", "hoth sujan gaye",
            "khane se allergy",
        ],
    },

    "snake_bite": {
        "english": [
            "snake bite", "snakebite", "bitten by snake",
            "snake bit me",
        ],
        "hindi": [
            "सांप काटना", "सर्पदंश", "सांप ने काटा",
        ],
        "marathi": [
            "सापाने चावणे", "साप चावला",
        ],
        "hinglish": [
            "saanp ne kaata", "snake ne kaata", "sarpadansh",
        ],
    },

    "dog_bite": {
        "english": [
            "dog bite", "bitten by dog", "animal bite",
            "dog bit me", "cat bite", "monkey bite",
        ],
        "hindi": [
            "कुत्ते ने काटा", "जानवर ने काटा", "बिल्ली ने काटा",
        ],
        "marathi": [
            "कुत्र्याने चावणे", "प्राण्याने चावणे",
        ],
        "hinglish": [
            "kutte ne kaata", "janwar ne kaata",
        ],
    },

    # ── Obstetrics & Gynecology ───────────────────────────────────────────────

    "pregnancy": {
        "english": [
            "pregnant", "pregnancy", "weeks pregnant",
            "months pregnant", "expecting", "expecting a baby",
        ],
        "hindi": [
            "गर्भवती", "प्रेगनेंट", "गर्भावस्था",
        ],
        "marathi": [
            "गर्भवती", "गरोदर",
        ],
        "hinglish": [
            "pregnant hun", "pregnancy hai", "garbhavati hun",
            "garbodar ahe",
        ],
    },

    "vaginal_bleeding": {
        "english": [
            "vaginal bleeding", "bleeding during pregnancy",
            "bleeding from vagina", "blood from vagina",
        ],
        "hindi": [
            "योनि से खून", "गर्भावस्था में खून आना",
        ],
        "marathi": [
            "गर्भावस्थेत रक्तस्राव",
        ],
        "hinglish": [
            "pregnancy mein bleeding", "yoni se khoon",
        ],
    },

    "labor_pain": {
        "english": [
            "labor pain", "labour pain", "contractions",
            "water broke", "water breaking", "birth pain",
            "delivery pain",
        ],
        "hindi": [
            "प्रसव पीड़ा", "दर्द हो रहा है बच्चे के", "पेट में तेज दर्द गर्भावस्था में",
        ],
        "marathi": [
            "प्रसूती वेदना", "कळा येत आहेत",
        ],
        "hinglish": [
            "prasav peeda", "delivery pain", "contractions ho rahe hain",
        ],
    },

    "reduced_fetal_movement": {
        "english": [
            "baby not moving", "reduced fetal movement",
            "fetus not moving", "baby movement reduced",
            "no movement from baby",
        ],
        "hindi": [
            "बच्चा हिल नहीं रहा", "गर्भ में हलचल नहीं",
        ],
        "marathi": [
            "बाळ हालत नाही",
        ],
        "hinglish": [
            "bacha hil nahi raha", "baby move nahi kar raha",
        ],
    },

    # ── Urinary ───────────────────────────────────────────────────────────────

    "urinary_symptoms": {
        "english": [
            "burning urination", "burning while urinating",
            "burning sensation while urinating", "burning sensation urinating",
            "pain while urinating", "pain when urinating",
            "frequent urination", "blood in urine", "urine infection", "uti",
            "urinary tract infection", "difficulty urinating",
            "cannot urinate",
        ],
        "hindi": [
            "पेशाब में जलन", "बार-बार पेशाब", "पेशाब में खून",
            "पेशाब करने में दिक्कत",
        ],
        "marathi": [
            "लघवीला जळजळ", "वारंवार लघवी", "लघवीत रक्त",
        ],
        "hinglish": [
            "peshab mein jalan", "baar baar peshab", "urine mein khoon",
            "peshab karne mein dikkat", "uti hai",
        ],
    },

    # ── Dental ────────────────────────────────────────────────────────────────

    "toothache": {
        "english": [
            "toothache", "tooth pain", "tooth ache", "gum pain",
            "dental pain", "broken tooth", "gum swelling",
        ],
        "hindi": [
            "दांत दर्द", "दांत में दर्द", "मसूड़ों में दर्द",
        ],
        "marathi": [
            "दात दुखणे", "हिरड्या दुखतात",
        ],
        "hinglish": [
            "daant dard", "daant mein dard", "masoodon mein dard",
        ],
    },
}


# ── Severity modifiers ────────────────────────────────────────────────────────
# These words boost severity to "severe" when found near symptom text.

SEVERITY_SEVERE: List[str] = [
    "severe", "worst", "extreme", "unbearable", "excruciating",
    "very bad", "terrible", "intense",
    "बहुत तेज", "असहनीय", "बहुत ज़्यादा",
    "खूप तीव्र", "असह्य",
    "bahut tej", "asahneey", "bahut zyada",
]

SEVERITY_MILD: List[str] = [
    "mild", "slight", "a little", "minor",
    "हल्का", "थोड़ा", "कम",
    "सौम्य",
    "halka", "thoda",
]


# ── Emergency indicator phrases ───────────────────────────────────────────────
# If ANY of these appear in text, flag as potential emergency regardless of
# other routing logic.

EMERGENCY_PHRASES: List[str] = [
    # English
    "cannot breathe", "can't breathe", "not breathing",
    "chest pain radiating", "crushing chest",
    "unconscious", "not responding", "unresponsive", "collapsed",
    "severe bleeding", "heavy bleeding", "losing blood",
    "stroke", "face drooping", "arm weakness and speech",
    "anaphylaxis", "throat closing", "throat swelling",
    "snake bite", "snakebite",
    "seizure", "convulsion", "fits",
    "water broke", "labor pain", "delivery now",
    "baby not moving", "no fetal movement",
    "overdose", "poisoning", "swallowed poison",
    "heart attack", "cardiac arrest",
    "road accident", "hit by vehicle",
    # Hindi
    "सांस नहीं आ रही", "बेहोश", "खून बंद नहीं हो रहा",
    "दौरे पड़ रहे हैं", "मुंह टेढ़ा हो गया",
    "सांप ने काटा", "जहर खाया",
    # Marathi
    "श्वास घेता येत नाही", "बेशुद्ध", "साप चावला",
    # Hinglish
    "saans nahi aa rahi", "behosh ho gaya", "khoon band nahi ho raha",
    "saanp ne kaata", "daure pad rahe hain",
]

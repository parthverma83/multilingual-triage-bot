# 🏥 MedRoute AI

> **Multilingual Medical Triage — Powered by Sarvam-2B + LoRA**

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live%20Demo-medroute--retrocat.streamlit.app-red?style=for-the-badge&logo=streamlit)](https://medroute-retrocat.streamlit.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render)](https://medroute-ai-p8hm.onrender.com/health)
[![GitHub](https://img.shields.io/badge/GitHub-multilingual--triage--bot-181717?style=for-the-badge&logo=github)](https://github.com/parthverma83/multilingual-triage-bot)
[![Tests](https://img.shields.io/badge/Tests-45%2F45%20Passing-28a745?style=for-the-badge)](#testing)
[![Languages](https://img.shields.io/badge/Languages-English%20%7C%20Hindi%20%7C%20Marathi%20%7C%20Hinglish-blue?style=for-the-badge)](#multilingual-support)

</div>

---

## What is MedRoute AI?

MedRoute AI routes patients to the correct hospital department based on symptoms described in natural language — in **English, Hindi, Marathi, or Hinglish**.

A patient types:

> *"मुझे सीने में दर्द हो रहा है"*

And gets back:

```
🚨 आपातकाल — तुरंत चिकित्सकीय सहायता लें

Department  →  हृदय रोग विभाग
Priority    →  आपातकाल
Tests       →  ईसीजी · ट्रोपोनिन · जीवन संकेत जांच
```

No translation API. No external NLP service. Everything runs on a custom multilingual medical dictionary built for Indian healthcare.

---

## Architecture

```
Patient (any language)
        │
        ▼
┌───────────────────┐
│  Streamlit UI     │  streamlit.app  (public)
└────────┬──────────┘
         │ HTTP POST /triage
         ▼
┌───────────────────────────────────────────┐
│           FastAPI Backend                 │  Render (public)
│                                           │
│  ① Language Detection   (pure regex)      │
│  ② Text Normaliser      (Unicode NFC)     │
│  ③ Symptom Extractor    (48 symptoms)     │
│       ↑ Medical Dictionary                │
│         EN · HI · MR · Hinglish          │
│  ④ Emergency Detector   (4 rules)        │
│  ⑤ Department Router    (12 depts)       │
│  ⑥ Deterministic Fallback  ◄─── always  │
└──────────────────┬────────────────────────┘
                   │ HTTPS /generate
                   ▼
         Cloudflare Tunnel
                   │
                   ▼
┌───────────────────────────────────────────┐
│     Google Colab — Tesla T4 GPU           │
│                                           │
│  Sarvam-2B v0.5  (4-bit NF4 quantised)   │
│  + LoRA Adapter  (rank 16 · 91 MB)        │
│  trained with Unsloth on triage data      │
└───────────────────────────────────────────┘
```

**Safety guarantee:** If the AI model fails or times out, the deterministic layer always returns a valid clinical response. The system never crashes.

---

## Features

| Feature | Detail |
|---|---|
| 🌐 Multilingual input | English, Hindi (Devanagari), Marathi (Devanagari), Hinglish |
| 🌐 Multilingual output | Department names, priority, advice translated to patient's language |
| 🧠 48 canonical symptoms | Across 4 language layers, no external NLP library |
| 🏥 12 departments | Cardiology, ENT, Neurology, OB/GYN, General Surgery, and more |
| 🚨 Emergency detection | 4 clinical rules + 30+ emergency phrases across all languages |
| 🛡️ Deterministic fallback | AI enhances, never replaces the safety layer |
| ⚡ Staged loading | 6-step animation during inference so the UI never looks frozen |
| 📊 Confidence bar | Visual confidence score per response |

---

## Multilingual Support

The system works natively in four language layers — no translation API involved.

| Language | Example Input | Output Language |
|---|---|---|
| English | `I have chest pain radiating to my left arm` | English |
| Hindi | `मुझे सीने में दर्द हो रहा है` | Hindi |
| Marathi | `मला ३२ आठवड्यांची गर्भवती... रक्तस्राव होत आहे` | Marathi |
| Hinglish | `kaan dard ho raha hai aur paani nikal raha hai` | English |

---

## Clinical Scenario Coverage

| Symptom | Department | Priority |
|---|---|---|
| Chest pain radiating to left arm | Cardiology | 🔴 Emergency |
| Fever for 3 days with chills | General Medicine | 🟢 Routine |
| Ear pain with yellow discharge | ENT | 🟡 Routine |
| Severe lower right abdominal pain | General Surgery | 🔴 Emergency |
| 32 weeks pregnant with bleeding | Obstetrics & Gynecology | 🔴 Emergency |
| Face drooping, cannot speak | Neurology | 🔴 Emergency |
| Snake bite | Emergency | 🔴 Emergency |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Python · Streamlit |
| Backend | Python · FastAPI · Uvicorn |
| NLP Pipeline | Custom regex + Medical Dictionary (zero external deps) |
| AI Model | Sarvam-2B v0.5 (AI4Bharat) |
| Fine-tuning | LoRA rank 16, trained with Unsloth |
| Quantisation | BitsAndBytes 4-bit NF4 |
| GPU | NVIDIA Tesla T4 via Google Colab |
| Tunnel | Cloudflare cloudflared (free tier) |
| HTTP client | httpx (async + retry) |
| Hosting | Streamlit Community Cloud + Render |

---

## Testing

```
45 tests · 0 failures · runs in 0.12s
```

```
TestEnglish    ████████████████  16/16
TestHindi      █████████          9/9
TestMarathi    ██████             6/6
TestHinglish   ███████            7/7
TestEdgeCases  ███████            7/7
```

Run tests yourself:

```bash
python -m pytest backend/services/tests/test_medical_pipeline.py -v
```

---

## Running Locally

### Prerequisites

- Python 3.11+
- Google Colab session (for GPU inference)

### 1. Clone

```bash
git clone https://github.com/parthverma83/multilingual-triage-bot.git
cd multilingual-triage-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install streamlit httpx
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env — set MODEL_ENDPOINT to your Colab Cloudflare URL
```

### 4. Start Colab inference server

Open `Sarvam_Inference_Server.ipynb` in Google Colab:
- Runtime → T4 GPU
- Run all cells
- Copy the Cloudflare URL from Cell 7
- Paste into `.env` as `MODEL_ENDPOINT`

### 5. Start backend

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Start frontend

```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501`

---

## Project Structure

```
multilingual-triage-bot/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── api/routes.py
│   ├── schemas/
│   └── services/
│       ├── medical_dictionary.py    ← 48 symptoms × 4 languages
│       ├── text_normalizer.py       ← Unicode NFC + Hinglish
│       ├── symptom_extractor.py     ← compiled regex pipeline
│       ├── emergency_detector.py    ← clinical rule engine
│       ├── department_router.py     ← 12-department routing
│       ├── translations.py          ← multilingual output
│       ├── triage_engine.py         ← orchestrator
│       └── tests/
│           └── test_medical_pipeline.py
├── frontend/
│   └── app.py                       ← Streamlit UI
├── Sarvam_Inference_Server.ipynb    ← Colab GPU server
├── render.yaml                      ← Render deployment config
├── START_PROJECT.md                 ← startup guide
└── docs/
    ├── viva_complete.md
    ├── presentation_6_slides.md
    └── E3_demo_script.md
```

---

## Deployment

| Service | URL |
|---|---|
| Frontend | [medroute-retrocat.streamlit.app](https://medroute-retrocat.streamlit.app) |
| Backend | [medroute-ai-p8hm.onrender.com](https://medroute-ai-p8hm.onrender.com) |
| Inference | Google Colab T4 via Cloudflare tunnel |

---

## Team Retrocat

Built as a Final Year Project · 2025–26

---

## Disclaimer

MedRoute AI is a research prototype. It has not been clinically validated and is not approved for use in real clinical settings. Always consult a licensed medical professional for health decisions.

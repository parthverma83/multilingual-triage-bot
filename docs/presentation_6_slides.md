# MedRoute AI — 6-Slide Presentation

---

## SLIDE 1 — Title

**Heading:**
# MedRoute AI
### Multilingual Medical Triage Using Fine-Tuned Indic LLM

**Subtext:**
> Powered by Sarvam-2B + LoRA · Streamlit · FastAPI · Tesla T4 GPU

**Bottom line:**
`[Your Name] · Final Year Project · [Institute Name] · 2025–26`

**Visual suggestion:**
- Dark background (navy or black)
- A simple icon: stethoscope or hospital cross
- One thin horizontal line separating title from subtitle

---

## SLIDE 2 — The Problem

**Heading:** Why Medical Triage Needs AI

**Left column — The Numbers:**
| Stat | Value |
|---|---|
| India OPD visits / year | ~550 million |
| Average wait time | 2–4 hours |
| Patients with non-emergency cases | ~30% |
| India's official languages | 22 |

**Right column — The Gap:**
```
❌ Long queues — no smart routing
❌ Triage done manually by overworked staff
❌ Most AI tools only work in English
❌ Rural patients cannot describe symptoms in English
```

**Bottom callout box:**
> **The problem:** A patient describes symptoms in Hindi or Marathi.
> The system doesn't understand. They wait 3 hours to see the wrong doctor.

**Speaker note:**
"India has 22 official languages. Most medical AI only works in English. We built a system that meets the patient where they are."

---

## SLIDE 3 — System Architecture

**Heading:** How MedRoute AI Works

**Diagram (draw as vertical flow):**

```
[ Patient types symptoms ]
     ↓  (English / Hindi / Marathi / Hinglish)

[ Streamlit Frontend ]
     ↓  HTTP POST /triage

[ FastAPI Backend ]
  ├─ Language Detection
  ├─ Text Normalisation (Unicode, Hinglish variants)
  ├─ Symptom Extraction  ← Medical Dictionary (48 symptoms × 4 languages)
  ├─ Emergency Detector  ← Clinical Rule Engine
  └─ Department Router   ← 12 specialties

     ↓  Structured prompt (ChatML)

[ Cloudflare Tunnel ]
     ↓

[ Google Colab — Tesla T4 GPU ]
  └─ Sarvam-2B + LoRA Adapter
     (2B params · 4-bit quantised · 91 MB adapter)

     ↓  JSON response

[ Translated Output in Patient's Language ]
```

**Key callout:**
> **Safety guarantee:** If the AI model fails, the deterministic layer always returns a safe fallback. The system never crashes.

**Speaker note:**
"The most important design decision: deterministic intelligence runs first. The AI model enhances it — but never replaces the safety layer."

---

## SLIDE 4 — Technical Highlights

**Heading:** What Makes This Different

**4 boxes (2×2 grid):**

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│  🧠 Fine-Tuned Indic LLM   │  │  🌐 True Multilingual NLP   │
│                             │  │                             │
│  Sarvam-2B v0.5             │  │  48 canonical symptoms      │
│  LoRA rank 16, alpha 16     │  │  4 language layers:         │
│  4-bit NF4 quantisation     │  │  English · Hindi ·          │
│  91 MB adapter              │  │  Marathi · Hinglish         │
│  Runs on T4 GPU (4 GB VRAM) │  │  No external NLP library    │
└─────────────────────────────┘  └─────────────────────────────┘

┌─────────────────────────────┐  ┌─────────────────────────────┐
│  🏥 Clinical Rule Engine   │  │  ✅ 45 Automated Tests      │
│                             │  │                             │
│  Emergency detection        │  │  English · Hindi ·          │
│  4 clinical rules           │  │  Marathi · Hinglish ·       │
│  30+ emergency phrases      │  │  Edge cases                 │
│  12-department routing      │  │  All 45 pass                │
│  Graceful AI fallback       │  │  ~0.1 second run time       │
└─────────────────────────────┘  └─────────────────────────────┘
```

**Speaker note:**
"The NLP pipeline has zero external dependencies. No spaCy, no NLTK, no API calls — just compiled regex against a medical dictionary we built. This means it works offline and has deterministic, auditable behavior."

---

## SLIDE 5 — Results & Demo

**Heading:** Live System — Multilingual Triage in Action

**Table of tested scenarios:**

| Input Language | Symptom | Department | Priority |
|---|---|---|---|
| English | Chest pain radiating to left arm | Cardiology | 🔴 Emergency |
| Hindi | सीने में दर्द हो रहा है | हृदय रोग विभाग | 🔴 आपातकाल |
| Marathi | मला ३२ आठवड्यांची गर्भवती... | प्रसूती व स्त्रीरोग विभाग | 🔴 आपत्कालीन |
| Hinglish | kaan dard ho raha hai | ENT | 🟡 Routine |
| English | Fever for 3 days with chills | General Medicine | 🟢 Routine |
| Marathi | श्वास घेता येत नाही | — | 🔴 आपत्कालीन |

**Performance:**

| Metric | Value |
|---|---|
| End-to-end response time | ~6.5 seconds |
| Model inference (T4 GPU) | ~5.5 seconds |
| NLP pipeline | < 5 ms |
| Departments supported | 12 |
| Languages supported | 4 |
| Test pass rate | 45 / 45 (100%) |

**Speaker note:**
"The 6.5 second response time is dominated by GPU inference over a free Cloudflare tunnel. On a dedicated A100, this would drop below 500ms."

---

## SLIDE 6 — Conclusion & Future Work

**Heading:** What We Built · What Comes Next

**Left — What we built:**
```
✅ End-to-end multilingual triage AI
✅ Fine-tuned Sarvam-2B with LoRA
✅ 48-symptom multilingual medical dictionary
✅ Clinical rule engine with emergency detection
✅ Graceful fallback — never fails hard
✅ Translated output in patient's language
✅ 45 automated tests, all passing
✅ Full stack: Streamlit → FastAPI → GPU
```

**Right — Future work:**
```
→ Tamil · Telugu · Bengali support
→ Dedicated GPU (sub-1s inference)
→ Mobile app for rural healthcare workers
→ Patient history across sessions
→ Integration with hospital HIS systems
→ Clinical validation by licensed physicians
→ Regulatory review for deployment
```

**Bottom callout:**
> **This project demonstrates the feasibility of AI-powered multilingual triage for India's healthcare system — using open-source models, modest compute, and a safety-first architecture.**

**Final speaker line:**
"MedRoute AI is not a finished clinical product — it is a proof of concept that shows this is technically possible with open-source Indic AI. Thank you."

---

## Design Notes (for Canva / PowerPoint)

**Color palette:**
- Background: `#0d1117` (dark navy) or white
- Accent: `#4fa3e0` (medical blue)
- Emergency red: `#ff4444`
- Routine green: `#28a745`
- Text: white on dark / `#1e1e1e` on light

**Font:**
- Heading: Inter Bold or Poppins Bold
- Body: Inter Regular or Roboto

**Slide size:** 16:9 widescreen

**Logo placement:** Top-right corner, every slide (🏥 MedRoute AI)

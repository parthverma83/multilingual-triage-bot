# MedRoute AI — 5-Minute Demo Script

## Before you start

- Colab running, Cloudflare URL updated in .env
- Backend running: `python -m uvicorn backend.app:app --reload --port 8000`
- Streamlit running: `python -m streamlit run frontend/app.py`
- Browser open at `http://localhost:8501`
- Green dot visible: **Backend connected**

---

## Minute 0:00 – 0:45 | Problem Statement

> "India sees roughly 550 million OPD visits per year.
> The average patient waits 2–4 hours before seeing a doctor,
> yet 30% of those patients have non-emergency conditions.
>
> The core problem is triage — figuring out which patient
> needs which doctor, and how quickly.
>
> The second problem is language. India has 22 official languages.
> Most triage systems only work in English.
> Our patients speak Hindi, Marathi, Tamil, Bengali.
>
> MedRoute AI solves both problems."

---

## Minute 0:45 – 1:30 | Architecture Overview

Point to the whiteboard / architecture diagram.

> "The system has three main layers.
>
> First, a Streamlit frontend — clean, simple, works in any browser.
>
> Second, a FastAPI backend with what I call the Medical Intelligence Layer.
> This is a deterministic clinical rule engine that runs before the AI model.
> It extracts symptoms, detects emergencies, and routes to the right department
> using a multilingual medical dictionary covering English, Hindi, Marathi, and Hinglish.
>
> Third, a fine-tuned Sarvam-2B model running on a Tesla T4 GPU.
> Sarvam-2B is a 2-billion parameter Indic language model from AI4Bharat.
> We fine-tuned it with LoRA on medical triage data.
>
> Crucially, even if the AI model fails, the system never crashes.
> The deterministic layer always provides a safe fallback."

---

## Minute 1:30 – 3:00 | Live Demo — English

Type into the UI:

**Input 1:**
```
I have severe chest pain radiating to my left arm
```

> "Watch what happens."

Point to the result:
- Red emergency banner → "This is the safety system working. Chest pain with radiation to the left arm is a classic MI presentation."
- Department: **Cardiology**, Priority: **Emergency**
- Recommended tests: ECG, Troponin

---

**Input 2:**
```
I have fever for 3 days with chills
```

> "Compare this — no emergency. Routine. General Medicine. 
> The system correctly distinguishes between a life-threatening cardiac event
> and a standard fever presentation."

---

## Minute 3:00 – 4:00 | Live Demo — Multilingual

**Input 3 (Hindi):**
```
मुझे सीने में दर्द हो रहा है
```

> "Same scenario, in Hindi. No code change, no translation API.
> The medical dictionary handles this natively."

Show result → Cardiology / Emergency

---

**Input 4 (Hinglish):**
```
mujhe seene mein dard ho raha hai aur saans lene mein dikkat hai
```

> "Hinglish — the way millions of Indians actually type.
> Mixed romanised Hindi. The system still routes correctly."

Show result → Cardiology / Emergency

---

**Input 5 (Marathi):**
```
मला 3 दिवसांपासून ताप आहे
```

> "Marathi. Fever for 3 days. General Medicine. Routine."

---

## Minute 4:00 – 4:30 | Resilience Demo (optional — only if examiner asks)

Stop the Colab server (stop Cell 8 in Colab).

Type a symptom. Show that:
- The app doesn't crash
- The deterministic fallback returns a valid department
- The user never sees a traceback

> "Even if the GPU server is unavailable, the system degrades gracefully.
> The deterministic layer still gives a valid clinical recommendation."

Restart Colab before continuing.

---

## Minute 4:30 – 5:00 | Closing

> "To summarise:
>
> MedRoute AI is a production-ready multilingual medical triage system.
> It combines a fine-tuned Indic language model with a deterministic clinical
> safety layer, supports 4 languages natively, routes to 12 specialties,
> and never fails hard.
>
> The immediate next step is replacing Google Colab with a dedicated GPU server
> for sub-second inference, and expanding the multilingual dictionary to
> Tamil, Telugu, and Bengali.
>
> Thank you."

---

## Backup inputs (if examiner asks to test more)

| Input | Expected |
|---|---|
| `My ear hurts and there is yellow discharge` | ENT |
| `I am 32 weeks pregnant and bleeding` | Obstetrics & Gynecology / Emergency |
| `I was bitten by a snake` | Emergency |
| `saans nahi aa rahi hai` | Emergency |
| `I have difficulty breathing and my lips are swelling` | Emergency (allergic reaction) |
| `severe pain in lower right abdomen` | General Surgery / Emergency |
| `कान में दर्द हो रहा है` | ENT |
| `श्वास घेता येत नाही` | Emergency |

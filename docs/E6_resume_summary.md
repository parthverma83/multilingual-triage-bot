# MedRoute AI — Resume & Portfolio Summary

---

## Resume Bullet Points

**For technical roles (SDE, ML Engineer, Backend):**

> Built MedRoute AI, a multilingual medical triage system using a fine-tuned Sarvam-2B Indic LLM with LoRA adapters, deployed on a Tesla T4 GPU via a FastAPI inference server and Cloudflare tunnel. Engineered a deterministic NLP pipeline covering 48 canonical symptoms across English, Hindi, Marathi, and Hinglish; implemented a clinical rule engine for emergency detection and department routing with 100% test coverage (45 tests). Stack: Python, FastAPI, Streamlit, HuggingFace Transformers, PEFT, BitsAndBytes, httpx, Docker.

---

**For AI/ML roles:**

> Fine-tuned Sarvam-2B (2B-parameter Indic LLM) for multilingual medical triage using LoRA (rank 16) and 4-bit NF4 quantisation via BitsAndBytes, reducing VRAM requirement from 16 GB to 4 GB with negligible accuracy loss. Built a deterministic fallback layer to guarantee safe outputs when the model fails. Deployed on Google Colab T4 GPU with Cloudflare tunnel and exposed via a FastAPI REST API.

---

**Short version (LinkedIn headline style):**

> Final Year Project: MedRoute AI — Multilingual Medical Triage using Fine-tuned Sarvam-2B + LoRA on GPU. Python · FastAPI · Streamlit · HuggingFace · Docker.

---

## LinkedIn Project Description

**Project Name:** MedRoute AI — Multilingual Medical Triage System

**Duration:** Final Year (2025-2026)

**Description:**
MedRoute AI is an end-to-end AI system that routes patients to the correct medical department based on symptoms described in natural language — in English, Hindi, Marathi, or Hinglish.

**What I built:**
- Fine-tuned Sarvam-2B (an Indic LLM from AI4Bharat) using LoRA on medical triage data
- 4-bit quantised model serving via FastAPI on a Tesla T4 GPU
- A deterministic medical NLP pipeline with a multilingual symptom dictionary (48 symptoms × 4 languages)
- Clinical rule engine for emergency detection and routing to 12 medical specialties
- Streamlit frontend with staged loading, emergency banner, confidence bar, and session history
- Cloudflare tunnel for exposing the Colab GPU server via a public HTTPS endpoint
- 45-test multilingual regression suite covering English, Hindi, Marathi, Hinglish, and edge cases

**Key design decision:**  
The system never fails hard. A deterministic fallback always runs before the AI model call. If the model is unavailable, the NLP pipeline still returns a safe clinical recommendation.

**Tech stack:**  
Python · FastAPI · Streamlit · HuggingFace Transformers · PEFT · BitsAndBytes · httpx · Docker · Cloudflare · Google Colab T4

---

## GitHub README One-Liner

> MedRoute AI — Multilingual medical triage using fine-tuned Sarvam-2B + LoRA. Routes patients to the correct department from symptoms in English, Hindi, Marathi, or Hinglish. Built with FastAPI, Streamlit, and deployed on a T4 GPU via Cloudflare tunnel.

---

## Interview Talking Points (30-second version)

> "For my final year project I built a medical triage AI that routes patients to the right department from symptoms typed in English, Hindi, Marathi, or Hinglish.
>
> The core is a fine-tuned Sarvam-2B language model — an Indic LLM — running on a GPU with LoRA adapters.
>
> What I'm most proud of is the architecture: the system has a deterministic NLP layer that runs before the AI. So even if the GPU server goes down, the system never crashes — it falls back to rule-based clinical routing.
>
> We have 45 multilingual tests across all four languages and all pass."

---

## Skills Demonstrated (for CV skills section)

**Languages:** Python  
**Frameworks:** FastAPI, Streamlit, HuggingFace Transformers, PEFT  
**AI/ML:** LLM fine-tuning, LoRA, 4-bit quantisation, BitsAndBytes, prompt engineering  
**Backend:** REST API design, async Python, httpx, Uvicorn  
**DevOps:** Docker, Cloudflare tunnel, environment configuration  
**Testing:** pytest, multilingual test suite design  
**NLP:** Regex-based extraction, Unicode normalization, multilingual vocabulary design  
**Tools:** Git, Google Colab, VS Code

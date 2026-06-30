# MedRoute AI — Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER / PATIENT                               │
│              (Any language: English, Hindi, Marathi, Hinglish)      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │  Types symptoms in natural language
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND                              │
│                     localhost:8501                                  │
│                                                                     │
│  • Language selector (auto / en / hi / mr / te / ta / bn)          │
│  • Staged loading animation (6 steps)                               │
│  • Emergency banner  •  Department card  •  Confidence bar         │
│  • Reasoning  •  Recommended tests  •  Session history             │
└───────────────────────────────┬─────────────────────────────────────┘
                                │  HTTP POST /triage
                                │  { message, language }
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                                 │
│                     localhost:8000                                  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              MEDICAL INTELLIGENCE LAYER                      │   │
│  │                                                              │   │
│  │  ① Language Detector   → detects script / language          │   │
│  │                                                              │   │
│  │  ② Text Normalizer     → Unicode NFC, Hinglish variants     │   │
│  │                                                              │   │
│  │  ③ Symptom Extractor   → 48 canonical symptoms              │   │
│  │       ↑ reads from Medical Dictionary                        │   │
│  │       (English + Hindi + Marathi + Hinglish)                │   │
│  │                                                              │   │
│  │  ④ Emergency Detector  → 4 clinical rules + phrase scan     │   │
│  │                                                              │   │
│  │  ⑤ Department Router   → 12 departments, priority-ordered   │   │
│  │                                                              │   │
│  │  ⑥ Deterministic Fallback built before AI call              │   │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 │  Structured prompt (ChatML)       │
│                                 ▼                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              HTTP INFERENCE CLIENT                            │  │
│  │         (HttpInferenceService — httpx + retry logic)         │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────────┘
                                  │  HTTPS POST /generate
                                  │  (Cloudflare tunnel)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CLOUDFLARE TUNNEL                                 │
│           *.trycloudflare.com  (free, no account needed)            │
│           TLS termination  •  Public HTTPS endpoint                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                │  HTTP to localhost:8001
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   GOOGLE COLAB (T4 GPU)                             │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  FASTAPI INFERENCE SERVER                      │ │
│  │                      port 8001                                 │ │
│  └──────────────────────────────┬────────────────────────────────┘ │
│                                 │                                   │
│  ┌──────────────────────────────▼────────────────────────────────┐ │
│  │               SARVAM-2B BASE MODEL                             │ │
│  │          sarvamai/sarvam-2b-v0.5  (4-bit NF4 quantised)       │ │
│  │          bfloat16  •  ~4 GB VRAM                               │ │
│  └──────────────────────────────┬────────────────────────────────┘ │
│                                 │  PEFT adapter                    │
│  ┌──────────────────────────────▼────────────────────────────────┐ │
│  │               LoRA ADAPTER  (MedRoute v1)                      │ │
│  │          rank=16  •  alpha=16  •  91 MB safetensors           │ │
│  │          trained with Unsloth on medical triage data           │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Python · Streamlit |
| Backend | Python · FastAPI · Uvicorn |
| NLP Pipeline | Custom (regex + dictionary, no external NLP library) |
| AI Model | Sarvam-2B v0.5 (Indic LLM, 2B parameters) |
| Fine-tuning | LoRA rank 16, trained with Unsloth |
| Quantisation | BitsAndBytes 4-bit NF4 |
| GPU | NVIDIA Tesla T4 (16 GB VRAM) via Google Colab |
| Tunnel | Cloudflare cloudflared (free tier) |
| HTTP client | httpx (async, retry logic) |
| Model serving | FastAPI + Uvicorn (Colab side) |

## Key Design Decisions

**Deterministic-first architecture**  
Every request runs through the Medical Intelligence Layer before the AI model is called.  
If the model fails, times out, or returns malformed JSON, the deterministic result is returned as fallback.  
This means the system never crashes — it degrades gracefully.

**Language-agnostic canonical symptoms**  
The Medical Dictionary maps 48 canonical symptom IDs across 4 language layers.  
Emergency detection and department routing operate on IDs, not raw text.  
Adding a new language requires only a new vocabulary section in one file.

**Provider-agnostic inference client**  
`HttpInferenceService` talks to any HTTP endpoint that accepts `{ prompt }` and returns `{ generated_text }`.  
Switching from Colab to a dedicated GPU server requires changing one `.env` line.

# MedRoute AI — Request Sequence Diagram

## Happy Path (Model Available)

```
Patient     Streamlit     FastAPI      Intelligence    Colab
  │             │            │             Layer          │
  │ types       │            │               │            │
  │ symptoms    │            │               │            │
  │────────────▶│            │               │            │
  │             │ POST       │               │            │
  │             │ /triage    │               │            │
  │             │───────────▶│               │            │
  │             │            │               │            │
  │             │ [loading   │ detect_lang() │            │
  │             │  stages    │──────────────▶│            │
  │             │  animate]  │               │            │
  │             │            │ normalize()   │            │
  │             │            │──────────────▶│            │
  │             │            │               │            │
  │             │            │ extract_symptoms()         │
  │             │            │──────────────▶│            │
  │             │            │               │            │
  │             │            │ detect_emergency()         │
  │             │            │──────────────▶│            │
  │             │            │               │            │
  │             │            │ route_department()         │
  │             │            │──────────────▶│            │
  │             │            │ ◀─────────────│            │
  │             │            │ deterministic │            │
  │             │            │ fallback ready│            │
  │             │            │               │            │
  │             │            │ POST /generate│            │
  │             │            │ (ChatML prompt)            │
  │             │            │───────────────────────────▶│
  │             │            │               │ T4 GPU     │
  │             │            │               │ inference  │
  │             │            │               │ ~5-6 sec   │
  │             │            │◀───────────────────────────│
  │             │            │ { generated_text: "..." }  │
  │             │            │               │            │
  │             │            │ validate_and_normalize()   │
  │             │            │ (parse JSON from LLM)      │
  │             │            │               │            │
  │             │            │ enforce emergency rules    │
  │             │            │ (deterministic override)   │
  │             │            │               │            │
  │             │◀───────────│               │            │
  │             │ TriageResponse             │            │
  │             │ { department, priority,    │            │
  │             │   emergency, confidence,   │            │
  │             │   reasoning, tests }       │            │
  │◀────────────│            │               │            │
  │ sees result │            │               │            │
```

## Fallback Path (Model Unavailable / Timeout)

```
Patient     Streamlit     FastAPI      Intelligence    Colab
  │             │            │             Layer       [DOWN]
  │ types       │            │               │            │
  │ symptoms    │            │               │            │
  │────────────▶│            │               │            │
  │             │────────────▶               │            │
  │             │            │ deterministic result built │
  │             │            │ [same as happy path]       │
  │             │            │               │            │
  │             │            │ POST /generate             │
  │             │            │───────────────────────────▶│
  │             │            │               │ timeout /  │
  │             │            │               │ connection │
  │             │            │◀──────────────────────────x│
  │             │            │ exception caught            │
  │             │            │ model_output = {}          │
  │             │            │               │            │
  │             │            │ validate_and_normalize()   │
  │             │            │ → falls back to            │
  │             │            │   deterministic result     │
  │             │◀───────────│               │            │
  │             │ TriageResponse (deterministic)          │
  │◀────────────│            │               │            │
  │ sees result │            │               │            │
  │ (no error)  │            │               │            │
```

## Latency Budget

| Step | Time |
|---|---|
| Language detection | < 1 ms |
| Text normalization | < 1 ms |
| Symptom extraction (pattern match) | < 5 ms |
| Emergency detection | < 1 ms |
| Department routing | < 1 ms |
| Prompt construction | < 1 ms |
| HTTP to Colab (network) | ~100-200 ms |
| T4 GPU inference (Sarvam-2B) | ~5,000-6,000 ms |
| Response parsing + validation | < 5 ms |
| **Total end-to-end** | **~5,500-6,500 ms** |

> The dominant cost is GPU inference. On a dedicated A100 GPU this would drop to ~500ms.  
> On a locally hosted quantised model it would be ~1,500ms.

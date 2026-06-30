# MedRoute AI — Viva Preparation

## Core Architecture

**Q: Why did you choose Sarvam-2B instead of a larger model like GPT-4?**

Three reasons.
First, Sarvam-2B is specifically pre-trained on Indic languages — it understands Hindi, Marathi, and other Indian languages natively, which GPT-4 handles less well for regional dialects.
Second, a 2B parameter model can be fine-tuned and run on a single T4 GPU, making it accessible without expensive infrastructure.
Third, for a structured classification task like triage, a smaller fine-tuned model consistently outperforms a larger general-purpose model.

---

**Q: What is LoRA and why did you use it instead of full fine-tuning?**

LoRA — Low-Rank Adaptation — freezes the original model weights and adds small trainable matrices to the attention layers.
The rank-16 adapter we trained is only 91 MB, compared to the ~4 GB base model.
Full fine-tuning would require much more GPU memory and time.
LoRA achieves comparable results in a fraction of the compute and is reversible — the base model is untouched.

---

**Q: What is 4-bit quantisation and what does it trade off?**

Quantisation reduces the precision of model weights from 32-bit floats to 4-bit integers.
This cuts memory usage by roughly 8x, allowing Sarvam-2B to fit in 4 GB of VRAM instead of 16 GB.
We use NF4 (Normal Float 4) with double quantisation, which minimises accuracy loss.
The trade-off is a slight reduction in output quality, which in practice is undetectable for triage-style structured outputs.

---

**Q: Why did you add a deterministic layer instead of relying entirely on the LLM?**

LLMs can hallucinate — they may return malformed JSON, wrong department names, or miss emergencies in their output.
In a medical context, a missed emergency is dangerous.
The deterministic layer is a clinical safety net:
- It runs before the model call, building a guaranteed valid response
- If the model fails, times out, or returns garbage, the fallback is returned instead
- Emergency flags from the deterministic layer always override the model's output

This is a standard pattern in production AI systems — the AI enhances but doesn't replace deterministic safety logic.

---

**Q: What is ChatML format?**

ChatML is a prompt format used to structure multi-turn conversations for language models:
```
<|im_start|>system
You are a medical triage assistant...
<|im_end|>
<|im_start|>user
Patient symptoms...
<|im_end|>
<|im_start|>assistant
```
The model is trained to complete the assistant block.
We use this because Sarvam-2B was fine-tuned with this format.

---

## Technical Depth

**Q: How does your multilingual symptom extraction work?**

We built a Medical Dictionary with 48 canonical symptom IDs.
Each symptom has phrase lists in English, Hindi (Devanagari), Marathi (Devanagari), and Hinglish (romanised).
At import time, we compile one regex per symptom that ORs all phrases across all languages.
The normalizer first runs Unicode NFC composition and Hinglish spelling unification.
Then we search the normalised text against all 48 patterns simultaneously.
This gives us O(n) extraction where n is the number of symptoms, regardless of language.

---

**Q: How do you detect emergencies?**

Two passes.
First, canonical symptom IDs — if any of 13 emergency symptom IDs appear (chest pain, shortness of breath, stroke symptoms, seizure, snake bite, etc.), the emergency flag is set.
Second, a raw text phrase scan using a compiled regex of 30+ emergency phrases across all languages.
This catches cases where the phrase extractor missed a symptom but the raw text is still clearly dangerous (e.g. "cannot breathe" typed in a non-standard way).
Additionally, pregnancy combined with any of bleeding, abdominal pain, or labor pain is always flagged as an emergency.

---

**Q: How do you handle the case where the model returns invalid JSON?**

The response validator in `response_validator.py` tries multiple strategies:
1. Direct JSON parse of the full response
2. Regex extraction of the first JSON object found in the text
3. If both fail, it uses the deterministic fallback response

The model is instructed in the system prompt to return only valid JSON, but LLMs don't always comply.

---

**Q: What is Cloudflare tunnel and why did you use it?**

Cloudflare tunnel (`cloudflared`) creates a secure public HTTPS endpoint that proxies traffic to a local port.
We use it to expose the Colab GPU server (which has no public IP) to the internet without port forwarding or a paid service.
The free tier generates a random subdomain like `https://xxxx.trycloudflare.com`.
The limitation is that the URL changes every session, requiring a `.env` update each time.

---

**Q: How would you move this to production?**

Three changes:
1. Replace Colab + Cloudflare with a dedicated GPU server (RunPod, Lambda Labs, or cloud GPU)
2. Replace the Cloudflare URL with a stable domain
3. Add authentication to the FastAPI backend

The codebase is already provider-agnostic — `HttpInferenceService` talks to any URL that implements the `/generate` endpoint.

---

## Dataset and Training

**Q: What data did you use to fine-tune the model?**

Medical triage conversations covering OPD scenarios across specialties.
The training data was structured as ChatML-formatted JSON with symptom input and structured JSON output containing department, priority, emergency flag, reasoning, and recommended tests.

---

**Q: How did you evaluate model performance?**

Two levels.
First, automated — 45 unit tests across the full NLP pipeline covering English, Hindi, Marathi, Hinglish, and edge cases. All 45 pass.
Second, manual regression — live end-to-end tests through the UI covering all major clinical scenarios.

---

## Design Decisions

**Q: Why Streamlit instead of React or a mobile app?**

For a final-year project demo, Streamlit allows rapid iteration without frontend development overhead.
The architecture is decoupled — the Streamlit app is a thin client that calls the FastAPI backend.
Replacing it with a React frontend or a Flutter mobile app would require only changing the HTTP client, not the backend or AI layer.

---

**Q: What are the limitations of your current system?**

Four main limitations:
1. Colab GPU disconnects after ~12 hours of inactivity, requiring a manual restart
2. Inference latency is 6–7 seconds due to the free T4 GPU and Cloudflare routing overhead
3. The multilingual dictionary doesn't yet cover Tamil, Telugu, or Bengali
4. The model has not been evaluated by medical professionals — it is a research prototype, not a clinical tool

---

**Q: What would you do differently if you had 3 more months?**

1. Expand the training dataset with verified medical cases
2. Add a medical professional validation pipeline
3. Deploy on a dedicated GPU with a stable endpoint (target: sub-1-second latency)
4. Add Tamil, Telugu, and Bengali to the multilingual dictionary
5. Build a mobile app for last-mile healthcare workers
6. Add patient history context across sessions

---

## The Hardest Question

**Q: Is this safe to use in a hospital?**

No — not in its current form, and I want to be clear about that.

This is a research prototype. It has not been clinically validated. It has not been approved by any medical regulatory body.

What it demonstrates is the feasibility of the architecture: that a fine-tuned Indic language model with a deterministic safety layer can accurately perform preliminary triage across multiple languages.

Before any clinical deployment, this would need: validation by licensed physicians, clinical trials, regulatory approval, audit logging, and integration with existing hospital information systems.

The value of this project is the architecture and the proof of concept — showing that this is technically possible with open-source models and modest compute.

# MedRoute AI — Complete Viva Preparation

Read each question. Say the answer out loud. If you can't say it fluently, read it again.
The goal is not to memorise — it is to understand so deeply you can answer any version of the question.

---

# PART 1 — The Basics (Every viva starts here)

---

**Q: What is your project? Explain it in one sentence.**

MedRoute AI is a multilingual medical triage system that takes patient symptoms described in English, Hindi, Marathi, or Hinglish and routes them to the correct hospital department using a fine-tuned Indic language model combined with a clinical rule engine.

---

**Q: What problem are you solving?**

Two problems. First, Indian hospitals have long OPD queues because triage is done manually — there is no smart system to decide which patient needs which doctor first. Second, most AI-based triage tools only work in English, which excludes the majority of Indian patients who communicate in Hindi, Marathi, or other regional languages. We built a system that solves both.

---

**Q: Why did you choose this topic?**

Medical triage is one of the highest-impact applications of NLP because it directly affects patient outcomes. The multilingual problem is unsolved in the Indian healthcare context — existing systems assume English input. We had access to an Indic language model (Sarvam-2B) that could be fine-tuned, and we wanted to demonstrate that this is achievable with accessible compute, not just large cloud infrastructure.

---

**Q: What is the novelty of your project?**

Three things. One — we fine-tuned Sarvam-2B, an Indic LLM, specifically for medical triage, which has not been done publicly at this scale. Two — we built a multilingual medical dictionary from scratch covering 48 symptoms across four language layers with no external NLP dependency. Three — the deterministic-first architecture ensures the system is always safe, even when the AI model fails. Most student projects either use an API (no real AI work) or fine-tune a model (no real engineering work). We did both, and added a clinical safety layer on top.

---

**Q: Who would use this?**

Two audiences. Primary — hospital reception or triage nurses who take patient details and need to quickly route them to the right department. Secondary — a patient-facing kiosk or mobile app at rural healthcare centres where a health worker could describe symptoms in a local language and get a routing recommendation.

---

# PART 2 — The AI Model

---

**Q: What is Sarvam-2B?**

Sarvam-2B is a 2-billion parameter language model developed by AI4Bharat and Sarvam AI, specifically pre-trained on Indic languages including Hindi, Marathi, Tamil, Telugu, Bengali, and others, alongside English. Unlike general models that treat Indian languages as a secondary concern, Sarvam-2B has native Indic language capability. The "v0.5" version we used is publicly available on HuggingFace under the model ID `sarvamai/sarvam-2b-v0.5`.

---

**Q: What is fine-tuning? What did you fine-tune it on?**

Fine-tuning is the process of taking a pre-trained model and continuing to train it on a smaller, task-specific dataset so it learns to perform a particular job. We fine-tuned Sarvam-2B on medical triage conversations — patient symptom descriptions paired with structured JSON outputs containing the correct department, priority, emergency flag, reasoning, and recommended tests. The model learns to map from natural language symptoms to this structured clinical output.

---

**Q: What is LoRA? Why did you use it?**

LoRA stands for Low-Rank Adaptation. Instead of updating all 2 billion parameters during fine-tuning — which requires enormous GPU memory and time — LoRA freezes the original model weights and adds small trainable matrices called adapters to the attention layers. These adapters have a much lower rank, meaning far fewer trainable parameters. We used rank 16, which produced an adapter file of only 91 MB, compared to the 4 GB base model. The result is comparable to full fine-tuning, but faster and more memory efficient. It also means the base model is untouched — the adapter can be removed or swapped.

---

**Q: What is 4-bit quantisation? What does NF4 mean?**

Quantisation reduces the numerical precision of model weights. Normally weights are stored as 32-bit floats. We reduce them to 4-bit integers, which cuts memory by roughly 8 times. NF4 stands for Normal Float 4 — a quantisation format designed by Tim Dettmers that minimises accuracy loss by using a data type whose distribution matches how neural network weights are actually distributed (normally distributed). We also used double quantisation, which quantises the quantisation constants themselves, saving an additional ~0.4 GB. The total result: Sarvam-2B fits in about 4 GB of VRAM instead of 16 GB, allowing it to run on a free Colab T4 GPU.

---

**Q: What is BitsAndBytes?**

BitsAndBytes is a Python library developed by Tim Dettmers that provides efficient implementations of quantisation for transformer models. We use its `BitsAndBytesConfig` class to configure 4-bit NF4 quantisation when loading the model with HuggingFace Transformers. It handles the quantisation transparently — the model is loaded in 4-bit but computations are done in bfloat16.

---

**Q: What is PEFT?**

PEFT stands for Parameter-Efficient Fine-Tuning, a HuggingFace library that implements LoRA and other adapter methods. We use its `PeftModel.from_pretrained()` to load our LoRA adapter on top of the quantised base model. PEFT wraps the base model and routes forward passes through the adapter layers without modifying the underlying weights.

---

**Q: What is ChatML format?**

ChatML is a conversation markup format used to structure prompts for instruction-tuned language models. A typical prompt looks like:
```
<|im_start|>system
You are a medical triage assistant. Return only valid JSON.
<|im_end|>
<|im_start|>user
Patient symptoms: chest pain radiating to left arm
<|im_end|>
<|im_start|>assistant
```
The model is trained to complete the assistant block. We use this because Sarvam-2B was fine-tuned with this format. The `<|im_start|>` and `<|im_end|>` tokens are special tokens the model has learned to associate with role boundaries.

---

**Q: Why not use GPT-4 or Gemini?**

Three reasons. One — GPT-4 and Gemini are closed-source APIs, which means we cannot fine-tune them on custom medical data without enterprise access. Two — they are English-first models; their Indic language capability is weaker than a model pre-trained on Indic corpora. Three — for a final-year project demonstrating AI engineering skills, using an API is not meaningful — anyone can call an API. Fine-tuning a model demonstrates real understanding of the training process.

---

**Q: Why not use a larger model like LLaMA-70B?**

A 70B parameter model requires approximately 40 GB of VRAM even after 4-bit quantisation, which exceeds the capacity of any free GPU tier. The T4 GPU on Colab has 16 GB VRAM. A 2B parameter model is the right size for the available infrastructure, and for a structured output task like triage classification, a well-fine-tuned smaller model consistently outperforms a larger general-purpose model.

---

# PART 3 — The Architecture

---

**Q: Explain the full system architecture.**

The system has four layers. First, a Streamlit frontend running at port 8501 in the browser — this is the patient-facing interface. Second, a FastAPI backend at port 8000 that contains the Medical Intelligence Layer. Third, a Cloudflare tunnel that exposes a local inference server on Google Colab to the internet. Fourth, the Colab server running Sarvam-2B with the LoRA adapter on a T4 GPU.

When a patient submits symptoms, the frontend sends an HTTP POST to the backend. The backend runs language detection, text normalisation, symptom extraction, emergency detection, and department routing — all deterministically, with no AI involved. It builds a safe fallback response. Then it sends a structured prompt to the Colab inference server via the Cloudflare URL. The model generates a JSON response, the backend validates it, applies emergency overrides, translates everything to the patient's language, and returns the final response to the frontend.

---

**Q: What is the deterministic layer and why is it important?**

The deterministic layer is a sequence of rule-based processing steps that runs before the AI model is called. It includes language detection, text normalisation, symptom extraction using our medical dictionary, emergency detection using clinical rules, and department routing. The result of this is a complete, valid triage response — before the AI has done anything.

This matters for two reasons. First, if the AI model fails, times out, or returns malformed output, the deterministic result is returned as fallback. The user never sees an error. Second, the emergency flag and priority from the deterministic layer always override the model's output. This means a missed emergency in the AI response is corrected by the safety layer.

---

**Q: What is FastAPI? Why did you use it over Flask?**

FastAPI is a modern Python web framework for building REST APIs. It is asynchronous by default, supports Python type hints natively, generates automatic OpenAPI documentation, and has built-in request validation via Pydantic. We used it over Flask because the async support is important — when waiting for the Colab model response (5+ seconds), FastAPI can handle other requests concurrently. Flask is synchronous by default and would block.

---

**Q: What is Cloudflare tunnel? How does it work?**

Google Colab runs on a remote server with no public IP address and no port forwarding. To expose its local port 8001 to the internet, we run `cloudflared`, a command-line tool from Cloudflare. It establishes an outbound connection from Colab to Cloudflare's edge network and receives a public URL like `https://xxxx.trycloudflare.com`. All traffic to that URL is forwarded through the tunnel to Colab's port 8001. It is free, requires no account, and takes about 3 seconds to set up. The limitation is that the URL changes every session.

---

**Q: Why Google Colab instead of a dedicated GPU server?**

Colab provides a free T4 GPU with 16 GB VRAM, which is sufficient for running Sarvam-2B at 4-bit quantisation. A dedicated GPU server like RunPod or Lambda Labs would cost money and require configuration. For a final-year project demo, Colab is practical. The architecture is designed to be provider-agnostic — the `HttpInferenceService` class talks to any URL that implements the `/generate` endpoint, so switching to a dedicated server requires changing one line in the `.env` file.

---

**Q: What is Streamlit?**

Streamlit is a Python library for building interactive web applications without writing HTML, CSS, or JavaScript. You write Python and Streamlit renders it as a browser UI. We use it for the frontend because it lets us focus on the AI and backend logic rather than frontend development. For a final-year project, this is the right trade-off. The backend is completely decoupled — any frontend (React, Flutter, etc.) could replace Streamlit by calling the same FastAPI endpoints.

---

# PART 4 — The NLP Pipeline

---

**Q: How does your multilingual symptom extraction work?**

We built a Medical Dictionary — a Python file containing 48 canonical symptom identifiers, each with phrase lists in four languages: English, Hindi (Devanagari), Marathi (Devanagari), and Hinglish (romanised). For example, the symptom `chest_pain` has English phrases like "chest pain", "pain in chest", "tightness in chest"; Hindi phrases like "सीने में दर्द", "छाती में दर्द"; Marathi phrases like "छातीत दुखणे"; and Hinglish phrases like "seene mein dard", "chhaati mein dard".

At import time, we compile one regex pattern per symptom that ORs all phrases across all languages. The text normaliser first applies Unicode NFC composition and Hinglish spelling standardisation. Then we match the normalised text against all 48 patterns. This runs in under 5 milliseconds regardless of input language.

---

**Q: What is Unicode NFC normalisation?**

In Unicode, some characters can be represented in multiple ways. For example, the Devanagari character "साँ" (with chandrabindu) and "सां" (with anusvara) are visually similar but have different Unicode codepoints. If our dictionary contains one form and the user types the other, a simple string match fails. NFC (Canonical Decomposition followed by Canonical Composition) recomposes split characters into their standard forms. We also explicitly unify chandrabindu (U+0901) to anusvara (U+0902) since they are nearly identical in medical context.

---

**Q: What is Hinglish and how do you handle it?**

Hinglish is romanised Hindi — Hindi typed in English script, which is extremely common in India on mobile keyboards where users don't switch to Devanagari. Examples: "bukhar" for बुखार, "seene mein dard" for सीने में दर्द. We handle it with two mechanisms. First, Hinglish phrase lists in the Medical Dictionary. Second, a spelling normaliser that maps common variants — "bukhaar" → "bukhar", "khansi" / "khanshi" → "khansi", "saans" / "sans" / "saas" → "saans". The language detector also recognises Hinglish by checking for romanised Hindi markers.

---

**Q: How does emergency detection work?**

Four rules. Rule 1: if any of 13 emergency symptom IDs are present (chest pain, shortness of breath, stroke symptoms, seizure, snake bite, labor pain, vaginal bleeding, etc.), flag as emergency. Rule 2: if pregnancy is detected alongside bleeding, abdominal pain, or labor pain, flag as emergency — this is a specific obstetric rule. Rule 3: if severity is severe and the symptom is abdominal pain, headache, or back pain, escalate to emergency. Rule 4: scan the raw text against 30+ emergency phrases across all languages — this catches cases where the symptom extractor missed something but the phrase "cannot breathe" or "behosh ho gaya" is still present.

---

**Q: How does department routing work?**

The router receives the extracted symptom list, detected body part, and severity. It applies rules in priority order — most specific first. Pregnancy or labor pain → Obstetrics & Gynecology. Chest pain or heart palpitations → Cardiology. Stroke or seizure → Neurology. Headache or dizziness → Neurology. Ear, discharge, or throat symptoms → ENT. Severe abdominal pain → General Surgery. Fractures → Orthopaedics. And so on for 12 departments. General Medicine is the default catch-all. First match wins and returns immediately — no scoring, no ambiguity.

---

**Q: How does the output translation work?**

The system processes everything internally using canonical English identifiers. Department names, priority labels, reasoning strings, and test names are all English throughout the pipeline. Just before returning the response, a translation function looks up each field in a static translation dictionary and replaces it with the patient's language equivalent. For example, "Cardiology" → "हृदय रोग विभाग" in Hindi, "हृदयरोग विभाग" in Marathi. Dynamic strings like "Symptoms present for 3 days" use templates: "लक्षण 3 दिन से हैं" in Hindi. No AI translation is used — everything is pre-defined, consistent, and instantaneous.

---

# PART 5 — Testing & Results

---

**Q: How did you test the system?**

Two levels. First, 45 automated unit tests in pytest covering the full NLP pipeline — symptom extraction, emergency detection, and department routing — across English, Hindi, Marathi, Hinglish, and edge cases. All 45 pass and run in under 0.2 seconds. Second, manual end-to-end testing through the Streamlit UI across all major clinical scenarios to verify the full stack including the AI model and translation layer.

---

**Q: What is your accuracy?**

For the deterministic pipeline — 100% on our 45 test cases, which cover the scenarios we designed the system for. For the AI model output — we do not have a formal accuracy metric because we do not have a labelled test dataset of real patient cases. What we can say is that when the model output disagrees with the deterministic routing, the deterministic result is used as the final answer. This means the system's department routing accuracy equals the deterministic layer's accuracy on our test suite.

---

**Q: What is the latency?**

End-to-end response time is approximately 6.5 seconds. The NLP pipeline takes under 5 milliseconds. The network round-trip to Colab via Cloudflare adds around 150 milliseconds. The T4 GPU inference for Sarvam-2B takes approximately 5.5 seconds for a triage prompt. On a dedicated A100 GPU this would drop to under 500 milliseconds. On a locally hosted quantised model on a modern CPU it would be around 15–20 seconds.

---

**Q: What clinical scenarios did you test?**

Cardiology emergency (chest pain radiating to left arm), General Medicine routine (fever with chills), ENT (ear pain with discharge), General Surgery (severe lower right abdominal pain), Obstetrics emergency (32 weeks pregnant with bleeding), Neurology (stroke symptoms, seizure), snake bite emergency, shortness of breath, and several others. We also tested all scenarios in Hindi, Marathi, and Hinglish to verify multilingual routing.

---

# PART 6 — The Hard Questions

---

**Q: Is this system safe to use in a real hospital?**

No, not in its current form, and I want to be clear about that. This is a research prototype. It has not been clinically validated, has not been reviewed by licensed physicians, and has not received any regulatory approval. A missed emergency or wrong department routing in a real hospital could harm a patient.

What this project demonstrates is feasibility — that a fine-tuned Indic LLM combined with a deterministic clinical safety layer can accurately perform preliminary triage routing. Before any deployment, this would require clinical trials, physician validation, audit logging, integration with hospital information systems, and regulatory approval under India's Medical Device Rules.

---

**Q: What if the model gives the wrong answer?**

Two safety mechanisms. First, the deterministic layer always produces a fallback before the model is called. If the model output is wrong or malformed, the fallback is used. Second, the emergency flag from the deterministic layer overrides the model. So even if the model says "routine," if the clinical rules detect an emergency, the response will say Emergency. The model can only influence the department name and reasoning — it cannot remove an emergency flag that the rule engine set.

---

**Q: What are the limitations of your system?**

Five main limitations. One — the Colab GPU disconnects after 12 hours, requiring a manual restart and URL update. Two — inference latency is 6.5 seconds, which is slow for a real triage desk. Three — the multilingual dictionary covers only English, Hindi, Marathi, and Hinglish — Tamil, Telugu, and Bengali are not supported yet. Four — the model was not validated by medical professionals. Five — the training dataset is limited; the model may not generalise well to rare or complex presentations.

---

**Q: How is this different from just calling ChatGPT?**

Three fundamental differences. One — Sarvam-2B is fine-tuned on medical triage data, so it produces structured JSON in the expected format reliably. ChatGPT would require careful prompt engineering and still may not produce consistent output. Two — we have a deterministic safety layer that runs independently of the AI. ChatGPT has no such fallback. Three — Sarvam-2B is an Indic model with native Hindi and Marathi understanding. ChatGPT handles these languages but was not pre-trained on them as a primary corpus.

Also — in a real hospital deployment, sending patient symptom data to OpenAI's servers would be a HIPAA/DISHA data privacy violation. A self-hosted model avoids this entirely.

---

**Q: Why not use a translation API (Google Translate) and just work in English?**

We considered this. The problem is medical terminology. Google Translate may translate "सांस लेने में दिक्कत" correctly, but it will lose regional dialect nuance and Hinglish transliteration entirely. It also introduces an external API dependency, adds latency, costs money at scale, and creates a privacy issue — patient symptoms sent to a third-party API. Our approach — a medical dictionary with native multilingual vocabulary — is faster, free, offline-capable, and has predictable, auditable behaviour.

---

**Q: What would you do differently if you had six more months?**

Four things. One — build a proper labelled evaluation dataset with physician-verified correct routings across all departments and languages. Two — expand the multilingual dictionary to Tamil, Telugu, and Bengali. Three — deploy on a dedicated GPU with a stable endpoint and measure real latency. Four — conduct a pilot with actual patients or healthcare workers to collect qualitative feedback on output quality and usability.

---

**Q: Can you explain what Unsloth is?**

Unsloth is a library that accelerates LoRA fine-tuning — it provides optimised CUDA kernels that make training 2–5x faster and use less memory. We used it during the training phase. However, the trained adapter files are standard PEFT/LoRA format — we load them using standard HuggingFace transformers and PEFT at inference time, without Unsloth. This is important because Unsloth's model loading had validation issues with local paths that we bypassed by using standard PEFT for inference.

---

**Q: What is httpx and why did you use it instead of requests?**

httpx is a modern Python HTTP client that supports both synchronous and asynchronous requests. We use it in `HttpInferenceService` for async HTTP calls to the Colab inference server. The `requests` library is synchronous only — in a FastAPI async endpoint, a synchronous HTTP call blocks the event loop and prevents the server from handling other requests during the 5-second GPU wait. httpx with `async with httpx.AsyncClient()` allows FastAPI to remain responsive while waiting for the model.

---

# PART 7 — Questions You Should Ask Back

If an examiner gives you time to ask a question, ask one of these — it shows maturity:

- "In your view, what would be the most important validation step before this could be used in a clinical setting?"
- "Are there existing hospital triage systems in India that a solution like this could integrate with?"
- "Would you see more value in the multilingual NLP layer or the fine-tuned model — which do you think is more novel?"

---

# PART 8 — One-Line Answers (for rapid-fire rounds)

| Question | Answer |
|---|---|
| What model did you use? | Sarvam-2B v0.5 by AI4Bharat, fine-tuned with LoRA |
| What is LoRA? | Adapters that train < 1% of parameters, 91 MB vs 4 GB |
| What is 4-bit quantisation? | Compress weights to 4 bits, 8x memory reduction |
| What GPU did you use? | NVIDIA Tesla T4, 16 GB VRAM, Google Colab free tier |
| How many languages? | 4: English, Hindi, Marathi, Hinglish |
| How many symptoms? | 48 canonical symptoms in the medical dictionary |
| How many departments? | 12 |
| How many tests? | 45 automated tests, all pass |
| What is the latency? | ~6.5 seconds end-to-end |
| What framework is the backend? | FastAPI |
| What framework is the frontend? | Streamlit |
| What if the AI fails? | Deterministic fallback always returns a safe response |
| Is it safe for hospitals? | No — research prototype, not clinically validated |
| What is Cloudflare tunnel? | Free tool to expose Colab's local port to the internet |
| What is ChatML? | Prompt format with role markers for instruction-tuned models |

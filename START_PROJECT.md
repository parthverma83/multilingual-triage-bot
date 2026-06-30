# MedRoute AI — Startup Guide

Every session requires 3 things to be running:
1. Colab inference server
2. FastAPI backend
3. Streamlit frontend

Total setup time: ~8 minutes (most of it is model loading).

---

## Step 1 — Start Colab Inference Server (~6 min)

1. Open Google Colab
2. Open `Sarvam_Inference_Server.ipynb`
3. Runtime → Change runtime type → **T4 GPU**
4. Run all cells top to bottom (Cells 1–8)
5. Wait for Cell 4 to print:
   ```
   ✅ Model loaded successfully
   ```
6. Cell 7 will print a URL like:
   ```
   URL: https://xxxx-xxxx.trycloudflare.com
   ```
7. **Copy that URL.**
8. Run Cell 8 (keep alive) — leave this running.

---

## Step 2 — Update Backend Config (30 seconds)

Open this file:

```
C:\Users\Parth\OneDrive\Desktop\project ieee\triage-bot\.env
```

Update this line with the URL from Step 1:

```env
MODEL_ENDPOINT=https://xxxx-xxxx.trycloudflare.com
```

Save the file.

---

## Step 3 — Start FastAPI Backend

Open PowerShell and run:

```powershell
cd "C:\Users\Parth\OneDrive\Desktop\project ieee\triage-bot"
& "C:\Users\Parth\AppData\Local\Python\bin\python3.14-64.exe" -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Wait for:
```
INFO: Application startup complete.
```

Leave this window open.

---

## Step 4 — Start Streamlit Frontend

Open a **second** PowerShell window and run:

```powershell
cd "C:\Users\Parth\OneDrive\Desktop\project ieee\triage-bot"
& "C:\Users\Parth\AppData\Local\Python\bin\python3.14-64.exe" -m streamlit run frontend/app.py
```

Browser opens at `http://localhost:8501`

Verify the green dot shows: **Backend connected**

---

## Step 5 — Verify Everything Works

Type this into the UI:

```
I have severe chest pain radiating to my left arm
```

Expected result:
- Department: **Cardiology**
- Priority: **Emergency**
- Tests: ECG, Troponin

If this works, the full system is live.

---

## Shutdown

- Stop Streamlit: `Ctrl+C` in its PowerShell window
- Stop Backend: `Ctrl+C` in its PowerShell window
- Stop Colab: Runtime → Disconnect and delete runtime

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Green dot is red (Backend offline) | Run Step 3 |
| Request times out | Colab disconnected — repeat Step 1 |
| `Module not found: backend` | Make sure you `cd` to the `triage-bot` folder first |
| Colab URL changed | Update `.env` and restart backend (Steps 2 + 3) |
| Port 8000 already in use | Close the old PowerShell window or restart PC |

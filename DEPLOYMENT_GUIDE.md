# Sprint 7: GPU Deployment Guide

## Overview
This guide walks through deploying the Medical AI Triage System to RunPod with GPU inference.

**Current State:** Docker build in progress locally. Once complete, you'll push to a registry and deploy to RunPod.

---

## Step 7.1: Docker Build Status

The build is downloading the NVIDIA CUDA base image (~2GB). This is normal and expected.

**Monitoring:**
```bash
docker ps  # Check running containers
docker images  # Check completed images
```

**Expected Output When Build Completes:**
```
Successfully tagged triage-inference:latest
```

---

## Step 7.2: Push to Registry (Once Build Completes)

### Option A: Docker Hub (Recommended for simplicity)

1. **Create an account** at https://hub.docker.com/ (if you don't have one)

2. **Login locally:**
   ```bash
   docker login
   # Enter your Docker Hub username and password
   ```

3. **Tag the image:**
   ```bash
   docker tag triage-inference:latest <your-dockerhub-username>/triage-inference:latest
   ```

4. **Push:**
   ```bash
   docker push <your-dockerhub-username>/triage-inference:latest
   ```

### Option B: GitHub Container Registry

1. **Create a GitHub Personal Access Token:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select `write:packages` scope
   - Copy the token

2. **Login locally:**
   ```bash
   echo "<your-token>" | docker login ghcr.io -u <your-github-username> --password-stdin
   ```

3. **Tag:**
   ```bash
   docker tag triage-inference:latest ghcr.io/<your-github-username>/triage-inference:latest
   ```

4. **Push:**
   ```bash
   docker push ghcr.io/<your-github-username>/triage-inference:latest
   ```

---

## Step 7.3: Create RunPod GPU Pod

### 1. Go to https://www.runpod.io/

### 2. Sign Up / Log In

### 3. Click "GPU Pods" → "Create Pod"

### 4. Select a Template

Choose **"Pytorch"** or **"Custom CUDA"** template.

### 5. Configure Pod

**Template (or custom):**
```
Name: triage-inference
Image: <your-registry-image>  # e.g., your-username/triage-inference:latest
```

**GPU Selection:**
- **Recommended:** RTX A4000 (sufficient for 2B model) or RTX A5000
- **Budget Option:** RTX 3080 (minimum)

**Volume Settings:**
- **Container Disk:** 50GB (for model weights)
- **Volume Disk:** 10GB (for logs, optional)

**Environment Variables:**
```
SKIP_MODEL_LOAD=false
LORA_PATH=/models/sarvam_triage_lora
MODEL_NAME=sarvam-triage-v1
BASE_MODEL=sarvamai/sarvam-2b-v0.5
```

**Ports:**
- Expose port `8001` (inference API)

### 6. Start the Pod

Click "Deploy" and wait for the pod to initialize (2-5 minutes).

### 7. Verify Inference Service is Running

Once the pod is running:

```bash
curl https://<runpod-url>/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model": "sarvam-triage-v1",
  "base_model": "sarvamai/sarvam-2b-v0.5"
}
```

---

## Step 7.4: Update Backend Configuration

Update `.env` in your backend:

```env
APP_NAME=MedRoute AI
APP_VERSION=1.0.0

MODEL_PROVIDER=runpod
MODEL_ENDPOINT=https://<runpod-url>  # Copy from RunPod dashboard
MODEL_API_KEY=

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=triage_db
```

---

## Step 7.5: Test Backend → Inference Connection

### Start Backend Locally:

```bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Test Endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a severe chest pain and shortness of breath",
    "language": "en"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "department": "cardiology",
  "confidence": 0.92,
  "reasoning": "Severe chest pain with dyspnea suggests cardiac emergency"
}
```

---

## Step 7.6: Deploy Full Stack Locally (Optional)

To test the complete system with Docker Compose locally (without GPU):

```bash
docker-compose up -d
```

This will start:
- Backend (port 8000)
- Inference service (port 8001) - will be in `SKIP_MODEL_LOAD=true` mode
- MySQL (port 3306)

Monitor logs:
```bash
docker-compose logs -f
```

---

## Step 7.7: Troubleshooting

### Issue: "Model not loading"

**Check RunPod pod logs:**
```bash
# In RunPod dashboard, click "Connect" → "View Logs"
```

**Ensure environment variables are set:**
```bash
LORA_PATH=/models/sarvam_triage_lora
SKIP_MODEL_LOAD=false
```

### Issue: "Timeout connecting to inference service"

**Verify URL is correct:**
- Copy from RunPod dashboard (should look like: `https://xxxxx.runpod.io`)
- Test health endpoint first

**Check firewall:**
- Port 8001 must be exposed in RunPod pod settings

### Issue: "CUDA out of memory"

**Solutions:**
1. Increase GPU memory quota in RunPod
2. Reduce batch size (currently 1, which is fine for 2B model)
3. Use smaller GPU pod (RTX 3090)

---

## Deployment Checklist

Before going live:

- [ ] Docker image builds successfully locally
- [ ] Image pushed to registry (Docker Hub or GHCR)
- [ ] RunPod pod created and running
- [ ] Model loads successfully on RunPod (`/health` returns `loaded: true`)
- [ ] Backend connects to RunPod endpoint (test `/triage` endpoint)
- [ ] Response latency is <5 seconds
- [ ] Error handling works (test with malformed input)
- [ ] Logging captures request IDs and latencies
- [ ] `.env` file updated with RunPod endpoint

---

## Next Steps (Sprint 8)

Once deployment is verified:

1. Connect Streamlit frontend to backend
2. Add MySQL persistence layer
3. Test multilingual queries (English, Hindi, Marathi)
4. Performance profiling and optimization
5. Documentation and demo scripts

---

## Questions?

If you encounter issues:

1. **Check logs**: `docker logs <container-id>` (local) or RunPod dashboard (remote)
2. **Test in isolation**: Use `curl` to test each endpoint independently
3. **Verify configuration**: Double-check `.env` values match your RunPod setup

**Good luck with the deployment!**

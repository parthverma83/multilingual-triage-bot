# Sprint 7 Implementation Checklist

## PHASE 1: Local Docker Build ✅ IN PROGRESS

### Step 7.1: Docker Build
- [ ] `docker build` completes successfully
  - Expected output: `Successfully tagged triage-inference:latest`
  - Time: 10-20 minutes (first time, includes CUDA download)
  - Disk space needed: ~8GB free

### Step 7.2: Verify Image
```bash
docker images | grep triage-inference
docker image inspect triage-inference:latest
```

Expected output:
```
REPOSITORY              TAG       IMAGE ID      SIZE
triage-inference        latest    <hash>        ~2.5GB
```

---

## PHASE 2: Local Testing

### Step 7.3: Test Container Locally (No GPU)

```bash
# Set environment to skip model loading
docker run -p 8001:8001 \
  -e SKIP_MODEL_LOAD=true \
  triage-inference:latest
```

Test health endpoint:
```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": false,
  "model": "sarvam-triage-v1",
  "base_model": "sarvamai/sarvam-2b-v0.5"
}
```

### Step 7.4: Run Full Docker Compose Locally

```bash
# From project root
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

Monitor:
```bash
docker-compose logs -f
```

Test backend:
```bash
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever", "language": "en"}'
```

---

## PHASE 3: Registry Push

### Step 7.5: Push to Docker Hub

1. **Create Docker Hub account** (if not exists)
   - Go to https://hub.docker.com/signup

2. **Login:**
   ```bash
   docker login
   # Enter credentials
   ```

3. **Tag image:**
   ```bash
   docker tag triage-inference:latest <username>/triage-inference:latest
   ```

4. **Push:**
   ```bash
   docker push <username>/triage-inference:latest
   ```

5. **Verify:**
   - Go to https://hub.docker.com/r/<username>/triage-inference
   - Confirm image is listed with latest tag

---

## PHASE 4: RunPod Deployment

### Step 7.6: Create RunPod Pod

1. Go to https://www.runpod.io/console/pods

2. Click **"Create Pod"** → **"GPU Pods"**

3. **Search for PyTorch template** (or use custom CUDA image)

4. **Pod Configuration:**
   - **GPU:** RTX A4000 (recommended) or RTX 3080 (budget)
   - **Volume:** 50GB Container Disk
   - **Image:** `<your-username>/triage-inference:latest`

5. **Environment Variables:**
   ```
   SKIP_MODEL_LOAD=false
   LORA_PATH=/models/sarvam_triage_lora
   ```

6. **Ports:**
   - Expose: 8001
   - Public: Yes

7. **Click Deploy** and wait 2-5 minutes for startup

### Step 7.7: Verify RunPod Pod

Copy the pod URL from RunPod dashboard (looks like: `https://xxxxx.runpod.io`)

```bash
curl https://<pod-url>/health
```

Expected:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

## PHASE 5: Backend Integration

### Step 7.8: Update Backend Configuration

Edit `.env`:
```env
MODEL_ENDPOINT=https://<runpod-pod-url>
```

### Step 7.9: Test Backend → Inference Connection

```bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

In another terminal:
```bash
python ../tests/sprint7_integration_tests.py http://localhost:8000 https://<runpod-pod-url>
```

Expected output:
```
✓ Inference Service Health Check
✓ Backend Health Check
✓ Inference Generate Endpoint
✓ Triage Endpoint
✓ Error Handling
==============================================================
Passed: 5/5
==============================================================
```

---

## PHASE 6: Performance Validation

### Step 7.10: Measure Latency

```bash
# Test inference latency
time curl https://<pod-url>/generate \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Patient has chest pain", "request_id": "test-1"}'
```

**Target:** <5 seconds

### Step 7.11: Test Error Scenarios

```bash
# Empty message
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "", "language": "en"}'

# Invalid language
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message": "fever", "language": "xyz"}'

# Network timeout (kill inference service)
# Should fail gracefully with retry logic
```

---

## PHASE 7: Documentation & Handoff

### Step 7.12: Create Runbook

Document in `docs/RUNBOOK.md`:
- How to start/stop RunPod pod
- Common error messages and fixes
- How to update model or LoRA adapters
- How to scale (add more pods)

### Step 7.13: Finalize Deployment

- [ ] All tests passing
- [ ] Latency < 5 seconds (P95)
- [ ] Error handling working
- [ ] `.env` configured correctly
- [ ] Logs being collected
- [ ] Health checks responding

---

## Troubleshooting Guide

### Docker Build Fails

**Symptom:** `docker build` fails with dependency errors

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build -f inference/Dockerfile -t triage-inference:latest --no-cache .
```

### RunPod Pod Stuck in "Starting"

**Symptom:** Pod status shows "Starting" after 10 minutes

**Solution:**
1. Check logs: Click pod → "View Logs"
2. Look for error messages (e.g., model download failing)
3. Delete pod and create new one with explicit timeout (--start-period=180s)

### Model Loading Timeout

**Symptom:** `/health` endpoint times out or never returns `loaded: true`

**Solution:**
1. Ensure LoRA path is correct: `/models/sarvam_triage_lora`
2. Verify volume is mounted in RunPod
3. Check pod logs for CUDA errors or OOM

### Backend Cannot Reach Inference Service

**Symptom:** `CONNECTION_REFUSED` or `TIMEOUT`

**Solution:**
1. Verify URL in `.env` is correct
2. Check port 8001 is exposed in RunPod
3. Test from local machine: `curl https://<pod-url>/health`
4. Ensure firewall allows HTTPS (port 443)

---

## Sprint 7 Success Criteria

✅ Complete when:

1. Docker image builds locally
2. Image pushed to registry (Docker Hub)
3. RunPod pod created and running
4. `/health` endpoint returns `loaded: true`
5. Backend connects to RunPod inference service
6. `/api/v1/triage` returns valid responses <5 seconds
7. All integration tests pass
8. Error scenarios handled gracefully
9. Documentation complete

---

## Time Estimates

| Phase | Task | Time |
|-------|------|------|
| 1 | Docker build | 15-20 min |
| 2 | Local testing | 10 min |
| 3 | Registry push | 5-10 min |
| 4 | RunPod setup | 10-15 min |
| 5 | Integration | 10 min |
| 6 | Performance validation | 15 min |
| **Total** | **All phases** | **~75-90 min** |

---

## Next: Sprint 8 Preview

Once Sprint 7 is complete:

- [ ] Connect Streamlit frontend to backend
- [ ] Add conversation persistence (MySQL)
- [ ] Implement multilingual support validation
- [ ] Performance optimization (caching, streaming)
- [ ] Final demo preparation

**Ready to proceed? Confirm each step as you go. I'll be here to debug any issues!**

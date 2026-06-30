# Sprint 7 Quick Reference Card

## One-Command Checklist

```bash
# 1. Verify Docker is running
docker version

# 2. Build inference image
cd "C:\Users\Parth\OneDrive\Desktop\project ieee\triage-bot"
docker build -f inference/Dockerfile -t triage-inference:latest .

# 3. Login to Docker Hub
docker login

# 4. Tag and push
docker tag triage-inference:latest YOUR_USERNAME/triage-inference:latest
docker push YOUR_USERNAME/triage-inference:latest

# 5. Test locally
docker run -p 8001:8001 -e SKIP_MODEL_LOAD=true triage-inference:latest

# 6. In another terminal, test endpoint
curl http://localhost:8001/health

# 7. Test full stack with Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# 8. Run integration tests
python tests/sprint7_integration_tests.py
```

---

## Key Files Created

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Complete deployment walkthrough |
| `SPRINT_7_CHECKLIST.md` | Phase-by-phase checklist |
| `docs/RUNPOD_DEPLOYMENT.md` | RunPod-specific instructions |
| `tests/sprint7_integration_tests.py` | End-to-end validation tests |
| `docker-compose.override.yml` | Local testing with MySQL |
| `inference/Dockerfile` | Optimized container image |

---

## Critical Paths

### Path 1: Local → Docker Hub → RunPod
```
Build Image
    ↓
Test Locally
    ↓
Push to Docker Hub
    ↓
Create RunPod Pod
    ↓
Update Backend .env
    ↓
Test End-to-End
```

### Path 2: Debug Failures
```
docker logs <container>
    ↓
Check .env values
    ↓
Verify firewall/ports
    ↓
Test endpoints with curl
    ↓
Check system resources
```

---

## Environment Setup

### `.env` for Local Development
```env
APP_NAME=MedRoute AI
APP_VERSION=1.0.0
MODEL_PROVIDER=runpod
MODEL_ENDPOINT=http://inference:8001
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=triage123
MYSQL_DATABASE=triage_db
```

### `.env` for RunPod Production
```env
APP_NAME=MedRoute AI
APP_VERSION=1.0.0
MODEL_PROVIDER=runpod
MODEL_ENDPOINT=https://<runpod-pod-url>
MYSQL_HOST=<your-mysql-server>
MYSQL_USER=<prod-user>
MYSQL_PASSWORD=<prod-password>
MYSQL_DATABASE=triage_db
```

---

## Success Metrics

| Metric | Target | Command |
|--------|--------|---------|
| Build Time | <20 min | `docker build ...` |
| Image Size | <3GB | `docker images` |
| Health Check | <1 sec | `curl /health` |
| Triage Latency | <5 sec | `curl -X POST /api/v1/triage ...` |
| Error Rate | <1% | Monitor logs |

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `docker: command not found` | Start Docker Desktop |
| `CUDA out of memory` | Reduce batch size or use smaller GPU |
| `Connection refused` | Verify firewall, check port 8001 |
| `Model not loading` | Check LORA_PATH, verify volume mount |
| `Timeout during build` | Increase Docker memory in settings |
| `Image push fails` | Run `docker login` first |

---

## Next Commands to Run

```bash
# 1. Check if build is still running
docker buildx du

# 2. Once build completes, verify image
docker images | grep triage-inference

# 3. Test the image
docker run -it -p 8001:8001 \
  -e SKIP_MODEL_LOAD=true \
  triage-inference:latest

# 4. In another terminal
curl http://localhost:8001/health

# 5. Push to registry
docker push <your-username>/triage-inference:latest
```

---

## Estimated Timeline

- **T+0:** Docker build starts (~15-20 minutes)
- **T+20:** Build completes
- **T+22:** Image pushed to Docker Hub
- **T+25:** RunPod pod created
- **T+30:** Pod fully initialized
- **T+35:** Backend connected
- **T+40:** End-to-end tests pass

**Total: ~40 minutes to production inference**

---

## Getting Help

If something doesn't work:

1. **Check logs:**
   ```bash
   docker logs <container-id>
   # or in RunPod dashboard: View Logs
   ```

2. **Test in isolation:**
   ```bash
   # Test just the inference service
   curl https://<url>/health
   
   # Test just the backend
   curl http://localhost:8000/health
   ```

3. **Verify configuration:**
   ```bash
   # Check environment variables in RunPod
   # Go to RunPod dashboard → Pod details → Environment
   ```

---

## You're 90% There!

Your architecture is solid. This sprint is purely operational:
1. Build a container
2. Push to registry
3. Deploy to RunPod
4. Verify connection

No code changes needed. Just execution.

**Let's go! 🚀**

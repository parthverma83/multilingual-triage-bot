# This file shows the ideal setup for RunPod deployment
# (You won't run docker-compose on RunPod - use their web UI instead)

version: '3.8'

services:
  # On RunPod, you'll deploy this as a single container
  inference:
    image: your-registry/triage-inference:latest
    environment:
      SKIP_MODEL_LOAD: "false"  # Load model on startup
      LORA_PATH: "/models/sarvam_triage_lora"
      MODEL_NAME: "sarvam-triage-v1"
      BASE_MODEL: "sarvamai/sarvam-2b-v0.5"
      ADAPTER_VERSION: "sarvam_triage_lora"
    
    # RunPod setup:
    # 1. Go to runpod.io/console/pods
    # 2. Click "Create Pod"
    # 3. Select GPU template
    # 4. Use this image
    # 5. Mount volume for models at /models
    # 6. Expose port 8001
    # 7. Add environment variables above
    
    ports:
      - "8001:8001"
    
    volumes:
      # Your LoRA adapters should be mounted here
      - ./models/sarvam_triage_lora:/models/sarvam_triage_lora:ro
    
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s  # Longer startup time for model loading
    
    # GPU resources (if running in Kubernetes on RunPod)
    # resources:
    #   reservations:
    #     devices:
    #       - driver: nvidia
    #         count: 1
    #         capabilities: [gpu]

  # Backend runs locally or on separate cloud infrastructure
  backend:
    image: your-registry/triage-backend:latest
    environment:
      MODEL_PROVIDER: "runpod"
      MODEL_ENDPOINT: "https://<runpod-pod-url>"  # From RunPod dashboard
      MODEL_API_KEY: "${MODEL_API_KEY}"
    ports:
      - "8000:8000"

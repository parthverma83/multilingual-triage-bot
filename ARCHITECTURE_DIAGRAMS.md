# System Architecture Diagrams

## Sprint 7: Production Deployment Architecture

### Local Development Stack
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Desktop                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │   Streamlit      │  │  FastAPI Backend │                │
│  │   (Localhost)    │  │  :8000           │                │
│  │   Port 8501      │  └────────┬─────────┘                │
│  └────────┬─────────┘           │                          │
│           │                     │                          │
│           └────────────────────→│ HTTP                     │
│                                 │                          │
│                    ┌────────────▼─────────┐                │
│                    │ Inference Service    │                │
│                    │ :8001                │                │
│                    │ (SKIP_MODEL_LOAD=true)                │
│                    └──────────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │   MySQL          │  │   Redis          │                │
│  │   :3306          │  │   :6379          │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### RunPod Production Stack
```
┌──────────────────────────────────────────────────────────────┐
│                         Internet                             │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│              ┌──────────────────────────────────┐             │
│              │    RunPod GPU Pod                │             │
│              │    https://xxxxx.runpod.io       │             │
│              ├──────────────────────────────────┤             │
│              │                                  │             │
│              │  ┌──────────────────────────┐   │             │
│              │  │ Inference Service:8001   │   │             │
│              │  │ ├─ Sarvam-2B Model      │   │             │
│              │  │ ├─ LoRA Adapters         │   │             │
│              │  │ ├─ CUDA Runtime          │   │             │
│              │  │ └─ Health Checks         │   │             │
│              │  └──────────────────────────┘   │             │
│              │                                  │             │
│              │  ┌──────────────────────────┐   │             │
│              │  │ NVIDIA A4000 GPU         │   │             │
│              │  │ (24GB VRAM)              │   │             │
│              │  └──────────────────────────┘   │             │
│              │                                  │             │
│              └──────────────────────────────────┘             │
│                          ▲                                    │
│                          │ HTTPS                             │
│                          │ Request/Response                  │
│                          │                                    │
│              ┌───────────┴──────────────┐                    │
│              │                          │                    │
│    ┌─────────▼──────────┐    ┌──────────▼─────────┐          │
│    │  Backend Server    │    │  MySQL Server      │          │
│    │  Port 8000         │    │  (RDS)             │          │
│    │  • TriageEngine    │    │ • conversations    │          │
│    │  • Orchestrator    │    │ • messages         │          │
│    │  • Validators      │    │ • outcomes         │          │
│    └────────┬───────────┘    └────────────────────┘          │
│             │                                                 │
│    ┌────────▼──────────┐                                      │
│    │  Streamlit UI     │                                      │
│    │  (Public)         │                                      │
│    │ • Chat Interface  │                                      │
│    │ • Department View │                                      │
│    │ • Confidence Meter│                                      │
│    └───────────────────┘                                      │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Request Flow: End-to-End
```
User Input (Streamlit)
        │
        ▼
POST /api/v1/triage
├─ message: string
├─ language: "en" | "hi" | "mr"
└─ request_id: UUID
        │
        ▼
FastAPI Backend
        │
    ├─ Language Detector
    │   └─ Identify language
    │
    ├─ Symptom Extractor
    │   └─ Parse symptoms
    │
    ├─ Emergency Detector
    │   └─ Check urgency
    │
    ├─ Prompt Builder
    │   └─ Create inference prompt
    │
    └─ HTTP Client (with retry)
        │
        ▼
RunPod Inference Service
        │
    ├─ Load Model (first call)
    ├─ Load LoRA Adapters
    ├─ Run Inference
    └─ Stream Response
        │
        ▼
Response Validator
        │
    ├─ Parse JSON
    ├─ Validate schema
    └─ Fill defaults
        │
        ▼
Return to Frontend
{
  "status": "success",
  "department": "cardiology",
  "confidence": 0.92,
  "reasoning": "..."
}
        │
        ▼
Display in Streamlit UI
├─ Department card
├─ Confidence meter
├─ Emergency alert (if needed)
└─ Reasoning explanation
```

### Deployment Sequence
```
Step 1: Docker Build
┌─────────────────────────┐
│ docker build -f         │
│ inference/Dockerfile    │
│ -t triage-inference     │
└────────────┬────────────┘
             │
             ▼
       Image Created
        (~2.5 GB)
        
Step 2: Push to Registry
┌─────────────────────────┐
│ docker tag              │
│ docker push             │
│ → Docker Hub            │
└────────────┬────────────┘
             │
             ▼
    Image in Registry
  (accessible publicly)
        
Step 3: Create RunPod Pod
┌─────────────────────────┐
│ 1. Select GPU           │
│ 2. Specify Image        │
│ 3. Set Environment      │
│ 4. Configure Volumes    │
│ 5. Expose Port 8001     │
└────────────┬────────────┘
             │
             ▼
      Pod Initializing
        (2-5 min)
        
Step 4: Verify Pod
┌─────────────────────────┐
│ GET /health             │
│ Check loaded: true      │
└────────────┬────────────┘
             │
             ▼
   Pod Ready for Requests

Step 5: Backend Connection
┌─────────────────────────┐
│ Update .env:            │
│ MODEL_ENDPOINT=<url>    │
│ Restart Backend         │
└────────────┬────────────┘
             │
             ▼
   Connected & Testing
```

### Error Handling Flow
```
Request from Backend
        │
        ▼
    HTTP Timeout?
    /    \
   Yes   No
   │     │
   │     ▼
   │   HTTP Error?
   │   /    \
   │  Yes   No
   │  │     │
   │  │     ▼
   │  │   Response Valid?
   │  │   /    \
   │  │  Yes   No
   │  │  │     │
   ▼  ▼  ▼     ▼
Retry → Fallback → Return Error
Logic    Triage   (with request_id
         Engine   for tracking)
```

### Latency Budget
```
Request Received
    │
    ├─ Parse Request           5 ms
    │
    ├─ Language Detection     10 ms
    │
    ├─ Symptom Extraction     20 ms
    │
    ├─ Emergency Detection    10 ms
    │
    ├─ Prompt Building        15 ms
    │
    ├─ Network (RTT)          50 ms
    │
    ├─ GPU Inference       2,000 ms  ← Largest component
    │
    ├─ Response Parsing      100 ms
    │
    ├─ Validation           50 ms
    │
    └─ Return Response       10 ms
       
       Total: ~2,270 ms (~2.3 seconds)
       Target SLA: <5,000 ms ✅
```

### Monitoring Architecture
```
┌──────────────────────────────────────────┐
│      Observability Stack                 │
├──────────────────────────────────────────┤
│                                          │
│ ┌─ Backend Logs ─────────────────────┐  │
│ │ • Request ID                       │  │
│ │ • Latency per stage                │  │
│ │ • Error messages                   │  │
│ │ → Structured JSON format           │  │
│ └────────────────────────────────────┘  │
│                                          │
│ ┌─ Inference Logs ───────────────────┐  │
│ │ • Model load time                  │  │
│ │ • Inference latency                │  │
│ │ • GPU memory usage                 │  │
│ │ • Token generation rate            │  │
│ └────────────────────────────────────┘  │
│                                          │
│ ┌─ Health Checks ────────────────────┐  │
│ │ • Backend: /health                 │  │
│ │ • Inference: /health               │  │
│ │ • Database: connectivity test      │  │
│ └────────────────────────────────────┘  │
│                                          │
│ ┌─ Metrics ──────────────────────────┐  │
│ │ • P50/P95/P99 latency              │  │
│ │ • Error rate                       │  │
│ │ • Requests/sec                     │  │
│ │ • GPU memory utilization           │  │
│ └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

---

## Component Responsibilities

### Streamlit Frontend
- **Role:** User interface
- **Runs:** Local or cloud
- **Communicates:** Backend HTTP API
- **Handles:** Display, user input, conversation history

### FastAPI Backend
- **Role:** Orchestrator
- **Runs:** Local, cloud, or on RunPod
- **Communicates:** Inference service via HTTP
- **Handles:** Routing, validation, error handling

### RunPod Inference Service
- **Role:** Model inference
- **Runs:** GPU pod only
- **Communicates:** Backend HTTP API
- **Handles:** Model loading, CUDA operations, response generation

### MySQL Database
- **Role:** Persistent storage
- **Runs:** Cloud (RDS) or local
- **Communicates:** Backend (SQLAlchemy)
- **Handles:** Conversations, outcomes, user data

---

## Summary: You Have

✅ Solid architecture (tested design)  
✅ Production code (no hacks)  
✅ Comprehensive documentation (6+ guides)  
✅ Integration tests (automated validation)  
✅ Docker configuration (ready to build)  
✅ RunPod instructions (step-by-step)  

**All pieces are in place. Time to deploy.**

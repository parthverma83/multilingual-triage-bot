import os
from pathlib import Path

BASE_MODEL = "sarvamai/sarvam-2b-v0.5"
MODEL_NAME = "sarvam-triage-v1"
ADAPTER_VERSION = "sarvam_triage_lora"

LORA_PATH = Path(os.getenv("LORA_PATH", "/models/sarvam_triage_lora"))


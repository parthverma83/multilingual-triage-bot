from __future__ import annotations

import logging
import os
import time
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from config import BASE_MODEL, LORA_PATH

logger = logging.getLogger(__name__)


class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.loaded = False

    def load(self):
        if self.loaded:
            logger.info("Model already loaded; reusing existing model instance.")
            return self

        start_time = time.perf_counter()
        adapter_path = self._resolve_adapter_path()

        logger.info("Starting model load: base=%s adapter=%s", BASE_MODEL, adapter_path)

        quantization_config = None
        if torch.cuda.is_available():
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
        else:
            logger.warning("CUDA is not available; loading without 4-bit quantization.")

        self.tokenizer = AutoTokenizer.from_pretrained(
            BASE_MODEL,
            trust_remote_code=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            device_map="auto",
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True,
        )

        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model.eval()
        self.loaded = True

        elapsed = time.perf_counter() - start_time
        logger.info("Model loading finished in %.2f seconds.", elapsed)
        return self

    def generate(self, prompt: str):
        if not self.loaded:
            if os.getenv("SKIP_MODEL_LOAD", "").lower() in {"1", "true", "yes"}:
                return f"[stub] SKIP_MODEL_LOAD is set — no real inference. prompt_preview={prompt[:80]!r}"
            self.load()

        start_time = time.perf_counter()
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_device = next(self.model.parameters()).device
        inputs = {key: value.to(input_device) for key, value in inputs.items()}

        with torch.inference_mode():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        generated_ids = output_ids[0][inputs["input_ids"].shape[-1] :]
        generated_text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

        elapsed = time.perf_counter() - start_time
        logger.info("Generation finished in %.2f seconds.", elapsed)

        return generated_text

    @staticmethod
    def _resolve_adapter_path() -> Path:
        adapter_path = Path(LORA_PATH)
        if adapter_path.is_absolute():
            return adapter_path

        inference_dir = Path(__file__).resolve().parent
        return (inference_dir / adapter_path).resolve()


model_manager = ModelManager()


def load_model():
    return model_manager.load()

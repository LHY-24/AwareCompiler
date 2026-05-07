"""OpenAI-compatible client utilities for external LLM baselines."""

import os
from typing import Any, Dict, List, Optional

import httpx
from openai import OpenAI


DEFAULT_MODEL = "gpt-5.5"
DEFAULT_BASE_URL = "https://api.openai.com/v1"


def get_llm_config() -> Dict[str, Any]:
    """Read OpenAI-compatible endpoint settings from the environment."""
    api_key = (
        os.environ.get("AWARECOMPILER_LLM_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )
    base_url = (
        os.environ.get("AWARECOMPILER_LLM_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or DEFAULT_BASE_URL
    )
    model = os.environ.get("AWARECOMPILER_LLM_MODEL") or os.environ.get("LLM_MODEL") or DEFAULT_MODEL
    verify_ssl = os.environ.get("AWARECOMPILER_LLM_VERIFY_SSL", "true").lower() not in {"0", "false", "no"}
    timeout = float(os.environ.get("AWARECOMPILER_LLM_TIMEOUT", "90"))
    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "verify_ssl": verify_ssl,
        "timeout": timeout,
    }


def make_client() -> OpenAI:
    cfg = get_llm_config()
    if not cfg["api_key"]:
        raise RuntimeError(
            "Missing API key. Set AWARECOMPILER_LLM_API_KEY or OPENAI_API_KEY before running external LLM baselines."
        )
    http_client = httpx.Client(verify=cfg["verify_ssl"], timeout=cfg["timeout"])
    return OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"], http_client=http_client)


def chat_completion(
    messages: List[Dict[str, Any]],
    *,
    tools: Optional[List[Dict[str, Any]]] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
) -> Any:
    cfg = get_llm_config()
    client = make_client()
    kwargs: Dict[str, Any] = {
        "model": cfg["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if tools is not None:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs)

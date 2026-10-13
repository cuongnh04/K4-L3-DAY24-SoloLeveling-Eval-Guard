from __future__ import annotations

"""M5: optional LLM enrichment with deterministic fallbacks."""

import json
import os
import re
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, GENERATION_MODEL


@dataclass
class EnrichedChunk:
    original_text: str
    enriched_text: str
    summary: str
    hypothesis_questions: list[str]
    auto_metadata: dict
    method: str


def _completion(system: str, user: str, max_tokens: int) -> str | None:
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        response = OpenAI().chat.completions.create(
            model=GENERATION_MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print(f"  ⚠️  Enrichment API failed: {exc}")
        return None


def summarize_chunk(text: str) -> str:
    result = _completion("Tóm tắt đoạn văn trong 2-3 câu tiếng Việt.", text, 150)
    if result:
        return result
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip()]
    return " ".join(sentences[:2]) or text


def generate_hypothesis_questions(text: str, n_questions: int = 3) -> list[str]:
    result = _completion(f"Tạo {n_questions} câu hỏi tiếng Việt, mỗi câu trên một dòng.", text, 200)
    if result:
        return [q.strip().lstrip("0123456789.-) ") for q in result.splitlines() if q.strip()][:n_questions]
    sentences = [s.strip() for s in re.split(r"[.!?\n]", text) if len(s.strip()) > 10]
    return [f"{s.rstrip('.')}?" for s in sentences[:n_questions]]


def contextual_prepend(text: str, document_title: str = "") -> str:
    result = _completion("Mô tả ngắn vị trí và chủ đề của đoạn văn; chỉ trả về một câu.",
                         f"Tài liệu: {document_title}\n\nĐoạn văn:\n{text}", 80)
    prefix = result or (f"Trích từ {document_title}." if document_title else "Đoạn chính sách.")
    return f"{prefix}\n\n{text}"


def extract_metadata(text: str) -> dict:
    result = _completion(
        'Trả về JSON {"topic":"...","entities":[],"category":"policy|hr|it|finance","language":"vi|en"}.',
        text, 150)
    if result:
        try:
            return json.loads(result)
        except (json.JSONDecodeError, TypeError):
            pass
    lower = text.lower()
    category = "it" if any(word in lower for word in ("mật khẩu", "vpn", "máy tính")) else "policy"
    return {"topic": text.split(".")[0][:80], "entities": [], "category": category, "language": "vi"}


def _enrich_single_call(text: str, source: str) -> dict:
    result = _completion(
        'Phân tích và trả về JSON gồm summary, questions, context, metadata.',
        f"Tài liệu: {source}\n\nĐoạn văn:\n{text}", 400)
    if result:
        try:
            return json.loads(result)
        except (json.JSONDecodeError, TypeError):
            pass
    return {
        "summary": summarize_chunk(text),
        "questions": generate_hypothesis_questions(text),
        "context": f"Trích từ {source}." if source else "Nội dung chính sách.",
        "metadata": extract_metadata(text),
    }


def enrich_chunks(chunks: list[dict], methods: list[str] | None = None) -> list[EnrichedChunk]:
    if os.getenv("ENRICHMENT_ENABLED", "1") == "0":
        return []
    methods = methods or ["combined"]
    combined = "combined" in methods
    enriched = []
    for chunk in chunks:
        text = chunk["text"]
        source = chunk.get("metadata", {}).get("source", "")
        if combined:
            data = _enrich_single_call(text, source)
            summary = data.get("summary", "")
            questions = data.get("questions", [])
            context = data.get("context", "")
            enriched_text = f"{context}\n\n{text}" if context else text
            metadata = data.get("metadata", {})
        else:
            summary = summarize_chunk(text) if "summary" in methods else ""
            questions = generate_hypothesis_questions(text) if "hyqa" in methods else []
            enriched_text = contextual_prepend(text, source) if "contextual" in methods else text
            metadata = extract_metadata(text) if "metadata" in methods else {}
        enriched.append(EnrichedChunk(text, enriched_text, summary, questions,
                                      {**chunk.get("metadata", {}), **metadata},
                                      "+".join(methods)))
    return enriched

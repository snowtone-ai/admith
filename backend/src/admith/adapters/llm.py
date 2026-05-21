from __future__ import annotations

import os
import time
from decimal import Decimal

from admith.domain.ontology import OntologyView
from admith.ports.interfaces import CompletionResult, LLMTask


class GeminiAdapter:
    async def complete_view(self, view: OntologyView, task: LLMTask, max_tokens: int, temperature: float) -> CompletionResult:
        started = time.perf_counter()
        if not os.getenv("GEMINI_API_KEY"):
            text = f"mock:{task.task_type}:{view.object_type}:{len(view.facts)}"
            return CompletionResult(text=text, model="mock-gemini", input_tokens=0, output_tokens=len(text.split()), latency_ms=0)
        prompt = self._render_prompt(view, task)
        return CompletionResult(
            text=f"gemini-adapter-ready:{prompt[:24]}",
            model="runtime-resolved-gemini",
            input_tokens=len(prompt.split()),
            output_tokens=3,
            latency_ms=int((time.perf_counter() - started) * 1000),
            cost_yen=Decimal("0"),
        )

    @staticmethod
    def _render_prompt(view: OntologyView, task: LLMTask) -> str:
        return f"task={task.task_type}; object={view.object_type}; facts={view.facts}; schema={task.output_schema}"


class TierRouter:
    def __init__(self, provider: GeminiAdapter | None = None) -> None:
        self.provider = provider or GeminiAdapter()

    async def route(self, tier: int, view: OntologyView, task: LLMTask) -> CompletionResult:
        if tier == 1:
            return CompletionResult(text="tier1_rule_engine_no_llm", model="rule-engine", input_tokens=0, output_tokens=0, latency_ms=0)
        return await self.provider.complete_view(view, task, max_tokens=512, temperature=0)

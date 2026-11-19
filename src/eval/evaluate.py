"""Scores the extract-and-verify pipeline against the hand-labelled eval set.

    python -m eval.evaluate [--json out.json] [--min-accuracy 0.7]

Exits 1 if relevance accuracy falls below --min-accuracy, so CI can gate on it.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from agent.llm import get_generator
from agent.run_digest import extract_and_verify
from mcp_server.models import Paper

from .dataset import EVAL_CASES


def _dataset_match(expected: str, actual: str) -> bool:
    expected_n, actual_n = expected.strip().lower(), actual.strip().lower()
    if expected_n == "not stated":
        return actual_n == "not stated"
    return expected_n in actual_n or actual_n in expected_n


def run_eval() -> dict:
    generator = get_generator()
    results = []
    for case in EVAL_CASES:
        paper = Paper(
            arxiv_id=case["arxiv_id"],
            title=case["title"],
            abstract=case["abstract"],
            link=f"https://arxiv.org/abs/{case['arxiv_id']}",
            published=datetime.now(UTC),
        )
        state = extract_and_verify(generator, paper)
        relevance_correct = state["relevance"] == case["expected_relevance"]
        dataset_correct = _dataset_match(case["expected_datasets"], state["datasets"])
        results.append(
            {
                "arxiv_id": case["arxiv_id"],
                "expected_relevance": case["expected_relevance"],
                "actual_relevance": state["relevance"],
                "relevance_correct": relevance_correct,
                "expected_datasets": case["expected_datasets"],
                "actual_datasets": state["datasets"],
                "dataset_correct": dataset_correct,
                "verified": state["verified"],
            }
        )

    n = len(results)
    return {
        "relevance_accuracy": sum(r["relevance_correct"] for r in results) / n,
        "dataset_accuracy": sum(r["dataset_correct"] for r in results) / n,
        "n": n,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default=None, help="write full metrics to this path")
    parser.add_argument("--min-accuracy", type=float, default=0.7)
    args = parser.parse_args()

    metrics = run_eval()
    print(f"relevance accuracy: {metrics['relevance_accuracy']:.2f} ({metrics['n']} cases)")
    print(f"dataset accuracy:   {metrics['dataset_accuracy']:.2f}")
    for r in metrics["results"]:
        if not r["relevance_correct"] or not r["dataset_correct"]:
            print(f"  MISS {r['arxiv_id']}: relevance {r['actual_relevance']!r} (expected {r['expected_relevance']!r})")

    if args.json:
        Path(args.json).write_text(json.dumps(metrics, indent=2))

    if metrics["relevance_accuracy"] < args.min_accuracy:
        print(f"FAIL: relevance accuracy below threshold {args.min_accuracy}")
        sys.exit(1)


if __name__ == "__main__":
    main()

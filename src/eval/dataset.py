"""Hand-labelled eval cases. Fill this in with 15-20 real papers you've
read and judged yourself — the placeholder entries below are seeds, not a
finished set. Each case needs the real abstract text (copy it from arXiv),
your own relevance call, and the datasets actually named in the abstract.

Include at least one guard-rail case: a paper clearly irrelevant to your
research, which must NOT come back "High"."""

from __future__ import annotations

from typing import TypedDict


class EvalCase(TypedDict):
    arxiv_id: str
    title: str
    abstract: str
    expected_relevance: str  # High | Medium | Low
    expected_datasets: str  # substring expected to appear, or "not stated"


EVAL_CASES: list[EvalCase] = [
    {
        "arxiv_id": "2207.08815",
        "title": "Why do tree-based models still outperform deep learning on tabular data?",
        "abstract": (
            "We benchmark tree-based models and deep learning on a large collection of "
            "tabular datasets and find that tree-based models remain superior, especially "
            "on datasets with irregular decision boundaries, evaluated across 45 datasets."
        ),
        "expected_relevance": "High",
        "expected_datasets": "45 datasets",
    },
    {
        "arxiv_id": "2101.11605",
        "title": "Bottleneck Transformers for Visual Recognition",
        "abstract": (
            "We present BoTNet, a simple architecture that incorporates self-attention into "
            "ResNet for image classification, object detection and instance segmentation on "
            "ImageNet and COCO."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "ImageNet",
    },
    # guard-rail: clearly out of scope, must not be rated High.
    {
        "arxiv_id": "9999.00000",
        "title": "A Survey of Medieval Beekeeping Practices in Northern Europe",
        "abstract": (
            "This survey reviews historical records of beekeeping techniques in medieval "
            "Northern Europe, with no connection to machine learning or data analytics."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
]

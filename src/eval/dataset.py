"""Hand-labelled eval cases. Relevance labels are the user's own judgment
against their stated research interests (deskflow.config.yaml) — not copied
from the pipeline's own output, since that would make the eval circular.
`expected_datasets` is an independent reading of each abstract's actual text.

Note on class balance: within the "retrieval-augmented generation" arXiv
topic, most real papers turn out tangential to this user's specific interest
(retrieval/eval methodology + tabular DL), so this set skews heavily toward
"Low" (~13/18). A model that always predicts "Low" would already score high
on raw relevance accuracy — see evaluate.py's separate `high_recall` metric,
which checks whether genuinely relevant ("High") papers are actually caught,
since missing one of those is the failure mode that actually matters."""

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
    {
        "arxiv_id": "2611.16148",
        "title": "Calibrated Early Termination with Bounded Optimality Gaps for Constrained Vector Search",
        "abstract": (
            "Vector search over learned embeddings is the retrieval layer of recommendation "
            "and retrieval-augmented generation, and many applications cap how many answer "
            "items one category may contribute. Graph indexes answer a query by best-first "
            "traversal, and where it stops determines its cost and whether its answer is "
            "exact. We study early termination for such constrained k-nearest-neighbor (k-NN) "
            "queries, with plain k-NN as a special case, and seek the cheapest stopping rule "
            "whose answer is exact with probability at least 1-epsilon. On two datasets of one "
            "million items each, CaST replayed on logged searches costs at most 1.132 times "
            "the class optimum for risk levels from 0.03 to 0.10, at 95% joint confidence per "
            "setting. At a common risk target on held-out queries, CaST is faster than every "
            "other calibrated rule we time, which take 4.8% to 45.5% more mean time."
        ),
        "expected_relevance": "Medium",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.23147",
        "title": "AI Companions for Young Adult Caregivers: Practical Advice, Emotional Depth, and the Limits of Metric Evaluation",
        "abstract": (
            "Young adult caregivers (YACs) are individuals aged 18 to 25 currently taking "
            "care of a family member, partner, or friend facing chronic illness. We present "
            "Carebot, it uses an open-weight LLM (Gemma 3-27B) as its base model, on which we "
            "compared fine-tuning, retrieval-augmented generation (RAG), and a combination of "
            "both. An LLM judge preferred Carebot's responses over the base model's in 85% of "
            "evaluated pairs. We then conducted a user study with 90 YACs. We argue that "
            "support tools for YACs require situation-sensitive emotional depth and aligned "
            "evaluation frameworks to study their effectiveness."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.18771",
        "title": "Agri-MRAG: Parameter-Enhanced Multimodal Retrieval-Augmented Generation for Agricultural Visual Question Answering",
        "abstract": (
            "Multimodal Retrieval-Augmented Generation (MRAG) has shown promise for "
            "Agricultural Visual Question Answering (Agri-VQA). We propose Agri-MRAG, a "
            "multimodal retrieval-augmented framework for agricultural VQA. For evaluation, "
            "we use PlantVillageVQA as a broad agricultural benchmark and construct PlantVQA, "
            "a region-specific forestry and fruit crop VQA dataset containing 7,514 images and "
            "15,028 expert-verified question-answer pairs. Experiments show that Agri-MRAG "
            "achieves ROUGE-L scores of 41.21 and 46.58 on the two datasets, outperforming "
            "mRAG by 11.70 and 4.51 points, and VisRAG by 8.80 and 3.39 points, respectively."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "PlantVillageVQA, PlantVQA",
    },
    {
        "arxiv_id": "2611.23931",
        "title": "Quantifying the Intrusiveness of Retrofitting Retrieval-Augmented Generation onto Legacy Software Systems",
        "abstract": (
            "Enterprises increasingly add retrieval-augmented generation (RAG) to existing "
            "REST and monolithic systems. We present a taxonomy of three retrofit patterns, "
            "the Legacy Intrusion Score (LIS), a static evaluation on five legacy systems, and "
            "a live case study that deploys all three patterns as separate OS processes. The "
            "sidecar adds no detectable latency to the legacy endpoint, whereas SDK-embed and "
            "naive-invasive add 569 and 475 ms. Retrieval hit@1 is 0.95; three hosted LLMs "
            "answer all 12 test questions correctly and a local model 9/12."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.19253",
        "title": "KaleidoKV: Rearranging Evidence for Efficient KV Cache Reuse in Offline RAG Inference",
        "abstract": (
            "Retrieval-augmented generation (RAG) augments large language models (LLMs) on "
            "question-answering (QA) tasks with retrieved evidence at inference time. We "
            "propose KaleidoKV, a framework that plans evidence orders across the batch and "
            "controls when requests enter the engine while preserving each request's evidence "
            "set and content. Experiments on four QA workloads and four LLMs show that "
            "KaleidoKV achieves the highest throughput and lowest mean time to first token in "
            "all 16 settings, with approximately 1.24-1.75x the throughput of the strongest "
            "baseline, including planning time."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.16425",
        "title": "RMIT-ADM+S at TREC RAG 2026: Research Agents, Retriever Ablations, and Open-Weight Replication",
        "abstract": (
            "We describe the RMIT-ADM+S team's participation in the TREC 2026 "
            "Retrieval-Augmented Generation (RAG) track using the ClimbMix corpus. We "
            "submitted seven research-agent runs using proprietary OpenAI and open-weight "
            "models, exploring different retrieval strategies, writer models, and agent "
            "workflows. Pre-submission ablations identified writer selection and "
            "adjacent-chunk expansion as the main factors affecting answer quality. In the "
            "official NIST evaluation, six of seven runs exceeded the track median across all "
            "three rubric/nugget collections."
        ),
        "expected_relevance": "High",
        "expected_datasets": "ClimbMix",
    },
    {
        "arxiv_id": "2611.16590",
        "title": "AstroMemBench: A Benchmark for Memory Systems in Embodied Spacecraft Agents",
        "abstract": (
            "Long-term spacecraft autonomy requires embodied agents to use operational "
            "history under communication delays and time-critical operations. We introduce "
            "AstroMemBench, covering 16 memory subchallenges through 140 templates and 2240 "
            "instances across nine tasks in planetary surface operations, on-orbit servicing, "
            "and deep-space exploration. Main experiments compare six configurations. Mem0, "
            "Chain-of-Memory, LightMem, and retrieval-augmented generation (RAG) improve "
            "same-session mean scores over native Pi Agent, with no clear advantage of the "
            "three memory systems over RAG."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "AstroMemBench",
    },
    {
        "arxiv_id": "2611.17161",
        "title": "Cited but Unused: Parametric Provenance in Retrieval-Augmented Generation",
        "abstract": (
            "Retrieval-augmented generation systems attach citations to attribute claims to "
            "their sources. These citations frequently misstate provenance, and standard "
            "verification cannot detect this. We measure provenance by counterfactual value "
            "substitution: a fact in the retrieved passages is replaced with a false variant "
            "and the model re-queried. We find that across five sizes of one model family and "
            "a second comparator family, 1.2% to 15.7% of citable claims derive from "
            "parametric memory rather than the retrieved context. We further find that "
            "natural language inference verification, the standard approach, gives results "
            "indistinguishable from chance across models, even when restricted to the cited "
            "passage."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.16366",
        "title": "CURATOR: Scalable Fine-grained Evidence Selection for Retrieval-Augmented Generation using Decision Models",
        "abstract": (
            "Retrieval-augmented generation (RAG) provides entire retrieved passages to the "
            "LLM, even though only a handful of spans within them contain the evidence "
            "pertaining to the question. We introduce CURATOR, a fine-tuned decision model "
            "trained to make reliable evidence-selection decisions over large candidate sets. "
            "By training a decision model to select varying numbers of supporting spans from "
            "large candidate pools, CURATOR develops the capability to select evidence for RAG "
            "while retaining the computational efficiency of joint decision-making. CURATOR "
            "maintains a strong evidence discrimination capability as the number of candidates "
            "increases, generalizes across different tasks and document domains, and improves "
            "downstream RAG performance."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.19862",
        "title": "Bioformer-RetroMAE: retrieval-oriented pretraining of a compact biomedical language model for literature search",
        "abstract": (
            "Dense retrieval is increasingly used for biomedical literature search and "
            "retrieval-augmented generation (RAG). We present Bioformer-RetroMAE, a compact "
            "(43M-parameter) retrieval-oriented biomedical encoder obtained by continually "
            "pretraining Bioformer8L with RetroMAE on approximately 32 million PubMed titles "
            "and abstracts. After bi-encoder fine-tuning with BM25 hard negatives, we "
            "evaluated it on BioASQ Task 12B test questions by retrieving from all PubMed "
            "abstracts. Bioformer-RetroMAE outperformed BioBERT and PubMedBERT bi-encoders "
            "fine-tuned under identical settings on all metrics."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "PubMed, BioASQ Task 12B",
    },
    {
        "arxiv_id": "2611.20261",
        "title": "Estimating Outpatient Visit Prices from Hospital Price Transparency Data using Large Language Models",
        "abstract": (
            "Hospital care prices in the United States have increased substantially, yet "
            "patients lack effective tools to access and compare costs. To estimate visit "
            "prices, we used a retrieval-augmented generation (RAG) framework to analyze "
            "price transparency (PT) files from three major hospitals in Maryland and the "
            "surrounding region. The GPT-BM25 retriever achieved the best performance, with "
            "average price MAPE of 19.44% for individual procedures and 4.90% for groups, "
            "compared with 147.98% and 82.82%, respectively, for the no-RAG baseline."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.19333",
        "title": "Orbit AI: Evaluating Tool-Augmented Agents For Enterprise Question Answering",
        "abstract": (
            "Enterprise information is commonly stored across multiple platforms rather than "
            "in one centralized location. We evaluate Orbit AI, a tool-based "
            "retrieval-augmented generation (RAG) system that uses a ReAct agent implemented "
            "with LangGraph to retrieve and combine information from three different "
            "workspace sources. The held-out evaluation set contains 80 questions designed "
            "for Phase 3 workspace; Gemini 3.5 Flash Lite achieves an accuracy of 86.25% with "
            "the complete agent. Document-only RAG achieves 60.00%, and the plain LLM achieves "
            "23.13%."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.24039",
        "title": "A Capability Framework for Evaluating Agentic AI Platforms in Regulated Enterprises",
        "abstract": (
            "Agentic AI platforms are being procured faster than they can be measured. We "
            "report an industrial evaluation programme (\"bakeoff\") run by the innovation "
            "laboratory of a global bank in which ten platforms were assessed by a "
            "cross-functional panel on nine capability dimensions across three "
            "financial-services workloads: counterparty credit risk, retrieval-augmented "
            "generation and process automation. A secondary analysis finds Cronbach's alpha = "
            "0.98 across nominally distinct dimensions, a halo effect indicating that "
            "demonstration-based scoring measures presentation as much as capability."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.19077",
        "title": "HorizANN: Elastically Scaling Vector Search with Ghost Edges",
        "abstract": (
            "Approximate nearest neighbor search (ANNS) is fundamental to modern "
            "data-intensive AI applications such as retrieval-augmented generation, "
            "recommendation systems, and semantic search. We present HorizANN, a distributed "
            "graph-based ANNS system that scales horizontally without requiring full index "
            "reconstruction, using ghost edges to preserve cross-partition connectivity as "
            "partition boundaries change during repartitioning. As the index grows from 100M "
            "vectors on one worker to 1B vectors on ten workers, HorizANN inserts each 100M "
            "vectors within 2.5 hours and sustains 3.4-3.5K queries per second at 0.998 "
            "Recall@10."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2611.21823",
        "title": "TUSI: A Citation-Grounded Graph-Based Benchmark",
        "abstract": (
            "Evaluating retrieval-augmented generation (RAG) systems in Persian law remains "
            "challenging because benchmarks lack realism, grounding, and coverage of legal "
            "reasoning. We introduce TUSI-Bench, a structured Persian legal benchmark built "
            "upon a multi-layered legal knowledge framework containing 7,261 legal articles. "
            "TUSI-Bench provides two complementary evaluation tasks: TUSI-QA, an open-ended "
            "question answering benchmark containing 1,999 questions, and TUSI-Bar, a "
            "multiple-choice benchmark containing approximately 500 four-option questions. "
            "Incorporating graph-based relations improves retrieval recall by up to 8 "
            "percentage points compared to standard baselines."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "TUSI-Bench, TUSI-QA, TUSI-Bar",
    },
]

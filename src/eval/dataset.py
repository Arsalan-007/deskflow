"""Hand-labelled eval cases. Relevance labels are the user's own judgment
against their stated research interests (deskflow.config.yaml) — not copied
from the pipeline's own output, since that would make the eval circular.
`expected_datasets` is an independent reading of each abstract's actual text.

This set was rebuilt after `topics` pivoted from RAG to pure tabular deep
learning. Two sources: (1) papers from the user's own pre-existing tabular-DL
research corpus (rag-tabular-assistant/data/pdfs/) — genuinely relevant by
construction, giving solid High cases; (2) fresh real arXiv results from the
new topics, which surfaced the Low/Medium cases needed for balance: several
domain-application papers that *use* an existing tabular foundation model
without contributing new tabular methodology (energetic materials, telecom
churn, photometric redshift), plus one genuine search false-positive
(2610.19601 matched "differentiable trees" via an incidental phrase in an
unrelated LLM-pretraining paper) that makes a clean guard-rail case."""

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
        "arxiv_id": "1908.07442",
        "title": "TabNet: Attentive Interpretable Tabular Learning",
        "abstract": (
            "We propose a novel high-performance and interpretable canonical deep tabular "
            "data learning architecture, TabNet. TabNet uses sequential attention to choose "
            "which features to reason from at each decision step, enabling interpretability "
            "and more efficient learning as the learning capacity is used for the most "
            "salient features. We demonstrate that TabNet outperforms other variants on a "
            "wide range of non-performance-saturated tabular datasets and yields "
            "interpretable feature attributions plus insights into its global behavior. "
            "Finally, we demonstrate self-supervised learning for tabular data, "
            "significantly improving performance when unlabeled data is abundant."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "1909.06312",
        "title": "Neural Oblivious Decision Ensembles for Deep Learning on Tabular Data",
        "abstract": (
            "In an important case of heterogenous tabular data, the advantage of DNNs over "
            "shallow counterparts remains questionable; there is no sufficient evidence that "
            "deep learning machinery allows constructing methods that outperform gradient "
            "boosting decision trees (GBDT). We introduce Neural Oblivious Decision "
            "Ensembles (NODE), a new deep learning architecture designed to work with any "
            "tabular data. NODE generalizes ensembles of oblivious decision trees, but "
            "benefits from both end-to-end gradient-based optimization and the power of "
            "multi-layer hierarchical representation learning. With an extensive "
            "experimental comparison to the leading GBDT packages on a large number of "
            "tabular datasets, we demonstrate the advantage of the proposed NODE "
            "architecture, which outperforms the competitors on most of the tasks."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2012.06678",
        "title": "TabTransformer: Tabular Data Modeling Using Contextual Embeddings",
        "abstract": (
            "We propose TabTransformer, a novel deep tabular data modeling architecture for "
            "supervised and semi-supervised learning. The TabTransformer is built upon "
            "self-attention based Transformers. The Transformer layers transform the "
            "embeddings of categorical features into robust contextual embeddings to "
            "achieve higher prediction accuracy. Through extensive experiments on fifteen "
            "publicly available datasets, we show that the TabTransformer outperforms the "
            "state-of-the-art deep learning methods for tabular data by at least 1.0% on "
            "mean AUC, and matches the performance of tree-based ensemble models."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2106.01342",
        "title": "SAINT: Improved Neural Networks for Tabular Data via Row Attention and Contrastive Pre-Training",
        "abstract": (
            "Tabular data underpins numerous high-impact applications of machine learning "
            "from fraud detection to genomics and healthcare. We devise a hybrid deep "
            "learning approach to solving tabular data problems. Our method, SAINT, "
            "performs attention over both rows and columns, and it includes an enhanced "
            "embedding method. We also study a new contrastive self-supervised pre-training "
            "method for use when labels are scarce. SAINT consistently improves performance "
            "over previous deep learning methods, and it even outperforms gradient boosting "
            "methods, including XGBoost, CatBoost, and LightGBM, on average over a variety "
            "of benchmark tasks."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2203.05556",
        "title": "On Embeddings for Numerical Features in Tabular Deep Learning",
        "abstract": (
            "Recently, Transformer-like deep architectures have shown strong performance on "
            "tabular data problems. We argue that embeddings for numerical features are an "
            "underexplored degree of freedom in tabular DL. We describe two conceptually "
            "different approaches to building embedding modules: one based on a piecewise "
            "linear encoding of scalar values, and one that utilizes periodic activations. "
            "We empirically demonstrate that these two approaches can lead to significant "
            "performance boosts compared to embeddings based on conventional blocks such as "
            "linear layers and ReLU activations, and that after proper embeddings, simple "
            "MLP-like models can perform on par with attention-based architectures."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2207.01848",
        "title": "TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second",
        "abstract": (
            "We present TabPFN, a trained Transformer that can do supervised classification "
            "for small tabular datasets in less than a second, needs no hyperparameter "
            "tuning and is competitive with state-of-the-art classification methods. TabPFN "
            "performs in-context learning (ICL). On the 18 datasets in the OpenML-CC18 "
            "suite that contain up to 1,000 training data points, we show that our method "
            "clearly outperforms boosted trees and performs on par with complex "
            "state-of-the-art AutoML systems with up to 230x speedup. We also validate these "
            "results on an additional 67 small numerical datasets from OpenML."
        ),
        "expected_relevance": "High",
        "expected_datasets": "OpenML-CC18, OpenML",
    },
    {
        "arxiv_id": "2410.24210",
        "title": "TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling",
        "abstract": (
            "Deep learning architectures for supervised learning on tabular data range from "
            "simple multilayer perceptrons (MLP) to sophisticated Transformers and "
            "retrieval-augmented methods. Our new model TabM relies on efficient "
            "ensembling, where one TabM efficiently imitates an ensemble of MLPs and "
            "produces multiple predictions per object, sharing most of their parameters. "
            "Using TabM as a new baseline, we perform a large-scale evaluation of tabular "
            "DL architectures on public benchmarks in terms of both task performance and "
            "efficiency. We find that TabM demonstrates the best performance among tabular "
            "DL models."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2610.25558",
        "title": "FTFM: Factorized Tabular Foundation Models",
        "abstract": (
            "Tabular foundation models (TFMs) are becoming a powerful alternative to "
            "conventional tabular learning, adapting to new datasets in context without "
            "task-specific training. Current architectures face a trade-off: models that "
            "preserve cell-level representations are expensive, while faster models "
            "collapse each row into a fixed embedding and lose fine-grained state. We "
            "introduce Factorized Tabular Foundation Models (FTFM), which preserve cell "
            "representations while factorizing their computation through one contextual "
            "latent per row and one per column. FTFM achieves competitive predictive "
            "performance in tabular classification on major benchmarks such as TabArena and "
            "BeyondArena."
        ),
        "expected_relevance": "High",
        "expected_datasets": "TabArena, BeyondArena",
    },
    {
        "arxiv_id": "2611.24214",
        "title": "Towards Reliable Scaling Laws for Tabular Foundation Models",
        "abstract": (
            "Scaling laws are widely used to predict foundation model performance and guide "
            "compute allocation. Tabular foundation models (TFMs) differ from conventional "
            "foundation models in that they are pretrained on virtually unlimited synthetic "
            "data, while ultimately being evaluated on real-world datasets. We investigate "
            "whether scaling laws for TabPFNv2-style models reliably extrapolate to larger "
            "compute budgets. Our analysis reveals differences between synthetic and "
            "real-world scaling behavior, and shows that compute-optimal scaling requires "
            "expanding the range of synthetic pretraining dataset sizes alongside model size "
            "and training compute."
        ),
        "expected_relevance": "High",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2608.26923",
        "title": "TabuLM: Morphology-Aware Tabular Pre-training for Low-Resource Languages",
        "abstract": (
            "We present TabuLM, the first language model pre-trained on Kinyarwanda tabular "
            "data. TabuLM extends KinyaBERT-large, a two-tier morphological transformer, "
            "with additive row, column, and cell-type embeddings and a learned "
            "table-structure attention bias. Pre-training uses two new objectives: Masked "
            "Cell Recovery (MCR) and Column Type Prediction (CTP). We introduce TabQA-kin, "
            "the first native Kinyarwanda table question-answering benchmark comprising 526 "
            "QA pairs across 31 tables. TabuLM achieves 62.0% exact match on TabQA-kin, "
            "outperforming KinyaBERT-large by 5.7 EM points and all multilingual baselines "
            "by 11.7-12.7 points."
        ),
        "expected_relevance": "Medium",
        "expected_datasets": "TabQA-kin",
    },
    {
        "arxiv_id": "2611.01090",
        "title": "Numerical Embeddings for CTR Prediction: A Taxonomy, Unified Benchmark, and Open-Source FuxiCTR Extension",
        "abstract": (
            "Numerical embeddings map scalar features into vectors before a click-through "
            "rate (CTR) backbone combines the fields. NumEmbBench is the first open "
            "benchmark dedicated to comparing numerical embeddings for CTR prediction. We "
            "classify 18 configurations into six mechanism-based families and evaluate them "
            "through one FuxiCTR interface. After equal-budget validation tuning, we compare "
            "frozen configurations on three datasets, nine backbones, and five seeds. DEER "
            "has the best mean rank, but six methods lead at least one dataset-backbone "
            "setting."
        ),
        "expected_relevance": "Medium",
        "expected_datasets": "NumEmbBench",
    },
    {
        "arxiv_id": "2611.12942",
        "title": "Tabular Foundation Models vs Tuned Gradient Boosting for Telecom Churn: A Profit- and Calibration-Aware Evaluation",
        "abstract": (
            "A churn model is useful through the customers it selects for a retention "
            "offer. Tabular foundation models (TFMs) were recently reported to decisively "
            "outperform tree ensembles for churn; that comparison used untuned "
            "gradient-boosted trees and ranking metrics only. We ask whether the advantage "
            "holds against tuned GBDTs when judged by expected campaign profit. Four TFMs "
            "face LightGBM, XGBoost and CatBoost tuned with Optuna, on five public telecom "
            "datasets: Cell2Cell, Iranian, and Orange among them. TabPFN-3.5 earns "
            "significantly more expected maximum profit on two datasets, Cell2Cell (1.9%) "
            "and Iranian (7.6%)."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "Cell2Cell, Iranian, Orange",
    },
    {
        "arxiv_id": "2611.14462",
        "title": "Accurate predictions of properties of energetic materials with tabular foundation models",
        "abstract": (
            "We use TabPFN, a recently developed tabular foundation model, to predict three "
            "properties of energetic materials: impact sensitivity, decomposition "
            "temperature and crystal density. Without any hyperparameter tuning, TabPFN "
            "outperforms the best published models for all three properties. It also "
            "substantially outperforms a wide range of established machine-learning models, "
            "including tuned gradient boosting (XGBoost), random forests and Gaussian "
            "processes. TabPFN is also among the fastest models we consider, more than an "
            "order of magnitude faster than XGBoost."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    {
        "arxiv_id": "2610.39332",
        "title": "Tabular Foundation Models Dramatically Outperform Bespoke Photometric Redshift Estimators",
        "abstract": (
            "Estimating galaxy redshifts (photo-z's) from imaging data alone is essential "
            "for studies of extragalactic astrophysics and cosmology. We show that tabular "
            "foundation models (TFMs) can outperform bespoke estimators using only "
            "in-context learning. Evaluating on a widely used benchmark dataset, we find "
            "that TFMs predicting full probability distributions in a single forward pass "
            "systematically outperform bespoke estimators, matching or exceeding baselines "
            "trained on over 40,000 galaxies with just 1,000 training context examples."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "not stated",
    },
    # guard-rail: a real arXiv search false-positive. "differentiable tree attention" is
    # an incidental phrase in an LLM-pretraining paper, not actually about tabular data.
    {
        "arxiv_id": "2610.19601",
        "title": "PA1-OPD: One-Step Prefix-Augmented On-Policy Distillation for Language Model Pretraining",
        "abstract": (
            "Knowledge distillation (KD) improves language-model pretraining by matching "
            "teacher distributions at corpus prefixes, but provides no direct supervision "
            "at contexts induced by student predictions. We introduce PA1-OPD, which "
            "augments corpus-path distillation with teacher feedback after one "
            "student-sampled transition per selected prefix. Data-anchored roots support "
            "parallel sampling, and differentiable tree attention shares prefix computation "
            "without changing inference. In two continued-pretraining settings, full "
            "coverage improves held-out cross-entropy over KD across C4, PG-19, and Pile at "
            "every evaluated checkpoint."
        ),
        "expected_relevance": "Low",
        "expected_datasets": "C4, PG-19, Pile",
    },
]

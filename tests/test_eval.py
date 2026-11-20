from eval.dataset import EVAL_CASES
from eval.evaluate import _dataset_match

VALID_RELEVANCE = {"High", "Medium", "Low"}


def test_eval_set_size_in_target_range():
    assert 15 <= len(EVAL_CASES) <= 20, "target eval set size is 15-20 hand-labelled cases"


def test_eval_set_labels_valid():
    for case in EVAL_CASES:
        assert case["expected_relevance"] in VALID_RELEVANCE, case
        assert case["abstract"].strip()
        assert case["title"].strip()


def test_eval_set_has_guard_rail_case():
    """At least one case must be a clearly-irrelevant paper expected Low —
    catches the model defaulting everything to High."""
    assert any(c["expected_relevance"] == "Low" for c in EVAL_CASES)


def test_eval_set_has_high_case():
    """At least one genuinely-relevant case must exist, or high_recall (the
    metric that matters most on this class-imbalanced set) is undefined."""
    assert any(c["expected_relevance"] == "High" for c in EVAL_CASES)


def test_eval_set_ids_unique():
    ids = [c["arxiv_id"] for c in EVAL_CASES]
    assert len(ids) == len(set(ids))


def test_dataset_match_exact_not_stated():
    assert _dataset_match("not stated", "not stated")
    assert not _dataset_match("not stated", "OpenML-CC18")


def test_dataset_match_substring_either_direction():
    assert _dataset_match("OpenML-CC18", "OpenML-CC18, 72 datasets")
    assert _dataset_match("OpenML-CC18, 72 datasets", "openml-cc18")


def test_dataset_match_mismatch():
    assert not _dataset_match("ImageNet", "OpenML-CC18")

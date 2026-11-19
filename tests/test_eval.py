from eval.dataset import EVAL_CASES
from eval.evaluate import _dataset_match

VALID_RELEVANCE = {"High", "Medium", "Low"}


def test_eval_set_non_empty():
    assert len(EVAL_CASES) >= 2


def test_eval_set_labels_valid():
    for case in EVAL_CASES:
        assert case["expected_relevance"] in VALID_RELEVANCE, case
        assert case["abstract"].strip()
        assert case["title"].strip()


def test_eval_set_has_guard_rail_case():
    """At least one case must be a clearly-irrelevant paper expected Low —
    catches the model defaulting everything to High."""
    assert any(c["expected_relevance"] == "Low" for c in EVAL_CASES)


def test_dataset_match_exact_not_stated():
    assert _dataset_match("not stated", "not stated")
    assert not _dataset_match("not stated", "OpenML-CC18")


def test_dataset_match_substring_either_direction():
    assert _dataset_match("OpenML-CC18", "OpenML-CC18, 72 datasets")
    assert _dataset_match("OpenML-CC18, 72 datasets", "openml-cc18")


def test_dataset_match_mismatch():
    assert not _dataset_match("ImageNet", "OpenML-CC18")

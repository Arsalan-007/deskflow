from agent.verify import final_relevance, verify_extraction

ABSTRACT = (
    "We introduce TabPFN v2, a single pretrained transformer for tabular "
    "classification requiring no per-dataset training. Evaluated on OpenML-CC18, "
    "72 datasets, it beats tuned gradient boosting on small (<10k-row) datasets."
)

GOOD_EXTRACTION = {
    "summary": "Pretrained transformer for tabular classification, no per-dataset training.",
    "datasets": "OpenML-CC18, 72 datasets",
    "result": "Beats tuned gradient boosting on small (<10k-row) datasets",
    "relevance": "High",
    "confidence": "high",
}


def test_good_extraction_verifies():
    verified, errors = verify_extraction(ABSTRACT, GOOD_EXTRACTION)
    assert verified, errors


def test_not_stated_always_grounded():
    """Lesson 1: abstaining with 'not stated' is valid, not a failure —
    even with no other content to check against."""
    extraction = {**GOOD_EXTRACTION, "datasets": "not stated", "result": "not stated"}
    verified, errors = verify_extraction(ABSTRACT, extraction)
    assert verified, errors


def test_paraphrased_result_still_grounds():
    """Lesson 3: grounding is token-overlap, not exact substring — a
    reworded-but-faithful result shouldn't be flagged as unsupported."""
    extraction = {**GOOD_EXTRACTION, "result": "Outperforms tuned gradient boosting on small datasets under 10k rows"}
    verified, errors = verify_extraction(ABSTRACT, extraction)
    assert verified, errors


def test_invented_dataset_fails_grounding():
    extraction = {**GOOD_EXTRACTION, "datasets": "ImageNet-21k and LAION-5B"}
    verified, errors = verify_extraction(ABSTRACT, extraction)
    assert not verified
    assert any("not grounded" in e for e in errors)


def test_bad_relevance_enum_fails():
    extraction = {**GOOD_EXTRACTION, "relevance": "Super High"}
    verified, errors = verify_extraction(ABSTRACT, extraction)
    assert not verified
    assert any("relevance" in e for e in errors)


def test_missing_fields_fail_gracefully_not_crash():
    verified, errors = verify_extraction(ABSTRACT, {})
    assert not verified
    assert len(errors) >= 3


def test_low_confidence_forces_needs_review():
    extraction = {**GOOD_EXTRACTION, "confidence": "low"}
    assert final_relevance(extraction) == "Needs Review"


def test_high_confidence_keeps_stated_relevance():
    assert final_relevance(GOOD_EXTRACTION) == "High"

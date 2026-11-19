import pytest

from agent.config import ProjectConfig, load_project_config, project_config


def test_real_config_file_loads():
    loaded = load_project_config("deskflow.config.yaml")
    assert loaded.topics
    assert loaded.lookback_days > 0


def test_module_level_config_matches_file():
    assert project_config.topics


def test_empty_topics_rejected():
    with pytest.raises(ValueError):
        ProjectConfig(
            topics=[],
            research_interests="x",
            relevance_rubric={"High": "a", "Medium": "b", "Low": "c"},
            lookback_days=7,
            schedule_cron="0 8 * * 1",
        )

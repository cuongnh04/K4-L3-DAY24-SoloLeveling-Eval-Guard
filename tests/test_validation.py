"""Reject unusable evaluator/judge evidence before exporting a submission."""
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src.phase_a_ragas import run_ragas_50q
from src.phase_b_judge import cohen_kappa, pairwise_judge, bias_report


@pytest.mark.parametrize("rows,models", [([], ["model"]), ([None], [])])
def test_ragas_rejects_incomplete_evidence(monkeypatch, rows, models):
    evaluator = Mock(return_value={"per_question": rows, "metadata": {"evaluator_models": models}})
    monkeypatch.setitem(sys.modules, "src.m4_eval", SimpleNamespace(evaluate_ragas=evaluator))
    with pytest.raises(ValueError):
        run_ragas_50q([dict(id=1, distribution="factual", question="Q", answer="A",
                           contexts=["C"], ground_truth="R")])


@pytest.mark.parametrize("labels,humans", [([], []), ([1], [1, 0]), ([True], [1]), ([2], [0])])
def test_kappa_rejects_invalid_labels(labels, humans):
    with pytest.raises(ValueError):
        cohen_kappa(labels, humans)


def test_empty_bias_has_complete_shape():
    report = bias_report([])
    assert report["position_bias_count"] == 0
    assert report["verbosity_details"]["total_decisive"] == 0


def test_pairwise_rejects_out_of_range_score(openai_client):
    openai_client.chat.completions.create.return_value.choices[0].message.content = (
        '{"winner":"A","reasoning":"test","scores":{"A":2,"B":0}}'
    )
    with pytest.raises(ValueError):
        pairwise_judge("Q", "A", "B", "Reference")

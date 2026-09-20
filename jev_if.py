"""Use a Jev yes/no probability as a Python if condition."""

from typing import Any

from typesafe_sdk import Noul, TypeSafeClient


def jev_probability(
    question: str,
    *,
    state: Any,
    model: str = "jev-latest",
) -> float:
    """Return Jev's probability of yes. API errors propagate to the caller.

    `state` must be JSON-serializable. Authentication uses TYPESAFE_API_KEY.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question must be a nonempty string")

    with TypeSafeClient() as client:
        response = client.system_one(
            model=model,
            state=state,
            questions={"condition": Noul(instructions=question)},
        )
        probability = response.nouls["condition"].noul

    if not 0 <= probability <= 1:
        raise ValueError("Jev returned a probability outside [0, 1]")
    return probability


def jev(
    question: str,
    *,
    state: Any,
    threshold: float = 0.5,
    model: str = "jev-latest",
) -> bool:
    """Return True when Jev's yes probability is at least `threshold`.

    Each call makes an API request. Failures raise an exception, not False.
    """
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    return jev_probability(question, state=state, model=model) >= threshold

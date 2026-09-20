import unittest
from unittest.mock import patch

from typesafe_sdk import SystemOneResponse

from jev_if import jev, jev_probability


def api_response(probability):
    return SystemOneResponse.model_validate(
        {
            "model": "test",
            "answers": {"condition": {"type": "noul", "noul": probability}},
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
    )


class JevTests(unittest.TestCase):
    def setUp(self):
        patcher = patch("jev_if.TypeSafeClient")
        self.client_class = patcher.start()
        self.addCleanup(patcher.stop)
        self.client = self.client_class.return_value.__enter__.return_value

    def test_threshold_boundary(self):
        for probability, threshold, expected in [
            (0.79, 0.8, False),
            (0.8, 0.8, True),
            (0.81, 0.8, True),
            (0, 0.5, False),
            (1, 1, True),
        ]:
            with self.subTest(probability=probability, threshold=threshold):
                self.client.system_one.return_value = api_response(probability)
                self.assertIs(jev("返金希望ですか？", state={}, threshold=threshold), expected)

    def test_default_threshold(self):
        self.client.system_one.return_value = api_response(0.5)
        self.assertIs(jev("返金希望ですか？", state={}), True)

    def test_question_state_and_model_are_forwarded(self):
        self.client.system_one.return_value = api_response(0.75)
        state = {"message": "返金してください"}
        probability = jev_probability("返金希望ですか？", state=state, model="test-model")
        self.assertEqual(probability, 0.75)
        self.client.system_one.assert_called_once()
        kwargs = self.client.system_one.call_args.kwargs
        self.assertEqual(kwargs["state"], state)
        self.assertEqual(kwargs["model"], "test-model")
        self.assertEqual(kwargs["questions"]["condition"].instructions, "返金希望ですか？")
        self.client_class.return_value.__exit__.assert_called_once()

    def test_invalid_threshold_does_not_call_api(self):
        for threshold in [-0.1, 1.1, float("nan"), float("inf")]:
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError):
                    jev("返金希望ですか？", state={}, threshold=threshold)
        self.client_class.assert_not_called()

    def test_empty_question_does_not_call_api(self):
        for question in ["", " \n"]:
            with self.subTest(question=question):
                with self.assertRaises(ValueError):
                    jev(question, state={})
        self.client_class.assert_not_called()

    def test_api_error_is_not_a_negative_decision(self):
        self.client.system_one.side_effect = RuntimeError("API unavailable")
        with self.assertRaisesRegex(RuntimeError, "API unavailable"):
            jev("返金希望ですか？", state={})

    def test_missing_answer_is_not_a_negative_decision(self):
        response = api_response(0.9)
        response.answers.clear()
        self.client.system_one.return_value = response
        with self.assertRaises(KeyError):
            jev("返金希望ですか？", state={})


if __name__ == "__main__":
    unittest.main()

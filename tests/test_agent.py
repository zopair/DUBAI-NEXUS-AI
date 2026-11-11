import unittest

from app.agent import build_plan, detect_language, resolve_intent
from app.policy import evaluate_action


class AgentTests(unittest.TestCase):
    def test_arabic_message_detects_arabic(self):
        self.assertEqual(detect_language("أريد تقريراً"), "ar")

    def test_english_message_detects_english(self):
        self.assertEqual(detect_language("Create a report"), "en")

    def test_report_intent(self):
        self.assertEqual(resolve_intent("Please summarize this report"), "report")

    def test_sensitive_send_requires_approval(self):
        plan = build_plan("أرسل رسالة إلى العميل")
        send = [step for step in plan.steps if step.action == "send"][0]
        self.assertTrue(send.requires_approval)
        self.assertEqual(send.status, "awaiting_approval")

    def test_unknown_action_denied(self):
        self.assertFalse(evaluate_action("execute_shell").allowed)

    def test_empty_request_rejected(self):
        with self.assertRaises(ValueError):
            build_plan("  ")

    def test_non_string_request_rejected(self):
        with self.assertRaises(ValueError):
            build_plan(None)


if __name__ == "__main__":
    unittest.main()

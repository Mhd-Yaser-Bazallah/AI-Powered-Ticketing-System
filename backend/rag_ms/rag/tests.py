from django.test import TestCase

from rag.core.retriever import _build_filter
from rag.core.graphs.chat_graph import _detect_smalltalk, _should_rewrite, _split_multi_questions, should_rerank


class TenantIsolationFilterTests(TestCase):
    def test_build_filter_includes_company_id(self):
        q_filter = _build_filter(7, {"category": "billing"})
        must = getattr(q_filter, "must", []) or []
        keys = [getattr(cond, "key", None) for cond in must]
        self.assertIn("company_id", keys)
        self.assertIn("category", keys)


class ChatGraphHeuristicsTests(TestCase):
    def test_smalltalk_greeting(self):
        matched, response = _detect_smalltalk("Hi there")
        self.assertTrue(matched)
        self.assertIn("help", response.lower())

    def test_should_rewrite_skips_without_context(self):
        state = {"user_message": "How do I reset my password?", "summary": ""}
        self.assertFalse(_should_rewrite(state))

    def test_should_rewrite_short_followup_with_summary(self):
        state = {"user_message": "why?", "summary": "Previous context about billing issue."}
        self.assertTrue(_should_rewrite(state))

    def test_multi_question_split(self):
        parts = _split_multi_questions("How do I reset my password? And how do I update my email?")
        self.assertEqual(len(parts), 2)


class ConditionalRerankTests(TestCase):
    def test_rerank_triggered_by_count(self):
        decision, info = should_rerank("test query", 6, [0.9, 0.7])
        self.assertTrue(decision)
        self.assertEqual(info["reason"], "count")

    def test_rerank_triggered_by_close_scores(self):
        decision, info = should_rerank("test query", 2, [0.82, 0.80])
        self.assertTrue(decision)
        self.assertEqual(info["reason"], "close_scores")

    def test_rerank_triggered_by_policy_like(self):
        decision, info = should_rerank("policy compliance requirement", 1, [0.9])
        self.assertTrue(decision)
        self.assertEqual(info["reason"], "policy_like")

    def test_rerank_not_triggered(self):
        decision, info = should_rerank("hello world", 2, [0.9, 0.5])
        self.assertFalse(decision)
        self.assertEqual(info["reason"], "none")

import unittest
from datetime import datetime, timezone

from chronoai.resolvers.atmosphere_resolver import AtmosphereResolver


class AtmosphereResolverTests(unittest.TestCase):
    def test_boot_window(self):
        now = datetime(2026, 1, 1, 7, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "boot")

    def test_inference_window(self):
        now = datetime(2026, 1, 1, 13, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "inference")

    def test_optimization_window(self):
        now = datetime(2026, 1, 1, 20, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "optimization")

    def test_research_window(self):
        now = datetime(2026, 1, 1, 23, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "research")


if __name__ == "__main__":
    unittest.main()

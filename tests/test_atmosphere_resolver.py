import unittest
from datetime import datetime, timezone

from chronoai.resolvers.atmosphere_resolver import AtmosphereResolver


class AtmosphereResolverTests(unittest.TestCase):
    def test_boot_window(self):
        now = datetime(2026, 1, 1, 6, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "boot")
        now_mid = datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now_mid), "boot")

    def test_inference_window(self):
        now = datetime(2026, 1, 1, 11, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "inference")
        now_mid = datetime(2026, 1, 1, 14, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now_mid), "inference")

    def test_optimization_window(self):
        now = datetime(2026, 1, 1, 17, 30, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "optimization")
        now_mid = datetime(2026, 1, 1, 19, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now_mid), "optimization")

    def test_research_window(self):
        now = datetime(2026, 1, 1, 21, 30, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now), "research")
        now_mid = datetime(2026, 1, 1, 3, 0, tzinfo=timezone.utc)
        self.assertEqual(AtmosphereResolver.resolve_mode(now_mid), "research")


if __name__ == "__main__":
    unittest.main()

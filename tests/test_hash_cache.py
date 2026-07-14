import os
import tempfile
import unittest

from chronoai.cache.hash_cache import HashCache


class HashCacheTests(unittest.TestCase):
    def test_compute_is_stable(self):
        content = "ChronoAI"
        digest_one = HashCache.compute(content)
        digest_two = HashCache.compute(content)
        self.assertEqual(digest_one, digest_two)

    def test_read_write_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "sample.sha256")
            expected = HashCache.compute("abc")
            HashCache.write(path, expected)
            self.assertEqual(HashCache.read(path), expected)


if __name__ == "__main__":
    unittest.main()

import unittest

from chronoai.loaders.schema_validator import ThemeSchemaError, ThemeSchemaValidator


class ThemeSchemaValidatorTests(unittest.TestCase):
    def test_base_shape_is_valid(self):
        mapping = {
            "typing": {"speed": 80, "lines": []},
            "footer": {"text": "Always learning"},
            "quotes": [],
        }
        ThemeSchemaValidator.validate(mapping)

    def test_invalid_typing_type_raises(self):
        mapping = {
            "typing": "invalid",
            "footer": {"text": "Always learning"},
            "quotes": [],
        }
        with self.assertRaises(ThemeSchemaError):
            ThemeSchemaValidator.validate(mapping)


if __name__ == "__main__":
    unittest.main()

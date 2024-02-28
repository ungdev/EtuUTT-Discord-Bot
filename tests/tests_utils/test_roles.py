import pytest

from etuutt_bot.utils.role import parse_categories


class TestParseCategories:
    def test_not_set(self):
        """Test proper error handling when env is not set."""
        with pytest.raises(KeyError):
            parse_categories()

    @pytest.mark.parametrize(
        "categories",
        [
            "CAT1:3451,CAT2:notadigit",
            "NF04:46218976:0727875587",  # the second colon shouldn't be there
            "NF04:4621AE32",  # id in hex format
        ],
    )
    def test_wrong_values(self, categories, set_env):
        """Test proper error handling when wrong values are given"""
        set_env(UES_CATEGORIES=categories)
        with pytest.raises(ValueError):  # noqa PT011
            parse_categories()

    @pytest.mark.parametrize(
        ("categories", "expected"),
        [
            (
                "NF04:462189760727875587,NF05:462189760427175581",
                {"NF04": 462189760727875587, "NF05": 462189760427175581},
            )
        ],
    )
    def test_ok(self, categories, expected, set_env):
        """Test the happy path where everything is properly set up"""
        set_env(UES_CATEGORIES=categories)
        assert parse_categories() == expected

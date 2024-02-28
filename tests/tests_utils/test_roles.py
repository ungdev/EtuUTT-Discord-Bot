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
            "TC:46218976:0727875587",  # The second colon shouldn't be there
            "TC:4621AE32",  # ID in hex format
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
                "TC:462189760727875587,ME:462189760427175581",
                {"TC": 462189760727875587, "ME": 462189760427175581},
            )
        ],
    )
    def test_ok(self, categories, expected, set_env):
        """Test the happy path where everything is properly set up"""
        set_env(UES_CATEGORIES=categories)
        assert parse_categories() == expected

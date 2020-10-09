import pytest

from app.utils.i18n import I18nException, i18n


class TestI18n(object):
    def test_OK_can_translate(self) -> None:
        """[正常系]メッセージを取得することができる."""
        assert i18n.t("type_error.integer", "en") == "value is not a valid integer"

    def test_OK_can_translate_with_parameter(self) -> None:
        """[正常系]メッセージを取得することができる."""
        values = {"limit_value": 1}
        actual = i18n.t("value_error.number.not_ge", "en", **values)
        assert actual == "ensure this value is greater than or equal to 1"

    def test_NG_cannot_translate_when_locale_not_exist(self) -> None:
        """[異常系]ロケールが存在しないため、例外が投げられる."""
        with pytest.raises(I18nException) as e:
            i18n.t("type_error.integer", "XX")
        assert e.value.message == "locale XX does not exist."

    def test_NG_cannot_translate_when_key_not_exist(self) -> None:
        """[異常系]キーが存在しないため、例外が投げられる."""
        with pytest.raises(I18nException) as e:
            i18n.t("type_error.XXXX", "en")
        assert e.value.message == "key XXXX(type_error.XXXX) does not exist."

    def test_NG_cannot_translate_when_key_not_exist_and_partial_match(self) -> None:
        """[異常系]キーが存在しない(一部マッチしている)ため、例外が投げられる."""
        with pytest.raises(I18nException) as e:
            i18n.t("type_error.integer.XXXX", "en")
        assert e.value.message == "key type_error.integer.XXXX does not exist."

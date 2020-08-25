"""ドメインエラーモジュール."""


class DomainError(Exception):
    """ドメインエラー.

    Attribute:
        __message (str): メッセージ

    """

    def __init__(self, message: str) -> None:
        """初期化処理.

        Args:
            message (str): エラーメッセージ
        """
        self.__message = message

    @property
    def message(self) -> str:
        """エラーメッセージを返します.

        Returns:
            str: エラーメッセージ
        """
        return self.__message

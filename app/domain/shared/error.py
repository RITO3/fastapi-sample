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
        self.message = message

"""ページクラス.

ページは以下の情報を持ちます.
    * ページ
    * ページサイズ
    * ページ番号

"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class PageSize:
    """PageSizeクラス.

    Attributes:
        value (int): １ページあたりに取得する数
    """

    value: int


@dataclasses.dataclass(frozen=True)
class PageNumber:
    """PageNumberクラス.
    
    Attributes:
        value (int) : ページ番号
    """

    value: int


@dataclasses.dataclass(frozen=True)
class Page:
    """Pageクラス.

    Attributes:
        page_size (PageSize): ページサイズ
        page_number (PageNumber): ページ番号
    """

    page_size: PageSize
    page_number: PageNumber

    @property
    def offset(self) -> int:
        """オフセットを返します.

        Returns:
            int: オフセット.
        """
        return self.page_size.value * self.page_number.value

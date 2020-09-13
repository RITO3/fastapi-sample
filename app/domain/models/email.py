import dataclasses


@dataclasses.dataclass(frozen=True)
class Email:
    value: str

    def __str__(self) -> str:
        return self.value

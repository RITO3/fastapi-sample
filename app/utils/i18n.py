from typing import Any, Dict, List

import yaml


class I18nException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()


class I18n:
    def __init__(self, dir: str, locales: List[str]) -> None:
        self.__locales = locales
        self.__dir = dir
        self.__dict: Dict[str, Any] = dict()

    def load(self) -> None:
        for locale in self.__locales:
            file_path = f"{self.__dir}/{locale}.yaml"
            with open(file_path, "r") as file_stream:
                self.__dict.setdefault(locale, yaml.safe_load(file_stream))

    def t(self, key: str, locale: str, **args: Dict[str, Any]) -> str:
        local_object = self.__dict.get(locale)
        if local_object is None:
            raise I18nException(message=f"locale {locale} does not exist.")
        key_parts = key.split(".")
        message = None
        obj: Dict[str, Any] = local_object
        index = 0
        for current_key in key_parts:
            message = obj.get(current_key)
            if message is None:
                raise I18nException(message=f"key {current_key}({key}) does not exist.")

            if not isinstance(message, dict) and index != len(key_parts) - 1:
                raise I18nException(message=f"key {key} does not exist.")

            obj = message
            index = index + 1

        return str(message).format(**args)


i18n = I18n("./app/locales", ["ja", "en"])
i18n.load()

import abc

import argostranslate.package
import argostranslate.translate


class BaseTranslator(abc.ABC):
    @abc.abstractmethod
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        raise NotImplementedError


class ArgosTranslate(BaseTranslator):
    def _download_package(self, from_lang: str, to_lang: str) -> None:
        argostranslate.package.update_package_index()  # pyright: ignore
        available_packages = (
            argostranslate.package.get_available_packages()  # pyright: ignore
        )
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_lang and x.to_code == to_lang,
                available_packages,
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())
        # TODO: Raise error if package not found

    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        self._download_package(from_lang, to_lang)
        translated_text: str = (
            argostranslate.translate.translate(  # pyright: ignore
                text, from_lang, to_lang
            )
        )
        return translated_text

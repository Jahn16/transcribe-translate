from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.providers.translate import ArgosTranslate


@pytest.fixture
def sentences() -> list[str]:
    return ["Hello world", "Hello, how are you?"]


@pytest.fixture
def lang_packages() -> list[MagicMock]:
    package = MagicMock()
    package.from_code = "fr"
    package.to_code = "de"
    package2 = MagicMock()
    package2.from_code = "en"
    package2.to_code = "pt"
    return [package, package2]


def test_download_package(
    lang_packages: list[MagicMock], mocker: MockerFixture
) -> None:
    translator = ArgosTranslate()
    mocker.patch("app.providers.translate.argostranslate.translate")
    package_mock = mocker.patch(
        "app.providers.translate.argostranslate.package"
    )

    from_code, to_code = "en", "pt"
    package_mock.get_available_packages.return_value = lang_packages
    translator.translate("Hello world", from_code, to_code)

    package_mock.update_package_index.assert_called_once()
    package_mock.install_from_path.assert_called_once_with(
        lang_packages[1].download()
    )


def test_translate(
    sentences: list[str], lang_packages: list[MagicMock], mocker: MockerFixture
) -> None:
    translator = ArgosTranslate()
    translate_mock = mocker.patch(
        "app.providers.translate.argostranslate.translate"
    )
    package_mock = mocker.patch(
        "app.providers.translate.argostranslate.package"
    )
    package_mock.get_available_packages.return_value = lang_packages[1:]
    translation = "Olá mundo"
    translate_mock.translate.return_value = translation

    sentence = "Hello world"
    from_code, to_code = "en", "pt"
    result = translator.translate(sentence, from_code, to_code)

    translate_mock.translate.assert_called_once_with(
        sentences[0], from_code, to_code
    )
    assert result == translation

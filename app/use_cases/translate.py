from app.providers.translate import BaseTranslator


class TranslateUseCase:
    def __init__(self, translator: BaseTranslator):
        self._translator = translator

    def execute(self, text: str, from_lang: str, to_lang: str) -> str:
        return self._translator.translate(text, from_lang, to_lang)

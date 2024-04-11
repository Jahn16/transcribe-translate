from app.providers.translate import BaseTranslator


class TranslateUseCase:
    def __init__(self, translator: BaseTranslator):
        self._translator = translator

    def execute(
        self, sentences: list[str], from_lang: str, to_lang: str
    ) -> list[str]:
        translated_sentences = [
            self._translator.translate(sentence, from_lang, to_lang)
            for sentence in sentences
        ]
        return translated_sentences

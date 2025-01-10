from typing import Any
from dataclasses import dataclass


@dataclass
class TranslatorModel:
    _translator: Any
    source: str
    destination: str

    def translate(self, text: str) -> str:
        translation =  self._translator.translate(text, src=self.source, dest=self.destination)
        if translation: return translation.text
        return ""

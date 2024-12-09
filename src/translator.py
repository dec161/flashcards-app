from typing import Protocol


class ITranslator(Protocol):
    def translate(self, text) -> str: pass

    @property
    def src(self) -> str: pass

    @src.setter
    def src(self, value): pass

    @property
    def dst(self) -> str: pass

    @dst.setter
    def dst(self, value): pass


class Translator:
    def __init__(self, translator, source: str, destination):
        self.__translator = translator
        self.__src: str = source
        self.__dst = destination

    @property
    def src(self) -> str:
        return self.__src

    @src.setter
    def src(self, value):
        self.__src = value

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self, value):
        self.__dst = value

    def translate(self, text) -> str:
        translation =  self.__translator.translate(text, src=self.src, dest=self.dst)
        if translation: return translation.text
        return ""

from typing import Protocol


class ITranslatorModel(Protocol):
    source: str
    destination: str

    def translate(self, text: str) -> str: pass


class ITranslatorPresenter(Protocol):
    def translate(self) -> None: pass

    def show(self) -> None: pass

    def hide(self) -> None: pass


class ITranslatorView(Protocol):
    def bind_presenter(self,
                       translator_presenter: ITranslatorPresenter) -> None: pass

    def get_input(self) -> str: pass

    def set_output(self, text: str) -> None: pass

    def show(self) -> None: pass

    def hide(self) -> None: pass

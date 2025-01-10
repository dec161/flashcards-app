from dataclasses import dataclass
from tkinter import messagebox

from .protocols import ITranslatorModel, ITranslatorView


@dataclass
class TranslatorPresenter:
    _model: ITranslatorModel
    _view: ITranslatorView

    def translate(self) -> None:
        text = self._view.get_input()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для перевода")
            return

        translation = self._model.translate(text)
        if not translation:
            messagebox.showerror("Ошибка", "Не удалось получить перевод")
            return

        self._view.set_output(translation)

    def show(self) -> None:
        self._view.show()

    def hide(self) -> None:
        self._view.hide()

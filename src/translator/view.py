import tkinter as tk
from tkinter import ttk

from .protocols import ITranslatorPresenter


class TranslatorView(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._title_label = ttk.Label(self, text="Переводчик", font=("Arial", 24, "bold"), anchor="center")
        self._title_label.pack(pady=20)

        self._input_label = ttk.Label(self, text="Введите текст для перевода:", font=("Arial", 14))
        self._input_label.pack(pady=10)

        self._input_text = tk.Text(self, font=("Arial", 14), height=5, wrap=tk.WORD)
        self._input_text.pack(pady=5)

        self._result_label = ttk.Label(self, text="Результат перевода:", font=("Arial", 14))
        self._result_label.pack(pady=10)

        self._output_text = tk.Text(self, font=("Arial", 14), height=5, wrap=tk.WORD, state=tk.DISABLED)
        self._output_text.pack(pady=5)

        self._translate_button = ttk.Button(self, text="Перевести")
        self._translate_button.pack(pady=10)

    def bind_presenter(self, translator_presenter: ITranslatorPresenter) -> None:
        self._translate_button.config(command=translator_presenter.translate)
        self.protocol("WM_DELETE_WINDOW", translator_presenter.hide)

    def get_input(self) -> str:
        return self._input_text.get("1.0", tk.END).strip()

    def set_output(self, text: str) -> None:
        self._output_text.config(state=tk.NORMAL)
        self._output_text.delete("1.0", tk.END)
        self._output_text.insert(tk.END, text)
        self._output_text.config(state=tk.DISABLED)

    def show(self) -> None:
        self.deiconify()

    def hide(self) -> None:
        self.withdraw()

import tkinter as tk

from numpy import random
from googletrans import Translator

from flashcards.model import WeightedFlashcardList
from flashcards.view import FlashcardsView
from flashcards.presenter import FlashcardsPresenter
from translator.view import TranslatorView
from translator.model import TranslatorModel
from translator.presenter import TranslatorPresenter


def main() -> None:
    translator_model = TranslatorModel(Translator(), "en", "ru")
    flashcards_model = WeightedFlashcardList(
        random.default_rng(),
        **{
            "cat": "кот",
            "dog": "собака",
            "apple": "яблоко",
            "car": "машина",
            "house": "дом",
            "sun": "солнце",
            "moon": "луна",
            "tree": "дерево",
            "sky": "небо",
            "water": "вода"
        }
    )

    root = tk.Tk()
    root.title("Угадалка от нас")
    root.geometry("1200x600")
    root.config(bg="#2e2e2e")

    flashcards_view = FlashcardsView(master=root)
    translator_view = TranslatorView(master=flashcards_view)
    translator_view.hide()
    flashcards_view.pack(fill=tk.BOTH, expand=True)

    translator_presenter = TranslatorPresenter(translator_model, translator_view)
    flashcards_presenter = FlashcardsPresenter(
        flashcards_model,
        flashcards_view,  # noqa
        translator_presenter
    )

    flashcards_view.bind_presenter(flashcards_presenter=flashcards_presenter)

    root.mainloop()

if __name__ == "__main__":
    main()

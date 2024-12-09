import tkinter as tk

from numpy.random import default_rng
from googletrans import Translator as GoogleTranslator

from gui import FlashcardGUI, TranslatorGUI
from flashcards import WeightedFlashcardList
from translator import Translator


def main():
    root = tk.Tk()
    root.title("Угадалка от нас")
    root.geometry("1200x600")
    root.configure(bg="#2e2e2e")

    flashcards_frame = tk.Frame(root, bg="#2e2e2e")
    flashcards_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    flashcard_source = WeightedFlashcardList(
        default_rng(),
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
    FlashcardGUI(flashcards_frame, flashcard_source)

    translator_frame = tk.Frame(root, bg="#2e2e2e")
    translator_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    translator = Translator(GoogleTranslator(), "en", "ru")
    TranslatorGUI(translator_frame, translator)  # noqa (баг с определением типа, отключил проверку комментом)

    # TODO: добавить режим теста и график

    root.mainloop()


if __name__ == "__main__":
    main()

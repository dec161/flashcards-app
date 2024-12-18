import tkinter as tk
from tkinter import ttk

from numpy.random import default_rng
from googletrans import Translator as GoogleTranslator

from gui.flashcards import FlashcardGUI
from gui.translator import TranslatorGUI
from gui.testmode import TestModeGUI
from classes.flashcards import WeightedFlashcardList
from classes.translator import Translator


def main():
    root = tk.Tk()
    root.title("Угадалка от нас")
    root.geometry("1200x600")
    root.configure(bg="#2e2e2e")

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
    flashcards_frame = tk.Frame(root, bg="#2e2e2e")
    flashcard_gui = FlashcardGUI(flashcards_frame, flashcard_source)
    flashcards_frame.pack(fill=tk.BOTH, expand=True)

    translator_window = tk.Toplevel(root, bg="#2e2e2e")
    translator_window.protocol("WM_DELETE_WINDOW", translator_window.withdraw)
    translator_window.withdraw()
    TranslatorGUI(translator_window, Translator(GoogleTranslator(), "en", "ru"))  # noqa

    open_translator = ttk.Button(root, text="Открыть переводчик", command=translator_window.deiconify)
    open_translator.pack(expand=True)

    def start_test():
        open_translator["state"] = "disabled"
        translator_window.withdraw()
        flashcard_gui.show_word()
        flashcard_gui.reset_answers()

    def end_test():
        open_translator["state"] = "normal"
        flashcard_gui.clear_word()
        flashcard_gui.save_progress()

    TestModeGUI(
        root,
        start_test,
        end_test
    )

    root.mainloop()


if __name__ == "__main__":
    main()

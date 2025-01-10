from typing import Protocol, Iterable


class IFlashcardsModel(Protocol):
    def next(self) -> None: pass

    @property
    def current_word(self) -> str: pass

    @property
    def current_translation(self) -> str: pass

    def correct_answer(self) -> None: pass

    def incorrect_answer(self) -> None: pass

    @property
    def total_correct(self) -> int: pass

    @property
    def total_incorrect(self) -> int: pass

    def reset_answers(self) -> None: pass

    def save_progress(self) -> None: pass

    def get_correct(self) -> Iterable: pass

    def get_incorrect(self) -> Iterable: pass


class IFlashcardsPresenter(Protocol):
    def show_word(self) -> None: pass

    def check_translation(self) -> None: pass

    def begin_test(self) -> None: pass

    def end_test(self) -> None: pass

    def show_progress(self) -> None: pass

    def show_translator(self) -> None: pass


class IFlashcardsView(Protocol):
    def bind_presenter(self,
                       flashcards_presenter: IFlashcardsPresenter) -> None: pass

    def focus_entry(self) -> None: pass

    def show_timer(self) -> None: pass

    def hide_timer(self) -> None: pass

    def get_answer(self) -> str: pass

    def set_word(self, word: str) -> None: pass

    def set_message(self, text: str, *, foreground: str) -> None: pass

    def set_stats(self, *, correct: int, incorrect: int) -> None: pass

    def set_translator_button_state(self, state: str) -> None: pass

    def start_timer(self) -> None: pass

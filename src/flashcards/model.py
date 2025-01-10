from dataclasses import dataclass, field
from functools import cache
from typing import Iterable


@dataclass
class Flashcard:
    """Карточка слова/предложения с переводом и счётчиками (не)правильных ответов."""

    _word: str
    _translation: str
    _correct: int = field(default=0, init=False)
    _incorrect: int = field(default=0, init=False)

    @property
    def word(self) -> str:
        return self._word

    @property
    def translation(self) -> str:
        return self._translation

    @property
    def correct(self) -> int:
        return self._correct

    def inc_correct(self) -> None:
        self._correct += 1

    @property
    def incorrect(self) -> int:
        return self._incorrect

    def inc_incorrect(self) -> None:
        self._incorrect += 1

    @property
    def ratio(self) -> float:
        return (self.incorrect + 1) / (self.correct + 1)

    def reset_counters(self) -> None:
        self._correct = 0
        self._incorrect = 0


class WeightedFlashcardList:
    def __init__(self, rng, *cards, **words) -> None:
        self._rng = rng

        flashcards = {}

        if words:
            flashcards.update(**{word: Flashcard(word, translation) for word, translation in words.items()})

        if cards:
            flashcards.update(**{card.word: card for card in cards})

        self._flashcards = flashcards
        self._current = ""

        self._total_correct = 0
        self._total_incorrect = 0

        for card in self._flashcards.values():
            self._total_correct += card.correct
            self._total_incorrect += card.incorrect

        self._progress = []

    @cache
    def _total_ratio(self) -> float:
        return sum([card.ratio for card in self._flashcards.values()])

    def _probability(self, card) -> float:
        return card.ratio / self._total_ratio()

    def next(self) -> None:
        probability_dist = [self._probability(card) for card in self._flashcards.values()]

        new = self._rng.choice(list(self._flashcards.keys()), p=probability_dist)
        while self._current == new:
            new = self._rng.choice(list(self._flashcards.keys()), p=probability_dist)

        self._current = new

    @property
    def current_word(self) -> str:
        return self._current

    @property
    def current_translation(self) -> str:
        if not self.current_word:
            return ""

        return self._flashcards[self.current_word].translation

    def correct_answer(self):
        self._flashcards[self.current_word].inc_correct()
        self._total_correct += 1
        self._total_ratio.cache_clear()

    def incorrect_answer(self):
        self._flashcards[self.current_word].inc_incorrect()
        self._total_incorrect += 1
        self._total_ratio.cache_clear()

    @property
    def total_correct(self):
        return self._total_correct

    @property
    def total_incorrect(self):
        return self._total_incorrect

    def reset_answers(self):
        for card in self._flashcards.values():
            card.reset()

    def clear_word(self):
        self._current = None

    def save_progress(self):
        self._progress.append({"correct": self.total_correct, "incorrect": self.total_incorrect})

    def get_correct(self) -> Iterable:
        return [entry["correct"] for entry in self._progress]

    def get_incorrect(self) -> Iterable:
        return [entry["incorrect"] for entry in self._progress]

    def try_add_flashcard(self, flashcard):
        if self._flashcards.get(flashcard.word):
            return False

        self._flashcards[flashcard.word] = flashcard
        return True

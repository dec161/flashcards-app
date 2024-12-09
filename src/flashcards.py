from typing import Protocol

class Flashcard:
    """Карточка слова/предложения с переводом и счётчиками (не)правильных ответов."""

    def __init__(self, word, translation):
        self.__word = word
        self.__translation = translation
        self.__correct = 0
        self.__wrong = 0

    @property
    def word(self):
        return self.__word

    @property
    def translation(self):
        return self.__translation

    @property
    def correct(self):
        return self.__correct

    def inc_correct(self):
        self.__correct += 1

    @property
    def wrong(self):
        return self.__wrong

    def inc_wrong(self):
        self.__wrong += 1


class IFlashcardSource(Protocol):
    def next(self):
        pass

    @property
    def current_word(self): pass

    @property
    def current_translation(self): pass

    def correct_answer(self): pass

    def wrong_answer(self): pass

    @property
    def total_correct(self) -> int: pass

    @property
    def total_wrong(self) -> int: pass


class WeightedFlashcardList:
    def __init__(self, rng, *cards, **words):
        self.__rng = rng

        flashcards = {}

        if words:
            flashcards.update(**{word: Flashcard(word, translation) for word, translation in words.items()})

        if cards:
            flashcards.update(**{card.word: card for card in cards})

        self.__flashcards = flashcards
        self.__current = None

        self.__total_correct = 0
        self.__total_wrong = 0

        for card in self.__flashcards.values():
            self.__total_correct += card.correct
            self.__total_wrong += card.wrong

    def next(self):
        probability_dist = [(card.wrong + 1) / (self.__total_wrong + len(self.__flashcards))
                            for card in self.__flashcards.values()]
        self.__current = self.__rng.choice(list(self.__flashcards.keys()), p=probability_dist)

    @property
    def current_word(self):
        return self.__current

    @property
    def current_translation(self):
        if not self.current_word:
            return None

        return self.__flashcards[self.current_word].translation

    def correct_answer(self):
        self.__flashcards[self.current_word].inc_correct()
        self.__total_correct += 1

    def wrong_answer(self):
        self.__flashcards[self.current_word].inc_wrong()
        self.__total_wrong += 1

    @property
    def total_correct(self):
        return self.__total_correct

    @property
    def total_wrong(self):
        return self.__total_wrong

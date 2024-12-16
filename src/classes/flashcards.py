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

    @property
    def wc_ratio(self):
        return (self.wrong + 1) / (self.correct + 1)

    def reset(self):
        self.__correct = 0
        self.__wrong = 0


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

        self.__total_ratio_cache = None

        for card in self.__flashcards.values():
            self.__total_correct += card.correct
            self.__total_wrong += card.wrong

        self.__progress = []

    @property
    def __total_wc_ratio(self):
        if not self.__total_ratio_cache:
            self.__total_ratio_cache = sum([card.wc_ratio for card in self.__flashcards.values()])
        return self.__total_ratio_cache

    def __calculate_probability(self, card):
        return card.wc_ratio / self.__total_wc_ratio

    def next(self):
        probability_dist = [self.__calculate_probability(card) for card in self.__flashcards.values()]
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
        self.__total_ratio_cache = None

    def wrong_answer(self):
        self.__flashcards[self.current_word].inc_wrong()
        self.__total_wrong += 1
        self.__total_ratio_cache = None

    @property
    def total_correct(self):
        return self.__total_correct

    @property
    def total_wrong(self):
        return self.__total_wrong

    def reset_answers(self):
        for card in self.__flashcards.values():
            card.reset()

    def clear_word(self):
        self.__current = None

    def save_progress(self):
        self.__progress.append({"correct": self.total_correct, "wrong": self.total_wrong})

    @property
    def progress(self):
        return self.__progress

    def try_add_flashcard(self, flashcard):
        if self.__flashcards.get(flashcard.word):
            return False

        self.__flashcards[flashcard.word] = flashcard
        return True

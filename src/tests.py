import unittest
from unittest.mock import Mock
from classes.flashcards import Flashcard, WeightedFlashcardList
from classes.translator import Translator
from gui.flashcards import FlashcardGUI
from tkinter import Tk


class TestFlashcard(unittest.TestCase):
    def test_flashcard_initialization(self):
        card = Flashcard("cat", "кот")
        
        self.assertEqual(card.word, "cat")
        self.assertEqual(card.translation, "кот")
        self.assertEqual(card.correct, 0)
        self.assertEqual(card.wrong, 0)

    def test_flashcard_correct_increment(self):
        card = Flashcard("cat", "кот")
        card.inc_correct()
        self.assertEqual(card.correct, 1)

    def test_flashcard_wrong_increment(self):
        card = Flashcard("cat", "кот")
        
        card.inc_wrong()
        
        self.assertEqual(card.wrong, 1)

    def test_flashcard_reset(self):
        card = Flashcard("cat", "кот")
        card.inc_correct()
        card.inc_wrong()
        
        card.reset()
        
        self.assertEqual(card.correct, 0)
        self.assertEqual(card.wrong, 0)

    def test_flashcard_wc_ratio(self):
        card = Flashcard("cat", "кот")
        card.inc_wrong()
        card.inc_wrong()
        card.inc_correct()
        
        self.assertAlmostEqual(card.wc_ratio, (2 + 1) / (1 + 1))


class TestWeightedFlashcardList(unittest.TestCase):
    def setUp(self):
        self.rng = Mock()
        self.rng.choice = Mock(return_value="cat")
        self.flashcards = WeightedFlashcardList(self.rng, cat="кот", dog="собака")

    def test_next_word(self):
        self.flashcards.next()
        
        self.assertEqual(self.flashcards.current_word, "cat")
        self.assertEqual(self.flashcards.current_translation, "кот")

    def test_correct_answer(self):
        self.flashcards.next()
        
        self.flashcards.correct_answer()
        
        self.assertEqual(self.flashcards.total_correct, 1)

    def test_wrong_answer(self):
        self.flashcards.next()
        
        self.flashcards.wrong_answer()
        
        self.assertEqual(self.flashcards.total_wrong, 1)

    def test_add_new_flashcard(self):
        new_card = Flashcard("tree", "дерево")
        
        result = self.flashcards.try_add_flashcard(new_card)
        
        self.assertTrue(result)
        self.assertIn(new_card, self.flashcards._WeightedFlashcardList__flashcards.values())  # noqa

    def test_save_progress(self):
        self.flashcards.next()
        self.flashcards.correct_answer()
        
        self.flashcards.save_progress()
        
        self.assertEqual(len(self.flashcards.progress), 1)
        self.assertEqual(self.flashcards.progress[0]["correct"], 1)
        self.assertEqual(self.flashcards.progress[0]["wrong"], 0)


class TestTranslator(unittest.TestCase):
    def setUp(self):
        mock_translator = Mock()
        mock_translator.translate = Mock(return_value=Mock(text="привет"))
        self.translator = Translator(mock_translator, "en", "ru")

    def test_translation(self):
        result = self.translator.translate("hello")
        
        self.assertEqual(result, "привет")

    def test_translation_empty(self):
        self.translator._Translator__translator.translate = Mock(return_value=None)  # noqa
        
        result = self.translator.translate("")
        
        self.assertEqual(result, "")


class TestFlashcardGUI(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.flashcards = Mock()
        self.gui = FlashcardGUI(self.root, self.flashcards)  # noqa

    def test_show_word(self):
        self.flashcards.next = Mock()
        self.flashcards.current_word = "cat"
        
        self.gui.show_word()
        
        self.assertEqual(self.gui._FlashcardGUI__word.get(), "cat")  # noqa

    def test_correct_answer(self):
        self.flashcards.correct_answer = Mock()
        
        self.gui._FlashcardGUI__correct_answer()  # noqa
        
        self.flashcards.correct_answer.assert_called_once()

    def test_wrong_answer(self):
        self.flashcards.wrong_answer = Mock()
        self.flashcards.current_translation = "кот"
        
        self.gui._FlashcardGUI__wrong_answer()  # noqa
        
        self.flashcards.wrong_answer.assert_called_once()


if __name__ == "__main__":
    unittest.main()

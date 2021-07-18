import Extractor
import enum

from GoogleExtractor import GoogleExtractor


class Extractor(enum.Enum):
	GOOGLE = 1

class AnswerRetriever:
	def __init__(self, extracter: Extractor = Extractor.GOOGLE):
		if extracter == Extractor.GOOGLE:
			self.extractor = GoogleExtractor()

	def get_answer(self, question: str) -> str:
		if question is None or question == '':
			raise Exception("Can't take empty string for question")

		return self.extractor.extract_answer(question)
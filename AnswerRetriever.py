import subprocess

import Extractor
import enum
import json

from GoogleUrlExtractor import GoogleUrlExtractor
from WikiPage import WikiPage

REQUEST_CONTENT_FILE = 'script/request_content.json'
REQUEST_SCRIPT = 'script/navie.sh'
RESULT_FILE = '/tmp/result.txt'

class Extractor(enum.Enum):
	GOOGLE = 1


class AnswerRetriever:
	def __init__(self, extracter: Extractor = Extractor.GOOGLE):
		if extracter == Extractor.GOOGLE:
			self.url_extractor = GoogleUrlExtractor()

	def get_answer(self, question: str) -> str:
		if question is None or question == '':
			raise Exception("Can't take empty string for question")

		url = self.url_extractor.extract_answer_url(question)

		wiki_page = WikiPage(url)
		self.prepare_question(wiki_page.get_data())
		self.send_request()
		print(self.retrieve_response())

		return ''

	def prepare_question(self, passage):
		json.dump(passage, open(REQUEST_CONTENT_FILE, 'w'))

	def send_request(self):
		subprocess.call(['sh', REQUEST_SCRIPT, REQUEST_CONTENT_FILE])

	def retrieve_response(self):
		return open(RESULT_FILE, 'r').readlines()
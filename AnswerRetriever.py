import subprocess

import Extractor
import enum
import json
import ast

from GoogleUrlExtractor import GoogleUrlExtractor
from WikiPage import WikiPage

REQUEST_CONTENT_FILE = '/Users/yvetteho/yvette/simple_flask/script/request_content.json'
REQUEST_SCRIPT = '/Users/yvetteho/yvette/simple_flask/script/navie.sh'
RESULT_FILE = '/tmp/result.txt'


class Extractor(enum.Enum):
	GOOGLE = 1

class AnswerRetriever:
	def __init__(self, extracter: Extractor = Extractor.GOOGLE):
		if extracter == Extractor.GOOGLE:
			self.url_extractor = GoogleUrlExtractor()

	def get_answer(self, question: str, url: str) -> dict:
		if question is None or question == '':
			raise Exception("Can't take empty string for question")

		wiki_page = WikiPage(url, question)
		wiki_data = wiki_page.get_data()
		self.prepare_question(wiki_data)
		self.send_request()
		response = self.retrieve_response()
		response_dict = ast.literal_eval(list(response)[0])
		print(response_dict)
		short_answer_dict = response_dict['short_answers'][0]
		long_answer_dict = response_dict['long_answer']
		print(long_answer_dict)
		# {'example_id': 1, 'yes_no_answer': 'NONE', 'short_answers_score': 2.685434669775068,
		#  'long_answer_score': 1.5318987159918693,
		#  'short_answers': [{'start_token': 187, 'end_token': 199, 'start_byte': -1, 'end_byte': -1}],
		#  'long_answer': {'start_token': 148, 'end_token': 3931, 'start_byte': -1, 'end_byte': -1}}
		tokens = wiki_page.tokens
		# print(tokens)
		tokens[int(short_answer_dict['start_token'])] = '<span id="short_answer" style="background-color: green">' + \
														tokens[int(short_answer_dict['start_token'])]
		tokens[int(short_answer_dict['end_token'])] += '</span>'

		tokens[int(long_answer_dict['start_token'])] = '<div id="long_answer" style="background-color: yellow">' + \
														tokens[int(long_answer_dict['start_token'])]
		tokens[int(long_answer_dict['end_token'])] += '</div>'

		answer = {
			'document_text': ' '.join(tokens),
			'short_answer': ' '.join(tokens[int(short_answer_dict['start_token']):int(short_answer_dict['end_token'])]),
			'long_answer': ' '.join(tokens[int(long_answer_dict['start_token']):int(long_answer_dict['end_token'])]),
		}
		print(answer)
		return answer
	# def get_answer(self, question: str) -> dict:
		# if question is None or question == '':
		# 	raise Exception("Can't take empty string for question")
		#
		# url = self.url_extractor.extract_answer_url(question)
		#
		# wiki_page = WikiPage(url, question)
		# wiki_data = wiki_page.get_data()
		# self.prepare_question(wiki_data)
		# # self.send_request()
		# response = self.retrieve_response()
		# response_dict = ast.literal_eval(list(response)[0])
		# print(response_dict)
		# short_answer_dict = response_dict['short_answers'][0]
		# long_answer_dict = response_dict['long_answer']
		# print(long_answer_dict)
		# # {'example_id': 1, 'yes_no_answer': 'NONE', 'short_answers_score': 2.685434669775068,
		# #  'long_answer_score': 1.5318987159918693,
		# #  'short_answers': [{'start_token': 187, 'end_token': 199, 'start_byte': -1, 'end_byte': -1}],
		# #  'long_answer': {'start_token': 148, 'end_token': 3931, 'start_byte': -1, 'end_byte': -1}}
		# tokens = wiki_page.tokens
		# # print(tokens)
		# tokens[int(short_answer_dict['start_token'])] = '<span id="short_answer" style="background-color: green">' + \
		# 												tokens[int(short_answer_dict['start_token'])]
		# tokens[int(short_answer_dict['end_token'])] += '</span>'
		#
		# tokens[int(long_answer_dict['start_token'])] = '<span id="long_answer" style="background-color: yellow">' + \
		# 												tokens[int(long_answer_dict['start_token'])]
		# tokens[int(long_answer_dict['end_token'])] += '</span>'
		#
		# answer = {
		# 	'document_text': ' '.join(tokens),
		# 	'short_answer': ' '.join(tokens[int(short_answer_dict['start_token']):int(short_answer_dict['end_token'])]),
		# 	'long_answer': ' '.join(tokens[int(long_answer_dict['start_token']):int(long_answer_dict['end_token'])]),
		# }
		# print(answer)
		# return answer

	def prepare_question(self, passage):
		print("========dump nq question to file========")
		with open(REQUEST_CONTENT_FILE, 'w') as f:
			f.write(json.dumps(passage))

	def send_request(self):
		print("========send request========")
		subprocess.call(['sh', REQUEST_SCRIPT, REQUEST_CONTENT_FILE])

	def retrieve_response(self):
		print("========read responses========")
		return open(RESULT_FILE, 'r').readlines()
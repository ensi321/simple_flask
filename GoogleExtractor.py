from typing import List

import requests
import urllib
from requests_html import HTMLSession


class GoogleExtractor:
	WIKI_URL = 'en.wikipedia.org'
	GOOGLE_QUERY_URL = 'https://www.google.com/search?q='

	def __init__(self):
		return

	def extract_answer_url(self, question: str) -> str:
		query_result = self.query_google(query=question + " site:" + self.WIKI_URL, result_prefix='https://' + self.WIKI_URL)

		if not query_result:
			raise Exception('No matching answer url found')

		return query_result[0]

	def query_google(self, query: str, result_contains: str = None, result_prefix: str = None,
	                 result_postfix: str = None) -> List[str]:
		query = urllib.parse.quote_plus(query)
		query = self.GOOGLE_QUERY_URL + query
		response = self.get_source(query)

		links = list(response.html.absolute_links)

		result = []
		for url in links[:]:
			if (result_contains is not None and result_contains in url) or \
					(result_prefix is not None and url.startswith(result_prefix) or
					 (result_postfix is not None and url.endswith(result_postfix))):
				result.append(url)

		return result

	def get_source(self, url: str):
		try:
			session = HTMLSession()
			response = session.get(url)
			return response

		except requests.exceptions.RequestException as e:
			print(e)


if __name__ == '__main__':
	g = GoogleExtractor()
	print(g.extract_answer_url("who is the US president"))

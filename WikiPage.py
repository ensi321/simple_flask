import requests
from bs4 import BeautifulSoup
import re
import json
import nltk


def remove_attrs(soup):
    for tag in soup.findAll(recursive=True):
        for attr in [attr for attr in tag.attrs if attr not in ["colspan"]]:
            del tag[attr]
        if "colspan" in tag.attrs:
            tag.name = tag.name + '_colspan' + '=' + "\"" + tag['colspan'] + "\""
            del tag['colspan']
        if tag.name == 'style':
            tag.extract()

    return soup


def capitalize_tags(soup):
    for tag in soup.findAll(recursive=True):
        tag.name = tag.name.capitalize()
    return soup


class WikiPage:
    def __init__(self, url, question):
        self.url = url
        self.question = question
        self.tokens = []
        self.document_text = ''
        self.long_answer_candidates = []

    def format_page(self):
        html = self.get_document_html()
        self.get_tokens(html)
        self.get_document_text()
        self.get_long_answer_candidates()

    def get_document_html(self):
        res = requests.get(self.url)
        return res.text

    def get_tokens(self, html):
        soup = BeautifulSoup(
            re.sub(r'</?(?!table|h1|h2|h3|p|th|tr|td|li|ul|dd|dl|ol|td_colspan|th_colspan)\w*\b[^>]*>', '',
                   str(remove_attrs(BeautifulSoup(html, "html.parser")))),
            "html.parser")

        soup = capitalize_tags(soup)

        result = ''
        for tag in soup.find_all(["Table", "H1", "H2", "H3", "P", "Tr", "Li", "Ul",
                                  "Dd", "Dl", "Ol", "Td_colspan", "Th_colspan"], recursive=False):

            if len(tag.get_text().replace('\n', '').replace(' ', '')) == 0:
                continue
            result += str(tag)

        result = result .replace('\n', '')
        # tokens = nltk.word_tokenize(result)
        # document_text = ' '.join(tokens)
        #
        # print(self.tokens)
        origin_tokens = result.replace('<', ' <').replace('>', '> ').split(' ')
        tokens = []
        for token in origin_tokens:
            if len(token) != 0:
                if token[0] != '<' or token[-1] != '>':
                    for new_token in nltk.word_tokenize(token):
                        tokens.append(new_token)
                else:
                    tokens.append(token)

        self.tokens = tokens

    def get_document_text(self):
        self.document_text = ' '.join(self.tokens).strip()

    def is_html_tag(self, element):
        if element[0] == '<' and element[-1] == '>':
            return True
        return False
    def get_document_tokens(self):
        # regex to get words, loop to get each start and end index
        res = []
        for ele in re.finditer(r'\S+', self.document_text):
            word = self.document_text[ele.start():ele.end()]
            res.append({
                "end_byte": ele.end() - 1,
                "html_token": self.is_html_tag(word),
                "start_byte": ele.start(),
                "token": word
            })
        # res = [(ele.start(), ele.end() - 1) for ele in re.finditer(r'\S+', self.document_text)]

        return res
    def get_long_answer_candidates(self):
        token_poses = dict()
        start = index = 0
        soup = capitalize_tags(BeautifulSoup(self.document_text, "html.parser"))

        for token in self.tokens:
            token_poses[start] = (token, index)
            start += len(token) + 1
            index += 1

        for tag in soup.find_all(["Table", "P", "Tr", "Li", "Ul"], recursive=True):
            # print(tag)
            start = 0
            is_top_level = True if tag.name in {'P', 'Table'} else False
            tokens = str(tag).replace('<', ' <').replace('>', '> ').split()
            tag = ' '.join(tokens).strip()
            pos = self.document_text.find(str(tag), start)
            while pos != -1:
                self.long_answer_candidates.append(
                    {'start_token': token_poses[pos][1], 'end_token': token_poses[pos][1] + len(tokens) - 1,
                     'top_level': is_top_level})
                pos = self.document_text.find(str(tag), pos + 1)

    def get_data(self):
        self.format_page()
        tokens = self.get_document_tokens()
        result = {
            "question_text": self.question,
            "example_id": "1",
            "long_answer_candidates": self.long_answer_candidates,
            "annotations": [],
            "document_tokens": tokens,
            "question_tokens": self.question.split(' ')
        }

        return result


# if __name__ == '__main__':
#     question = 'what do the 3 dots mean in math'
#     urls = scrape_google(question)
#     if len(urls) != 0:
#         wikiPage = WikiPage(urls[0], question)
#         wikiPage.get_data()


from flask import Flask, request

from AnswerRetriever import AnswerRetriever

app = Flask(__name__)


@app.errorhandler(Exception)
def server_error(err):
	app.logger.exception(err)
	return str(err), 500


@app.route('/', methods=['GET'])
def get_answer():
	question = request.args.get('question')
	ar = AnswerRetriever()
	return ar.get_answer(question)


if __name__ == '__main__':
	app.run()

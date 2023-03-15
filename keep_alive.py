from flask import Flask
import os
from threading import Thread

app = Flask('')


@app.route('/')
def main():
	return """Your bot is alive!
 <a href='/start'>restart</a>
 """


@app.route('/start')
def get_ses():
	os.system('kill 1')
	#os.system('python main.py')
	return ("<a href='/'>home</a>")


def run():
	app.run(host="0.0.0.0", port=8080)


def keep_alive():
	server = Thread(target=run)
	server.start()

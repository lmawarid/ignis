from flask import Flask, request
import messenger_bot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    return messenger_bot.receive_message(request)

if __name__ == '__main__':
    app.run()

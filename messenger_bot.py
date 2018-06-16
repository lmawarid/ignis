from pymessenger.bot import Bot
from secrets import SECRETS
import edamam

ACCESS_TOKEN = SECRETS['messenger']['access_token']
VERIFY_TOKEN = SECRETS['messenger']['verify_token']
bot = Bot(ACCESS_TOKEN)

def receive_message(request):
    if request.method == 'GET':
        return __handle_get_request(request)
    else:
        __handle_post_request(request)

    return 'Message Processed'

# private

def __handle_get_request(request):
    return __verify_fb_token(request)

def __verify_fb_token(request):
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'

def __handle_post_request(request):
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    __handle_text_message(message, recipient_id)
                if message['message'].get('attachments'):
                    __handle_attachments(message, recipient_id)

def __handle_text_message(message, recipient_id):
    original_message = message['message'].get('text')
    response_sent_text = edamam.recipes_for(original_message)

    #response_sent_text = message['message'].get('text')
    __send_message(recipient_id, response_sent_text)

def __handle_attachments(message, recipient_id):
    response_sent_attachment = message['message'].get('attachments')
    __send_message(recipient_id, response_sent_attachment)

def __send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

from pymessenger.bot import Bot
from secrets import secrets
import edamam

ACCESS_TOKEN = secrets['messenger']['access_token']
VERIFY_TOKEN = secrets['messenger']['verify_token']
NEW_RECIPE_LINE = "That's it! I've come up with a new recipe!"
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
    found_new_recipe, response_sent_text = edamam.recipes_for(original_message)

    if found_new_recipe:
        __send_message(recipient_id, NEW_RECIPE_LINE)

    __send_message(recipient_id, response_sent_text)

def __handle_attachments(message, recipient_id):
    response_sent_attachment = message['message'].get('attachments')
    __send_message(recipient_id, response_sent_attachment)

def __send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

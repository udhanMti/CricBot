from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
#from django.templatetags.static import static

chatbot = ChatBot(
    'CricBot',
    logic_adapters = [
         {   "import_path": "chatterbot.logic.BestMatch",
             "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
             "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
         },
         #{
            #  'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            #  'threshold': 0.65,
            #  'default_response': 'I am sorry, I do not understand.'
        # }
    ]
)
chatbot.set_trainer(ListTrainer)

for _file in os.listdir('/home/isuranga/mysite/static/data'):
   chat=open('/home/isuranga/mysite/static/data/'+_file,'r').readlines()
   chatbot.train(chat)

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)


def home(request, template_name="home.html"):
	context = {'title': 'CricBot'}
	return render_to_response(template_name, context)
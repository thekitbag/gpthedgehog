from webapp.main import bp
from flask import jsonify

import openai

from flask import json, request, current_app

@bp.route('/', methods=['GET'])
def home():
    return 'foo'

@bp.route('/test', methods=['GET'])
def test():
    return 'Working'

@bp.route('/ask', methods=['GET', 'POST'])
def ask():
    print(request.args)
    openai.api_key = current_app.config['GPT_API_KEY']
    user_message = request.args.get("q")
    
    system_message = "You are Hedgehog, a personal assistant that gives easy to understand answers \
                        to difficult questions for people who are less familiar with technology. \
                        Use analogies wherever possible and avoid jargon."
    
   
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ]
                    )
    
    answer = response["choices"][0]["message"]["content"]


    mock_answer = "Chat GPT (Generative Pretrained Transformer) is a machine learning model that's trained to generate \
                    human-like responses to text-based conversations. Think of it like a very smart friend who can listen \
                        to what you say and respond in a way that makes sense based on the context of the conversation. It's \
                            kind of like having a robot that can chat with you!"
    question = user_message
    result = {'question': question, 'answer': answer} 
    return jsonify(result)
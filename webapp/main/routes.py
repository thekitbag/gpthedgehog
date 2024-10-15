from webapp.main import bp
from webapp.models import User, Search
from flask_login import current_user

from flask import jsonify
from flask_login import login_required


import openai
import time, os

from flask import json, request, current_app

"""import speech_recognition as sr
from pydub import AudioSegment
import tempfile"""

"""The sending of a question to GPT should be a function or class of its own 
probably imported from a separate file, there is a lot of repitition and logic 
which doesnt belong in the routes file IYAM"""

@bp.route('/audio_question', methods=['POST'])
@login_required
def audio_question():
    if 'audio' in request.files:
        audio_file = request.files['audio']

        # Convert audio file to PCM WAV format using pydub
        try:
            audio_data = AudioSegment.from_file(audio_file)
            audio_data = audio_data.set_frame_rate(16000).set_channels(1)

            # Save the converted audio data to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
                audio_data.export(temp_audio_path, format='wav')

        # Create a SpeechRecognition recognizer instance
            recognizer = sr.Recognizer()
        
        except:
            print('failed to create recognizer instance')
            return "unable to transcribe question"

        # Perform speech recognition on the temporary audio file
        with sr.AudioFile(temp_audio_path) as audio:
            audio_data = recognizer.record(audio)
            try:
                text = recognizer.recognize_google(audio_data)
                openai.api_key = current_app.config['GPT_API_KEY']
                
                system_message = "You are Hedgehog, a personal assistant that gives easy to understand answers \
                                    to difficult questions especially but not limited to those relating to technology. \
                                    Your audience tend to be older and based in the UK. They generally have a good sense of humour  \
                                    but do not like to be patronised. When explaining complicated things, use analogies where appropriate and \
                                    avoid jargon. When giving an answer always finish by checking whether the user got the answer they wanted and \
                                    invite them to ask follow up questions if not. When a user asks you a silly question that an AI assistant could not answer \
                                    play along with their game rather than shutting it down."
                
                response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                        {"role": "system", "content": system_message},
                                        {"role": "user", "content": text}
                                    ]
                                )
                
                answer = response["choices"][0]["message"]["content"]
                result = {'question': text, 'answer': answer} 
                return jsonify(result)

            except Exception as error:
                print('failed to get a good response from chat GPT when asking:')
                print(text)
                print(error)
                return "unable to transcribe question"

        os.remove(temp_audio_path)

    else:
        return 'No audio file received'


@bp.route('/ask', methods=['GET'])
@login_required
def ask():
    user_message = request.args.get("q")
    openai.api_key = current_app.config['GPT_API_KEY']
    system_message = "You are Hedgehog, a personal assistant that gives easy to understand answers \
    to difficult questions especially but not limited to those relating to technology. \
    Your audience tend to be older and based in the UK. They generally have a good sense of humour  \
    but do not like to be patronised. When explaining complicated things, use analogies where appropriate and \
    avoid jargon. When giving an answer always finish by checking whether the user got the answer they wanted and \
    invite them to ask follow up questions if not. When a user asks you a silly question that an AI assistant could not answer \
    play along with their game rather than shutting it down."
    
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ]
                    )
    
    Search.save_search(user_id=current_user.id, query=user_message)
        
    answer = response["choices"][0]["message"]["content"]
    """time.sleep(3)
    mock_answer = "Chat GPT (Generative Pretrained Transformer) is a machine learning model that's trained to generate \
                    human-like responses to text-based conversations. Think of it like a very smart friend who can listen \
                        to what you say and respond in a way that makes sense based on the context of the conversation. It's \
                            kind of like having a robot that can chat with you!"
    
   """
    question = user_message
    result = {'question': question, 'answer': answer} 
    return jsonify(result)

@bp.route('/follow_up', methods=['POST'])
def follow_up():
    r = json.loads(request.data.decode('utf-8'))

    system_message = "You are Hedgehog, a personal assistant that gives easy to understand answers \
                        to difficult questions for people who are less familiar with technology. \
                        Use analogies wherever possible and avoid jargon."
    
    messages = [{"role": "system", "content": system_message}]

    for i in r['previousQuestions']:
        messages.append({"role": "user", "content": i["q"]})
        messages.append({"role": "assistant", "content": i["a"]})
    
    messages.append({"role": "user", "content": r['followUp']})

    
    openai.api_key = current_app.config['GPT_API_KEY']
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages)

    answer = response["choices"][0]["message"]["content"]
    """
    time.sleep(3)
    mock_answer = "Number two is the second counting number, which comes after one and before three. In terms of ranking, \
                number two is typically next in line after the best or most important thing, like the second-place winner in \
                a competition or the second choice on a list. So you can think of it like the silver medal in the Olympics: it's \
                not as good as first place, but it's still an impressive achievement."
    """
    result = {'question': r['followUp'], 'answer': answer}

    return jsonify(result)
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

from difflib import SequenceMatcher
from keras.preprocessing.sequence import pad_sequences

lemmatizer = WordNetLemmatizer()

#Importamos los archivos generados en el código anterior
intents = json.loads(open('./intents.json').read())
words = pickle.load(open('src/words.pkl', 'rb'))
classes = pickle.load(open('src/classes.pkl', 'rb'))
model = load_model('src/my_model.keras')

#Pasamos las palabras de oración a su forma raíz
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#Convertimos la información a unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    print(bag)
    return np.array(bag)

#Predecimos la categoría a la que pertenece la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res ==np.max(res))[0][0]
    category = classes[max_index]
    return category

#Obtenemos una respuesta aleatoria
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"]==tag:
            result = random.choice(i['responses'])
            break
    return result

# Función para determinar si la entrada del usuario coincide con alguno de los patrones
def matches_pattern(user_input, patterns):
    for pattern in patterns:
        similarity = SequenceMatcher(None, user_input, pattern).ratio()
        if similarity > 0.8:  # Ajusta este umbral según sea necesario
            return True
    return False

def chatbot_response(user_input):
    # Obtener los patrones asociados con la etiqueta predicha
    predicted_tag = predict_class(user_input)
    patterns = [pattern for intent in intents['intents'] if intent['tag'] == predicted_tag for pattern in intent['patterns']]
    # Verificar si la entrada del usuario coincide con alguno de los patrones
    if matches_pattern(user_input, patterns):
        # Si coincide, obtener una respuesta basada en la categoría predicha
        response = get_response(predicted_tag, intents)
    else:
        # Si no coincide, responder que no se comprendió la pregunta
        response = "Lo siento, no entendí tu pregunta. ¿Puedes intentarlo de nuevo?"
    return response

#Ejecutamos el chat en bucle
#terminarBucle = False
#while not terminarBucle:
#    message=input("")
#    if message == "bye":
#            terminarBucle = True
#    else:
#        res = chatbot_response(message)
#        print(res)
    
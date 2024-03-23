import constants
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import warnings
                                            
def get_formalities_response(formality) : #verifica si la formalidad del saludo esta en la lista
    if any(remove_punctuation_marks(formality).lower() in remove_punctuation_marks(greet).lower() for greet in constants.GREETING_INPUTS) :
        return random.choice(constants.GREETING_REPLIES)
    elif any(remove_punctuation_marks(formality).lower() in remove_punctuation_marks(thanks).lower() for thanks in constants.THANKS_INPUTS) :
        return random.choice(constants.THANKS_REPLIES)

def get_lemmatized_tokens(text) :
    normalized_tokens = nltk.word_tokenize(remove_punctuation_marks(text.lower())) #separa el texto en palabras individuales. list
    return [nltk.stem.WordNetLemmatizer().lemmatize(normalized_token) for normalized_token in normalized_tokens]
    #lematiza los tokens,pasa a su forma raiz es decir de donde deriva la palabra
    #estudiosos => estudioso    , aman => amar , felices => feliz
    #se normaliza y simplifica el texto para su analisis
    
    
def get_query_reply(query) :  #se usa un algoritmo matematico, para analizar la frecuencia de una palabra y en base a eso elige la respuesta. 
    documents.append(query)                                             #palabras vacias se sacan (a,is,the,are)
    tfidf_results = TfidfVectorizer(tokenizer = get_lemmatized_tokens, stop_words = constants.STOP_WORDS_SPANISH, ).fit_transform(documents)
    cosine_similarity_results = cosine_similarity(tfidf_results[-1], tfidf_results).flatten()
    best_index = cosine_similarity_results.argsort()[-2]
    documents.remove(query)
    if cosine_similarity_results[best_index] == 0 :
        return "Perdon pero no te entiendo!"
    else :
        return documents[best_index]

def remove_punctuation_marks(text) :  #eliminar caracteres , crea un dicc tipo tupla con el valor unicode del caracter
    punctuation_marks = dict((ord(punctuation_mark), None) for punctuation_mark in string.punctuation) 
    return text.translate(punctuation_marks) #elimina los caracteres con el mapeo previamente hecho

if __name__ == "__main__" :
    warnings.filterwarnings("ignore")

    try :
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try :
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    corpus = open('corpus.txt', 'r' , errors = 'ignore').read().lower()
    documents = nltk.sent_tokenize(corpus)

    print('RyuzakiBot: Mi nombre es RyuzakiBot. Esta vez fui modificado para responder otro tipo de preguntas. Si quieres salir escribe: bye')
    end_chat = False
    while end_chat == False :
        input_text = input()
        if remove_punctuation_marks(input_text).lower() != 'bye' :
            formality_reply = get_formalities_response(input_text)
            if  formality_reply :
                print('RyuzakiBot: ' + formality_reply)
            else :
                print('RyuzakiBot: ' + get_query_reply(input_text))
        else :
            print('RyuzakiBot: Adios! Cuidate.' + random.choice(constants.SWEETS))
            end_chat = True
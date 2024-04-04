import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz

#Para crear la red neuronal
from keras.models import Sequential
#Es una clase que permite crear modelos de manera secuencial, capa por capa. 
# Esta clase es comúnmente utilizada para construir modelos simples y en secuencia 
# donde la salida de una capa se convierte en la entrada de la siguiente.

from keras.layers import Dense, Activation, Dropout

#en dense se realiza la multiplicacion de matrices entre los datos de entrada y los pesos de la capa.
#en dropout se desactivan neuronas aleatoriamente para prevenir el sobreajuste(que neuronas influencien en otras).

from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('src/intents.json').read())

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def load_data(): 
    words = [] #palabras globales
    classes = []
    documents = [] #palabras por clase
    ignore_letters = ['?', '!', '¿', '.', ',']

    #Clasifica los patrones y las categorías
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    pickle.dump(words, open('src/words.pkl', 'wb'))
    pickle.dump(classes, open('src/classes.pkl', 'wb'))
    
    return words,classes,documents

def prepare_training_data(words,classes,documents):
    #Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
    training = []
    output_empty = [0]*len(classes)
    for document in documents:
        bag = []
        word_patterns = document[0] #lista de palabras de la categoria 
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns] #las de document no estaban lematizadas
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype="object") 
    print("training",training) 
        
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    
    return train_x,train_y

def create_model(train_x,train_y):
    #Creamos la red neuronal
    model = Sequential()
    model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    #Creamos el optimizador y lo compilamos
    sgd =SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

    return model
#Entrenamos el modelo y lo guardamos


def train_model(model, train_x, train_y):
    train_process = model.fit(np.array(train_x), np.array(train_y), epochs=10000, batch_size=128, verbose=1)
    model.save("src/my_model.keras", train_process)


# Cargar datos
words, classes, documents = load_data()

# Preparar datos de entrenamiento
train_x, train_y = prepare_training_data(words, classes, documents)

# Crear modelo
model = create_model(train_x, train_y)

# Entrenar y guardar modelo
train_model(model, train_x, train_y)
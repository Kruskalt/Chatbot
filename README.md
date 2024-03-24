# Chatbot
Equipo: Nazareno Avalos. 
        Matias Nissero.

Comisión: 1


# Introduccion

En esta segunda entrega presentaremos la documentación técnica y funcional del chatbot junto con su desarrollo y, además, incluiremos mejoras detectadas, contando la experiencia acerca de cómo nos embarcamos en el desarrollo de nuevas tecnologías como lo son la IA y el Machine Learning.
# Objetivos del chatbot

 Para comenzar, decidimos buscar en varias partes de internet, entre ellas YouTube y GitHub como las más relevantes, información sobre cómo comenzar a crear nuestro propio chatbot con alguna capacidad de inteligencia, pero quizá no tan avanzado por el momento.
 En nuestra búsqueda nos cruzamos con Ryuzaki Bot, un Chatbot hecho por Lucia Llavero, el cual además de otras, usa principalmente la biblioteca de Python, Scikit-Learn para obtener las respuestas más adecuadas para los usuarios a través de Machine Learning, además, puede ser fácilmente modificado para tomar las funciones que nosotros deseemos. En este caso, nos tomamos la libertad de modificarlo para que tome como su idioma de respuesta el español y modificamos su base de datos para satisfacer las dudas de los usuarios sobre el juego League of Legends, incluyendo un artículo de Wikipedia del juego y una biografía de un personaje del mismo.

# Modo de uso


 El uso del bot es simple, primero es necesario instalar las dependencias  necesarias para la ejecución. Lo haremos escribiendo en la consola el siguiente comando:   <font color="red">pip install -r requirements.txt</font> 

Luego, simplemente ejecutar el archivo bot_desktop.py y comenzar a hablar con el.

![](/imagenes/uso.png)


# Código 

## Main

Al principio de la ejecución, el programa filtra las warnings que pueden llegar a interrumpir con la continuación del mismo, luego, si no están instaladas, intenta descargar el tokenizador de frases punktokenizer, el cual se usa para dividir el texto en oraciones, además de WordNet, una base de datos léxica que se utiliza para el análisis semántico y la representación de palabras en la lingüística computacional.

 A continuación, toma archivo corpus.txt, el cual contiene la información que utilizará el chatbot para generar sus respuestas y lo guarda en la variable corpus, pero en lowercase. Luego, se tokeniza el contenido de la variable corpus y se guarda en documents.
 Cuando un texto se “tokeniza”, este es dividido en partes más pequeñas llamados tokens, los tokens pueden ser palabras, signos de puntuación, prefijos, sufijos, números, puntuación u otros elementos. La tokenización es una tarea fundamental en el procesamiento de lenguaje natural (NLP) y es el primer paso para procesar texto en una forma que pueda ser utilizada por algoritmos de aprendizaje automático o análisis lingüístico. 

![](/imagenes/main.png)
Luego, entramos en el ciclo el cual determina el flujo de ejecución del chatbot. Al principio, se toma el texto del usuario y se lo guarda en la variable input_text, en caso de que el input sea “bye” se dará fin a la ejecución, en caso contrario, hay dos caminos para tomar. En el primero se detecta que el input del usuario es una formalidad, en ese caso se llamará a la función get_formalities_response para responderle al usuario, en el otro caso, se llamará a get_query_reply para formular un texto relacionado a lo que consulta el usuario.

![](/imagenes/main2.png)


# Funciones


get_formalities_response<br>
Se verifica si el saludo del usuario es un saludo o un agradecimiento y de esta manera devuelve una respuesta adecuada. Las posibles entradas del usuario están guardadas en una variable llamada constants.

![](/imagenes/formalities.png)


get_lemmatized_tokens<br>
Primero, tokeniza el texto y luego devuelve una lista de esas palabras pero lematizadas, es decir, a su forma raíz. Por ejemplo, 'estudiosos' => 'estudioso'. Esto se hace para simplificar el texto y facilitar su análisis.

![](/imagenes/lemmatized.png)

get_query_reply<br>
Mediante el uso de un algoritmo llamado TF-IDF, se asigna un valor numérico a cada término encontrado en los documentos de acuerdo a la frecuencia con la que aparecen, lo que nos permite medir su relevancia. Luego, al comparar el coseno de la consulta con cada uno de los resultados, se genera una matriz unidimensional. Esta matriz se ordena de forma ascendente y se selecciona el elemento en la posición -2, ya que el último elemento corresponde a la comparación con la misma consulta. 
Si la similitud es mayor a cero significa que hubo éxito y se devuelve una respuesta de lo que busca el usuario.

ejemplo:<br> 
cosine_similarity_results = [0.4, 0.7, 0.9, 0.2]
consine_similarity_results.argsort() =><font color="green"> [3, 0, 1, 2]</font> <br>
<font color="green">De esta forma podemos encontrar el índice del que tenga más similitud en el documents. </font>

![](/imagenes/queryreply.png)

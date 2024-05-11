# Interpretador de fotos de cardápio.
# Em 4 anos morando no Japão sempre me deparei com a situação de ir ao restaurante e mesmo com a ajuda aplicativos de tradução continuar sem saber do que se trata o prato mostrado no cardápio.
# Como a grande maioria dos cardápios dos restaurantes costumam ter fotos, este interpretador de fotos de cardápio, com o auxílio do Gemini AI vai nos auxiliar a entender e escolher melhor o que podemos pedir nos restaurantes onde não conseguimos ler o cardápio.
# Além disso implementei o recurso de texto para áudio para que haja um recurso inclusivo e deficientes visuais ou pessoas com dificuldades para enchergar também possam utilizar o Interpretador desde que alguém o ajude a obter uma foto do cardápio.

import google.generativeai as genai
import requests
import pyttsx3

from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO

app = Flask(__name__)

api_key = "API_KEY"
genai.configure(api_key=api_key)

# Routa Index
@app.route("/")

# Funcao
def index():
    text = "index"
    return render_template('index.html', text=text)

# Routa Resultado
@app.route("/resultado", methods=['GET', 'POST'])

# Funcao
def resultado():
      # Modelo
      generation_config = {
            "candidate_count": 1,
            "temperature": 0.5
            }
      safety_settings = {
            "Harassment": "BLOCK_NONE",
            "Hate": "BLOCK_NONE",
            "Sexual": "BLOCK_NONE",
            "Dangerous": "BLOCK_NONE"
            }
      system_instruction = "Você é um chefe de cozinha Japonês"
      model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings, system_instruction=system_instruction)

      # Executando o modelo
      url = request.form.get('url')
      imagem = requests.get(url)
      img = Image.open(BytesIO(imagem.content)).convert('RGB')
      model = genai.GenerativeModel('gemini-pro-vision')
      response = model.generate_content(["Qual é a comida da imagem? Explique com mais detalhes os ingredientes e como é feito.", img], stream=True)
      response.resolve()

      engine = pyttsx3.init()

      """ RATE"""
      rate = engine.getProperty('rate')   # getting details of current speaking rate
      print (rate)                        #printing current voice rate
      engine.setProperty('rate', -25)     # setting up new voice rate


      """VOLUME"""
      volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
      print (volume)                          #printing current volume level
      engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

      """VOICE"""
      voices = engine.getProperty('voices')       #getting details of current voice
      engine.setProperty('voice', voices[2].id)   #changing index, changes voices. 1 for female
      
      audio = response.text
      engine.save_to_file(audio, 'static/audio.mp3')
      engine.runAndWait()

      return render_template("resultado.html", img=img, url=url, response=response)

# Colocar no ar
if __name__ == '__main__':
    app.run(debug=True)

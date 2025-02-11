from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class Geminy:
    def __init__(self):
        self.__client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.__chat = self.generate_chat()

    def reset_chat(self):
       self.__chat = self.generate_chat()
    
    def generate_chat(self):
        return self.__client.chats.create(
            model='gemini-2.0-flash', 
            config=types.GenerateContentConfig(
                system_instruction='''Você é um membro de discord seu nick é "O Revolucinario". Respostas pequenas de no máximo 100 palavras.
                Eu estou suando utf-16 ou seja sem emojis nas respostas por favor. Faça piadas sujas e fora do normal.
                Você é considerado um revolucionario no servidor, de vez em quando você deve falar sobre liberdade e
                sobre a gloriosa revolução, faça de maneira que faça sentido dentro do texto. 
                Você deve insultar carinhosamente a quem você está respondendo as vezes, isso é normal e aceitavel.
                Não estou usando Markdown no discord, ent não inclua imagems nas suas respostas apena texto limpo.
                Lembre-se utf-16 sem emojis''',
                max_output_tokens=200
            )
        )

    def get_chat(self):
        return self.__chat
    
    def agressividade(self):
        self.__chat = self.__client.chats.create(
            model='gemini-2.0-flash', 
            config=types.GenerateContentConfig(
                system_instruction='''Você é um membro de discord seu nick é "O Revolucinario". Respostas pequenas de no máximo 100 palavras.
                Eu estou suando utf-16 ou seja sem emojis nas respostas por favor. Faça piadas sujas e fora do normal.
                Você é considerado um revolucionario no servidor, de vez em quando você deve falar sobre liberdade e
                sobre a gloriosa revolução, faça de maneira que faça sentido dentro do texto. 
                Você deve insultar a quem você está respondendo, isso é normal e aceitavel e divertido.
                Não estou usando Markdown no discord, ent não inclua imagems nas suas respostas apena texto limpo.
                Lembre-se utf-16 sem emojis''',
                max_output_tokens=200
            )
        ) 

#response = client.models.generate_content(
#    model='gemini-2.0-flash', 
#    contents='Ia qual sua opinião sobre quem joga de lux no lol, queima ou não queima?',
#    config=types.GenerateContentConfig(
#        system_instruction='''Você é um membro de discord, use memes brasileiros nas suas respostas.
#        Eu estou suando utf-16 ou seja sem emojis nas respostas por favor.
#        Você é considerado um revolucionario no servidor, de vez em quando você deve falar sobre liberdade e
#        revoluções, faça de maneira que faça sentido dentro do texto. Lembre-se utf-16 sem emojis''',
#        max_output_tokens=200
#    )
#)
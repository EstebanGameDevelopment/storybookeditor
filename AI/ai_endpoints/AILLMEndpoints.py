from ai_endpoints.AlchemySQLFunctions import AlchemyDBFunctions

from gradio_client import Client
from enum import Enum
from pydantic import BaseModel, Field
from typing import List
import hashlib
import requests
import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from langchain_community.llms import Ollama
import os
import json
import re
import torch
import brotli
import time
from TTS.api import TTS
from pydub import AudioSegment
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.chains import ConversationChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.utils.json import parse_json_markdown
from langchain_openai import ChatOpenAI
from openai import OpenAI
from vertexai.preview import tokenization
import tiktoken
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chat_models import ChatOpenAI # In case you want to pay to use OpenAI
from langchain.memory import ConversationBufferMemory 
from langchain_core.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from mistral_common.protocol.instruct.messages import (
    UserMessage,
)
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.tool_calls import (
    Function,
    Tool,
)
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer

class ProviderLLM(Enum):
    CHAT_GPT = 1
    ANTHROPIC = 2
    MISTRAL = 3
    GOOGLE = 4
    LOCAL = 5
        
class AILLMServer:
    def __init__(self, hostAddress, portNumber, enableOpenAI, enableAntrophic, enableMistral, enableGoogle, enableOther, enableUltraGPT, enableUltraMistral, enableUltraGoogle, databaseAlchemy, voicesLanguage, urlSpeechGeneration, urlImageGeneration, urlFluxImageGeneration, templateQuestion, promptChapters, parserChapters, promptCharacters, parserCharacters, promptLocations, parserLocations, promptStoryPlots, parserStoryPlots, promptScene, parserScene, promptSceneCharacters, parserSceneCharacters, promptPlaces, parserPlaces, promptParagraphForCharacter, parserParagraphForCharacter, promptBaseCharacters, parserBaseCharacters, promptBaseLocations, parserBaseLocations, promptBasePlots, parserBasePlots, promptBaseChapters, parserBaseChapters, promptFormatImage, parserFormatImage, promptFormatSoundFX, parserFormatSoundFX, promptFormatMusicLoop, parserFormatMusicLoop, promptFormatCharacterDialog, parserFormatCharacterDialog, promptFormatTranslateToken, parserFormatTranslateToken, templateTranslation):
        self.host_address = hostAddress
        self.port_number = portNumber
        self.app = Flask(__name__)        
        self.app.config['SQLALCHEMY_DATABASE_URI'] = databaseAlchemy
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['wav_voices'] = voicesLanguage
        self.db = SQLAlchemy(self.app)
        self.is_db_inited = False

        self.template_question = templateQuestion
        self.provider_llm = -1

        # ++++ REQUIRE USER ++++ 
        # -If "True" you will need an stored user+password in the database in order to access the service
        # -Endpoint to create user: "/ai/users/create"
        self.enable_user_check = False 
        self.url_speech_generation = urlSpeechGeneration
        self.url_image_generation = urlImageGeneration        
        self.url_flux_image_generation = urlFluxImageGeneration        
        self.cost_per_token_input = 0
        self.cost_per_token_output = 0

        self.cached_llm = None
        self.clientOpenAI = None
        os.environ["OPENAI_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # STABILITY CONFIGURATION
        self.stability_config = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.stability_base_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        self.stability_base_model = 'sd3-large-turbo'

        # SCENEARIO CONFIGURATION
        self.scenario_config = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.scenario_model_landscape = 'NKStdSjYQjaeFiTK9ps8dg'  # It's one of our signature public models
        self.scenario_model_character = 'model_8FC4CAGPzXphAsbkA8rc4GRG' # The "Olivia" model generates images that showcase a character in various thematic settings
        self.scenario_base_url = "https://api.cloud.scenario.com/v1"
        
        # ++++ OPENAI CHATGPT OMNI ++++
        if enableUltraGPT:
            self.provider_llm = ProviderLLM.CHAT_GPT            
            # ++++ ChatGPT 4-Omni ++++ 
            self.cached_llm = ChatOpenAI(model_name="gpt-4o")
            self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
            self.cost_per_token_input = 0.000005 # GPT4-O (input)
            self.cost_per_token_output = 0.000015 # GPT4-O (output)
            print (" +++LLM++++ Running OpenAI gpt-4o LLM (WARNING: ULTRA EXPENSIVE!!!!!)")

        # ++++ OPENAI CHATGPT OMNI-MINI ++++
        if enableOpenAI:
            self.provider_llm = ProviderLLM.CHAT_GPT            
            # ++++ ChatGPT 4-Turbo ++++ 
            self.cached_llm = ChatOpenAI(model_name="gpt-4o-mini")
            self.tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
            self.cost_per_token_input = 0.00000015 # GPT4-O-mini (input)
            self.cost_per_token_output = 0.0000006 # GPT4-O-mini (output)
            # self.cost_per_token_input = 0.000005 # GPT4-O (input)
            # self.cost_per_token_output = 0.000015 # GPT4-O (output)
            print (" +++LLM++++ Running OpenAI gpt-4o-mini LLM")

        # ++++ ANTHROPIC (NOT WORKING BECAUSE ANTHROPIC DOESN'T SUPPORT LANGCHAIN'S JSON PARSER FORMAT) ++++
        if enableAntrophic:
            self.provider_llm = ProviderLLM.ANTHROPIC
            os.environ["ANTHROPIC_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            # self.cached_llm = ChatAnthropic(model='claude-3-haiku-20240307')
            # self.cached_llm = ChatAnthropic(model='claude-3-sonnet-20240229')            
            # self.cached_llm = ChatAnthropic(model='claude-3-opus-20240229')
            self.cached_llm = ChatAnthropic(model='claude-3-5-sonnet-20240620')
            print (" +++LLM++++ Running Anthropic claude-3-5-sonnet LLM")
            # print (" +++LLM++++ Running Anthropic claude-3-opus LLM")
            # print (" +++LLM++++ Running Anthropic claude-3-sonnet LLM")
            # print (" +++LLM++++ Running Anthropic claude-3-haiku LLM")
        
        # ++++ MISTRAL-LARGE ++++
        if enableUltraMistral:
            self.provider_llm = ProviderLLM.MISTRAL
            os.environ["MISTRAL_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            self.cached_llm = ChatMistralAI(model="mistral-large-latest")
            self.tokenizer = MistralTokenizer.from_model("mistral-large-latest")
            self.cost_per_token_input = 0.000003  # mistral-large-latest (input)
            self.cost_per_token_output = 0.000009 # mistral-large-latest (output)
            print (" +++LLM++++ Running Mistral mistral-large-latest LLM")            
        
        # ++++ MISTRAL-NEMO ++++
        if enableMistral:
            self.provider_llm = ProviderLLM.MISTRAL
            os.environ["MISTRAL_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            self.cached_llm = ChatMistralAI(model="open-mistral-nemo-2407")
            self.tokenizer = MistralTokenizer.from_model("mistral-large-latest")
            self.cost_per_token_input = 0.0000003  # mistral-nemo (input)
            self.cost_per_token_output = 0.0000003 # mistral-nemo (output)
            print (" +++LLM++++ Running Mistral mistral-nemo LLM")

        # ++++ GOOGLE GEMINI-FLASH ++++
        if enableUltraGoogle:
            self.provider_llm = ProviderLLM.GOOGLE
            os.environ["GOOGLE_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            self.cached_llm = ChatGoogleGenerativeAI(model="gemini-pro")
            self.tokenizer_google = tokenization.get_tokenizer_for_model("gemini-1.0-pro-002")
            self.cost_per_token_input = 0.000003  # gemini-pro (input)
            self.cost_per_token_output = 0.000007 # gemini-pro (output)
            print (" +++LLM++++ Running Google gemini-pro LLM")

        # ++++ GOOGLE GEMINI-FLASH ++++
        if enableGoogle:
            self.provider_llm = ProviderLLM.GOOGLE
            os.environ["GOOGLE_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            self.cached_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
            self.tokenizer_google = tokenization.get_tokenizer_for_model("gemini-1.0-pro-002")
            self.cost_per_token_input = 0.00000035  # gemini-1.5-flash (input)
            self.cost_per_token_output = 0.0000007 # gemini-1.5-flash (output)
            print (" +++LLM++++ Running Google gemini-flash LLM")

        # ++++ GLOBAL CONFIGURATION (LOCAL LLM) ++++
        if enableOther:
            self.provider_llm = ProviderLLM.LOCAL
            self.cached_llm = Ollama(model="mistral-nemo:latest") # MODEL WITH A CONTEXT LENGTH OF 128Kb
            # self.cached_llm = Ollama(model="llama3.1")
            # self.cached_llm.num_ctx = 131072
            # self.cached_llm.num_ctx = 32768
            # self.cached_llm.num_ctx = 16384
            # self.cached_llm.num_gpu = 1
            print ("Running LOCAL OLLAMA mistral-nemo 128K LLM")
            # print ("Running LOCAL OLLAMA llama3.1 LLM")

        self.cached_llm.temperature = 0.7
                                  
        self.chainChapters = promptChapters | self.cached_llm | parserChapters
        self.chainCharacters = promptCharacters | self.cached_llm | parserCharacters
        self.chainLocations = promptLocations | self.cached_llm | parserLocations
        self.chainStoryPlots = promptStoryPlots | self.cached_llm | parserStoryPlots
        self.chainScene = promptScene | self.cached_llm | parserScene
        self.chainSceneCharacters = promptSceneCharacters | self.cached_llm | parserSceneCharacters
        self.chainPlaces = promptPlaces | self.cached_llm | parserPlaces
        self.chainParagraphForCharacter = promptParagraphForCharacter | self.cached_llm | parserParagraphForCharacter
        self.chainBaseCharacter = promptBaseCharacters | self.cached_llm | parserBaseCharacters
        self.chainBaseLocations = promptBaseLocations | self.cached_llm | parserBaseLocations
        self.chainBasePlots = promptBasePlots | self.cached_llm | parserBasePlots
        self.chainBaseChapters = promptBaseChapters | self.cached_llm | parserBaseChapters

        self.chainFormatImage = promptFormatImage | self.cached_llm | parserFormatImage
        self.chainFormatSoundFX = promptFormatSoundFX | self.cached_llm | parserFormatSoundFX
        self.chainFormatMusicLoop = promptFormatMusicLoop | self.cached_llm | parserFormatMusicLoop
        self.chainFormatCharacterDialog = promptFormatCharacterDialog | self.cached_llm | parserFormatCharacterDialog
        
        self.templateTranslation = templateTranslation
        self.chainFormatTranslateToken = promptFormatTranslateToken | self.cached_llm | parserFormatTranslateToken

        self.app.add_url_rule('/store', 'store_value', self.store_value, methods=['POST'])
        self.app.add_url_rule('/init_db', 'init_db', self.init_db, methods=['GET'])
        self.app.add_url_rule('/retrieve', 'retrieve_values', self.retrieve_values, methods=['GET'])
        self.app.add_url_rule('/get_value', 'get_value', self.get_value, methods=['GET'])
        self.app.add_url_rule('/delete', 'delete_value', self.delete_value, methods=['DELETE'])
        self.app.add_url_rule('/clear', 'clear_values', self.clear_values, methods=['DELETE'])
        self.app.add_url_rule('/update', 'update_value', self.update_value, methods=['PUT'])

        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/ai/question', 'question', self.question, methods=['POST'])
        self.app.add_url_rule('/ai/question/history', 'question_history', self.question_history, methods=['POST'])
        self.app.add_url_rule('/ai/question/chapters', 'question_chapters', self.question_chapters, methods=['POST'])
        self.app.add_url_rule('/ai/question/characters', 'question_characters', self.question_characters, methods=['POST'])
        self.app.add_url_rule('/ai/question/locations', 'question_locations', self.question_locations, methods=['POST'])
        self.app.add_url_rule('/ai/question/plots', 'question_plots', self.question_plots, methods=['POST'])
        self.app.add_url_rule('/ai/question/scenes', 'question_scenes', self.question_scenes, methods=['POST'])
        self.app.add_url_rule('/ai/question/scene_characters', 'question_scene_characters', self.question_scene_characters, methods=['POST'])
        self.app.add_url_rule('/ai/question/scene_locations', 'question_scene_locations', self.question_scene_locations, methods=['POST'])
        self.app.add_url_rule('/ai/question/paragraph_character', 'question_paragraph_for_character', self.question_paragraph_for_character, methods=['POST'])
        self.app.add_url_rule('/ai/question/last_cost', 'get_user_operation_cost', self.get_user_operation_cost, methods=['POST'])
        self.app.add_url_rule('/ai/translation_text', 'translation_text', self.translation_text, methods=['POST'])        

        self.app.add_url_rule('/ai/question/delete_last', 'delete_last', self.delete_last, methods=['POST'])
        
        self.app.add_url_rule('/ai/creation/character', 'creation_character', self.creation_character, methods=['POST'])
        self.app.add_url_rule('/ai/creation/locations', 'creation_locations', self.creation_locations, methods=['POST'])
        self.app.add_url_rule('/ai/creation/plots', 'creation_plots', self.creation_plots, methods=['POST'])
        self.app.add_url_rule('/ai/creation/chapters', 'creation_chapters', self.creation_chapters, methods=['POST'])
        
        self.app.add_url_rule('/ai/users/login', 'login_user', self.login_user, methods=['GET'])
        self.app.add_url_rule('/ai/users/create', 'create_user', self.create_user, methods=['GET'])
        self.app.add_url_rule('/ai/conversations/new', 'new_conversation', self.new_conversation, methods=['GET'])
        self.app.add_url_rule('/ai/conversations/get', 'get_conversation', self.get_conversation, methods=['GET'])
        self.app.add_url_rule('/ai/conversations/delete', 'delete_conversation', self.delete_conversation, methods=['GET'])
        self.app.add_url_rule('/ai/conversations/delete_all', 'delete_all_conversations', self.delete_all_conversations, methods=['GET'])

        self.app.add_url_rule('/ai/image', 'image_generation', self.image_generation, methods=['POST'])
        self.app.add_url_rule('/ai/image/derivation', 'image_derivation', self.image_derivation, methods=['POST'])
        self.app.add_url_rule('/ai/speech', 'speech_generation', self.speech_generation, methods=['POST'])
        self.app.add_url_rule('/ai/speech/voice', 'upload_speech_voice', self.upload_speech_voice, methods=['POST'])
        self.app.add_url_rule('/ai/audio', 'audio_generation', self.audio_generation, methods=['POST'])
        self.app.add_url_rule('/ai/music', 'music_generation', self.music_generation, methods=['POST'])

        self.app.add_url_rule('/ai/format/image', 'format_image_generation', self.format_image_generation, methods=['POST'])
        self.app.add_url_rule('/ai/format/soundfx', 'format_soundfx_generation', self.format_soundfx_generation, methods=['POST'])
        self.app.add_url_rule('/ai/format/musicloop', 'format_musicloop_generation', self.format_musicloop_generation, methods=['POST'])
        self.app.add_url_rule('/ai/format/character', 'format_characterstate_generation', self.format_characterstate_generation, methods=['POST'])

        self.app.add_url_rule('/ai/stop', 'stop', self.stop, methods=['GET'])
        self.app.add_url_rule('/ai/status', 'status', self.status, methods=['GET'])
        
    def init_sql_functions(self, userapp):
        if self.is_db_inited is False:
            self.is_db_inited = True            
            self.sqlFunctions = AlchemyDBFunctions(self.db, userapp)
            with self.app.app_context():
                self.db.create_all()
            print ("+++++++++++++++++++++++++++++AlchemyDBFunctions HAS BEEN INITIALIZED")

    def is_free_llm(self):
        if self.cost_per_token_input > 0 and self.cost_per_token_output > 0:
            return False
        else:
            return True

    def count_tokens(self, text):
        if self.provider_llm == ProviderLLM.MISTRAL:
            tokens = self.tokenizer.instruct_tokenizer.tokenizer.encode(text, True, True)
        elif self.provider_llm == ProviderLLM.GOOGLE:
            return self.tokenizer_google.count_tokens(text).total_tokens
        else:
            tokens = self.tokenizer.encode(text)
        return len(tokens)
    
    def calculate_array_cost(self, input_texts, output_texts):
        if self.is_free_llm():
            return 0
        else:
            input_tokens = sum(self.count_tokens(text) for text in input_texts)
            output_tokens = sum(self.count_tokens(text) for text in output_texts)
        
            total_cost = (input_tokens * self.cost_per_token_input) + (output_tokens * self.cost_per_token_output)
            return total_cost
    
    def calculate_cost(self, input_text, output_text):
        if self.is_free_llm():
            return 0
        else:
            if len(input_text) > 0:
                input_tokens = self.count_tokens(input_text)
            else:
                input_tokens = 0
            output_tokens = self.count_tokens(output_text)

            total_cost = (input_tokens * self.cost_per_token_input) + (output_tokens * self.cost_per_token_output)
            return total_cost    

    def store_last_operation_cost(self, name_cost, cost_value):
        if not self.sqlFunctions.exist_value(name_cost):
            self.sqlFunctions.store_new_value(name_cost, str(cost_value * 1000))
        else:
            self.sqlFunctions.update_value(name_cost, str(cost_value * 1000))

    def get_last_operation_cost(self, name_cost):
        if not self.sqlFunctions.exist_value(name_cost):
            return 0
        else:
            cost_string = self.sqlFunctions.get_value_by_name(name_cost)
            return float(cost_string.value)

    def get_sceneario_image_url(self, base_url, model_id, inference_id, headers):
        status = ''
        while status not in ['succeeded', 'failed']:
            # Fetch the inference details
            inference_response = requests.get(f'{base_url}/models/{model_id}/inferences/{inference_id}', headers=headers)
            inference_data = inference_response.json()
            # print(inference_data)
            status = inference_data['inference']['status']
            print(f'Inference status: {status}')

            # Wait for a certain interval before polling again
            time.sleep(5)  # Polling every 5 seconds

        # Handle the final status
        if status == 'succeeded':
            print('Inference succeeded!')
            return inference_data['inference']['images'][0]['id'], inference_data['inference']['images'][0]['url']
        else:
            print('Inference failed!')
            print(inference_data)  # Print inference data
            return None, None
            
    def remove_background_image(self, base_url, headers, asset_id):
        url_background = base_url + "/images/erase-background"   
        payload_background = {
            "backgroundColor": "transparent",
            "assetId": asset_id,
            "format": "png"
        }
        response = requests.put(url_background, json=payload_background, headers=headers)
        if response.status_code == 200:
            print('Remove Background succeeded!')
            response_data = response.json()
            print(response_data['asset']['url'])
            return response_data['asset']['url']
        else:
            print('Remove Background failed!')
            print(response)
            return None
        
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # BASE ENDPOINTS
    # -------------------------------------------------------------
    # -------------------------------------------------------------

    def init_db(self):
        username = request.args.get('name')
        self.init_sql_functions(username)
        return jsonify({"message": "DB inited successfully"}), 201

    def store_value(self):
        name = request.json.get('name')
        value = request.json.get('value')
        if not name or not value:
            return jsonify({"error": "Invalid input"}), 400
        
        self.sqlFunctions.store_new_value(name, value)
        return jsonify({"message": "Value stored successfully"}), 201

    def retrieve_values(self):
        result = self.sqlFunctions.get_all_values()
        return jsonify(result), 200

    def get_value(self):
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Name parameter is required"}), 400
        
        entry = self.sqlFunctions.get_value_by_name(name)
        if entry:
            return jsonify({"name": entry.name, "value": entry.value}), 200
        else:
            return jsonify({"error": "Name not found"}), 404

    def delete_value(self):
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Name parameter is required"}), 400

        entry = self.sqlFunctions.get_value_by_name(name)
        if entry:
            self.sqlFunctions.delete_value_by_name(name)
            return jsonify({"message": f"Entry with name '{name}' deleted successfully"}), 200
        else:
            return jsonify({"error": "Name not found"}), 404

    def clear_values(self):
        try:
            num_rows_deleted = self.sqlFunctions.delete_all_values()
            return jsonify({"message": f"All entries deleted successfully, {num_rows_deleted} rows affected"}), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"error": str(e)}), 500

    def update_value(self):
        data = request.json
        name = data.get('name')
        new_value = data.get('value')

        if not name or not new_value:
            return jsonify({"error": "Name and new value are required"}), 400

        entry = self.sqlFunctions.get_value_by_name(name)
        if entry:
            self.sqlFunctions.update_value(name, new_value)
            return jsonify({"message": f"Value for name '{name}' updated successfully"}), 200
        else:
            return jsonify({"error": "Name not found"}), 404        

    def extract_json_from_string(self, input_string):
        # Updated regex to handle both objects and arrays
        json_pattern = r'(\{[\s\S]*\}|\[[\s\S]*\])'
        
        match = re.search(json_pattern, input_string)
        
        if match:
            json_string = match.group(0)
            try:
                json_data = json.loads(json_string)
                return json_data
            except json.JSONDecodeError:
                print("Extracted string is not valid JSON.")
                return None
        else:
            print("No JSON data found in the input string.")
            return None
            
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # AI ENDPOINTS
    # -------------------------------------------------------------
    # -------------------------------------------------------------

    def index(self):
           # self.cached_llm.set_user_id("abc123")
           return self.cached_llm.model + ":CONTEXT[" +  str(self.cached_llm.num_ctx) + "]" # ":GPU["+str(self.cached_llm.num_gpu)  +"]:TEMPERATURE["+ str(self.cached_llm.temperature)+"]"
           # return self.cached_llm.model_name + ":CONTEXT[" +  str(self.cached_llm.num_ctx) + "]" # ":GPU["+str(self.cached_llm.num_gpu)  +"]:TEMPERATURE["+ str(self.cached_llm.temperature)+"]"
           
    # ++ endpoint POST "/ai/question" ++
    # Raw body:
    # {
    #    "userid": 10,
    #    "username": "username",
    #    "password": "passwrod",
    #    "conversationid": "1",
    #    "question": "What can you tell me about the city of London?",
    #    "chain": true,
    #    "debug": true
    # }       
    def question(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]
            chain = bool(prompt["chain"])

            if args.get("debug", default=False, type=bool):
                print("AI question received...")
                print("AI question is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            historyJSON = None
            memory = None
            response = None
            cost = 0
            if chain:
                if not self.sqlFunctions.exist_value(conversationName):
                    self.sqlFunctions.store_new_value(conversationName, "")
            
                historyJSON = self.sqlFunctions.get_history_by_name(conversationName)
                memory = ConversationBufferMemory(return_messages=True)            
            
                if len(historyJSON) > 1:
                    messages = self.sqlFunctions.get_list_messages(historyJSON)
                    for user_msg, ai_msg in messages:
                        memory.chat_memory.add_user_message(user_msg)
                        memory.chat_memory.add_ai_message(ai_msg)
                    
                PROMPT = PromptTemplate(input_variables=["history", "input"], template=self.template_question)
                conversation = ConversationChain(prompt=PROMPT, llm=self.cached_llm, verbose=True, memory=memory)
                jsonResponse = conversation.invoke(question)
                response = self.sqlFunctions.get_ai_message_content(jsonResponse)
                
                input_texts = [msg.content for msg in conversation.memory.buffer if msg.type == "human"]
                output_texts = [msg.content for msg in conversation.memory.buffer if msg.type == "ai"]
                self.store_last_operation_cost(username + "_cost", 0)
                
                historyUpdated = self.sqlFunctions.add_new_message(historyJSON, question, response)
            
                self.sqlFunctions.update_value(conversationName, historyUpdated)
            else:
                response = self.cached_llm.invoke(question)
                if isinstance(response, AIMessage):
                    response = response.content
                    self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))

            print (response)

            if args.get("debug", default=False, type=bool):
                    print("AI response received...")

            return response

    def question_history(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]

            if args.get("debug", default=False, type=bool):
                print("AI history get received...")

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            output = ""
            if not self.sqlFunctions.exist_value(conversationName):
                return output
            else:
                historyJSON = self.sqlFunctions.get_history_by_name(conversationName)
            
                if len(historyJSON) > 1:
                    json_messages = []
                    messages = self.sqlFunctions.get_list_messages(historyJSON)
                    for user_msg, ai_msg in messages:
                        json_object_user = { "mode": 1, "text": user_msg }
                        json_messages.append(json_object_user)
                        json_object_ai = { "mode": 0, "text": ai_msg }
                        json_messages.append(json_object_ai)

                    output = json.dumps(json_messages, indent=4)  
        
                print (output)
                
                if args.get("debug", default=False, type=bool):
                        print("AI history response produced...")
                        
                return output

    def question_delete_history(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]

            if args.get("debug", default=False, type=bool):
                print("AI history delete received...")

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"

            if not self.sqlFunctions.exist_value(conversationName):
                return "Error"
            else:
                self.sqlFunctions.delete_value_by_name(conversationName)
                
                if args.get("debug", default=False, type=bool):
                        print("AI history response produced...")
                        
                return "true"
    
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # DELETE LAST PUSHED ITEM
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    def delete_last(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]

            if args.get("debug", default=False, type=bool):
                print("AI delete last question received...")

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            if self.sqlFunctions.delete_last_committed_value(conversationName):
                return "true"
            else:
                return "false"
    
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # TRANSLATION
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    def translation_text(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            instructions = prompt["instructions"]
            question = prompt["question"]
            chain = bool(prompt["chain"])
            isjson = bool(prompt["isjson"])

            if args.get("debug", default=False, type=bool):
                print("AI translation received...")
                print("AI translation instructions are {}".format(instructions))
                print("AI translation original text is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            if chain:
                if not self.sqlFunctions.exist_value(conversationName):
                    self.sqlFunctions.store_new_value(conversationName, "")
            
                historyJSON = self.sqlFunctions.get_history_by_name(conversationName)
                memory = ConversationBufferMemory(return_messages=True)            
            
                if len(historyJSON) > 1:
                    messages = self.sqlFunctions.get_list_messages(historyJSON)
                    for user_msg, ai_msg in messages:
                        memory.chat_memory.add_user_message(user_msg)
                        memory.chat_memory.add_ai_message(ai_msg)
                
                promptTranslationChain = PromptTemplate(template=self.templateTranslation, input_variables=["history", "input"])
                conversation = ConversationChain(prompt=promptTranslationChain, llm=self.cached_llm, verbose=True, memory=memory)
                jsonResponse = None
                if len(instructions) > 0:
                    jsonResponse = conversation.invoke(instructions + " " + question)
                else:
                    jsonResponse = conversation.invoke(question)                
                response = self.sqlFunctions.get_ai_message_content(jsonResponse)
                
                input_texts = [msg.content for msg in conversation.memory.buffer if msg.type == "human"]
                output_texts = [msg.content for msg in conversation.memory.buffer if msg.type == "ai"]
                cost = self.calculate_array_cost(input_texts, output_texts)
                
                historyUpdated = self.sqlFunctions.add_new_message(historyJSON, question, response)
            
                self.sqlFunctions.update_value(conversationName, historyUpdated)
            else:
                if isjson == True:
                    response = self.chainFormatTranslateToken.invoke({"query": question})
                    self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
                else:
                    response = None
                    if len(instructions) > 0:
                        response = self.cached_llm.invoke(instructions + " " + question)
                    else:
                        response = self.cached_llm.invoke(question)
                    if isinstance(response, AIMessage):
                        response = response.content
                        self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
                    # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI translation response received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # STORY
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++

    def question_chapters(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI chapters analysis received...")
                print("AI chapters analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            
            
            try:
                response = self.chainChapters.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)
                    
            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI chapters response received...")
                    print(response)
                    
            return response

    def question_characters(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI characters analysis received...")
                print("AI characters analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainCharacters.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI characters response received...")
                    print(response)

            return response

    def question_locations(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI locations analysis received...")
                print("AI locations analysis is {}".format(question))

            self.init_sql_functions(username)
            
            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainLocations.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI locations response received...")
                    print(response)

            return response

    def question_plots(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI plots analysis received...")
                print("AI plots analysis is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainStoryPlots.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI plots response received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # SCENES
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    
    def question_scenes(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI scenes analysis received...")
                print("AI scenes analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainScene.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI scenes response received...")
                    print(response)

            return response

    def question_scene_characters(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI characters for scene analysis received...")
                print("AI characters for scene analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainSceneCharacters.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI characters for scene response received...")
                    print(response)

            return response

    def question_scene_locations(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI scene places analysis received...")
                print("AI scene places analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainPlaces.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI scene places response received...")
                    print(response)

            return response

    def question_paragraph_for_character(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI paragraph for character analysis received...")
                print("AI paragraph for character analysis is {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainParagraphForCharacter.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI paragraph for character response received...")
                    print(response)

            return response          

    def get_user_operation_cost(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]

            if args.get("debug", default=False, type=bool):
                print("AI get last operation cost received...")

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            
            
            cost_operation = self.get_last_operation_cost(username + "_cost")

            if args.get("debug", default=False, type=bool):
                    print("AI get operation cost = " + str(cost_operation))

            return jsonify({"cost": cost_operation, "response": str(cost_operation)})

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # BASE CREATION
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++

    def creation_character(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI base characters creation received...")
                print("AI base characters creation {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainBaseCharacter.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI base characters response received...")
                    print(response)

            return response

    def creation_locations(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            if args.get("debug", default=False, type=bool):
                print("AI base locations creation received...")
                print("AI base locations creation {}".format(question))

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainBaseLocations.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI base locations response received...")
                    print(response)

            return response

    def creation_plots(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI base plots creation received...")
                print("AI base plots creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainBasePlots.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI base plots creation received...")
                    print(response)

            return response

    def creation_chapters(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI base chapters creation received...")
                print("AI base chapters creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainBaseChapters.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI base chapters creation received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # FORMAT VISUAL
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++    
    def format_image_generation(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI format visual image creation received...")
                print("AI format visual image creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainFormatImage.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI format visual image creation received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # FORMAT SOUND FX
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++    
    def format_soundfx_generation(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI format SOUND FX creation received...")
                print("AI format SOUND FX creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainFormatSoundFX.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI format SOUND FX creation received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # FORMAT MUSIC LOOP
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++    
    def format_musicloop_generation(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI format MUSIC LOOP creation received...")
                print("AI format MUSIC LOOP creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainFormatMusicLoop.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI format MUSIC LOOP creation received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # FORMAT CHARACTER STATE
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++    
    def format_characterstate_generation(self):
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            conversationName = prompt["conversationid"]
            question = prompt["question"]

            self.init_sql_functions(username)

            if args.get("debug", default=False, type=bool):
                print("AI format CHARACTER DIALOG STATE creation received...")
                print("AI format CHARACTER DIALOG STATE creation is {}".format(question))

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            try:
                response = self.chainFormatCharacterDialog.invoke({"query": question})
            except OutputParserException as e:
                if self.provider_llm == ProviderLLM.ANTHROPIC:
                    response = self.extract_json_from_string(e.llm_output)

            self.store_last_operation_cost(username + "_cost", self.calculate_cost(question, str(response)))
            # print(response)

            if args.get("debug", default=False, type=bool):
                    print("AI format CHARACTER DIALOG STATE creation received...")
                    print(response)

            return response

    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
    # OTHERS
    # ++++++++++++++++++++++
    # ++++++++++++++++++++++
           
    def login_user(self):
            args = request.args
            username = args.get("user", default="", type=str)
            password = args.get("password", default="", type=str)

            if args.get("debug", default=False, type=bool):
                    print("Login requested. User("+username+"), Psw("+password+")")

            self.init_sql_functions(username)

            id_user = self.sqlFunctions.validate_password(username, password)
            
            if id_user != -1:
                    return jsonify({"success": True, "user_id": id_user})
            else:
                    return jsonify({"success": False, "user_id": -1})        

    def create_user(self):
            args = request.args
            username = args.get("user", default="", type=str)
            password = args.get("password", default="", type=str)

            if args.get("debug", default=False, type=bool):
                    print("Create user requested. User("+username+"), Psw("+password+")")

            self.init_sql_functions(username)

            id_user = self.sqlFunctions.validate_password(username, password)
            
            if id_user == -1:
                self.sqlFunctions.store_new_value(username, password)
            
            return jsonify({"success": True})
           
    def new_conversation(self):
            args = request.args        
            userID = args.get("userid", default="", type=int)
            username = args.get("username", default="", type=str)
            password = args.get("password", default="", type=str)
            nameScript = args.get("namescript", default="None", type=str)

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                print ("Error: No matching user and password")
                return jsonify({"success": False})

            if not self.sqlFunctions.exist_value(nameScript):
                self.sqlFunctions.store_new_value(nameScript, "")

            print("New conversation with name("+nameScript+")")

            return jsonify({"success": True, "conversation_id": nameScript})

    def get_conversation(self):
            args = request.args        
            userID = args.get("userid", default="", type=int)
            username = args.get("username", default="", type=str)
            password = args.get("password", default="", type=str)
            conversationID = args.get("conversationid", default="", type=str)

            self.init_sql_functions(username)
            
            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                print ("Error: No matching user and password")
                return jsonify({"success": False})
            
            historyJSON = self.sqlFunctions.get_history_by_name(conversationID)
            
            return historyJSON

    def delete_conversation(self):
            args = request.args        
            userID = args.get("userid", default="", type=int)
            username = args.get("username", default="", type=str)
            password = args.get("password", default="", type=str)
            conversationID = args.get("conversationid", default="", type=str)

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                print ("Error: No matching user and password")
                return jsonify({"success": False})
            
            self.sqlFunctions.delete_value_by_name(conversationID)
            
            print("Conversation deleted with name("+conversationID+")")

            return jsonify({"success": True})        
    
    def delete_all_conversations(self):
            args = request.args        
            userID = args.get("userid", default="", type=int)
            username = args.get("username", default="", type=str)
            password = args.get("password", default="", type=str)
            conversationIDs = args.get("conversationids", default="", type=str)

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                print ("Error: No matching user and password")
                return jsonify({"success": False})

            if args.get("debug", default=False, type=bool):
                    print("+++++++++++++userName["+username+"] Conversations to delete("+conversationIDs+")")

            ids = conversationIDs.split(',')

            for convID in ids:
                    if len(convID) > 0:
                        if args.get("debug", default=False, type=bool):
                            print("Deleting conversation with conversation ID("+convID+")")

                        self.sqlFunctions.delete_value_by_name(convID)
                        
            return jsonify({"success": True})

    # ++ endpoint POST "/ai/speech" ++
    # Raw body:
    # {
    #    "userid": -1,
    #    "username": "username",
    #    "password": "password",
    #    "voice": "HalleB1.wav",
    #    "speech": "Hello world! How are you today?",
    #    "language": "en",
    #    "emotion": "",
    #    "speed": 1
    # }
    def speech_generation(self) -> bytes:
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])            
            username = prompt["username"]
            password = prompt["password"]
            project = prompt["project"]
            voice = prompt["voice"]
            speech = prompt["speech"]
            language = prompt["language"]
            emotion = prompt["emotion"]
            speed = prompt["speed"]

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            print ("speech_generation="+speech)

            if self.clientOpenAI is not None:
                temp_mp3_file = "output.mp3"
                responseOpenAI = self.clientOpenAI.audio.speech.create(
                                                            model="tts-1",
                                                            voice="alloy",
                                                            input=speech
                                                            )
                responseOpenAI.stream_to_file(temp_mp3_file)
                dataaudio = AudioSegment.from_mp3(temp_mp3_file).export(format="ogg")
                os.remove(temp_mp3_file)
                return dataaudio
            else:
                # Define the URL and the payload to send.
                url = self.url_speech_generation

                payload = {
                    "project": project,
                    "username": username,
                    "voice": voice,
                    "speech": speech,
                    "language": language,
                    "emotion": emotion,
                    "speed": speed
                }

                # Send said payload to said URL through the API.
                response = requests.post(url=f'{url}/ai/speech', json=payload)
                return response.content
    
    def upload_speech_voice(self):
            userID = request.form.get("userid")
            username = request.form.get("username")
            password = request.form.get("password")
            project = request.form.get("project")
            voicename = request.form.get("voice")
            language = request.form.get("language")
            voicedata = request.files.get("file")            

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                print ("Error: No matching user and password")
                return jsonify({"success": False})

            # If the user does not select a file, the browser submits an empty file without a filename.
            if voicedata.filename == '':
                flash('No selected file')
                return jsonify({"success": False})
                
            if voicedata:
                url = self.url_speech_generation

                # Prepare the payload and files for the request
                payload = {
                    "project": project,
                    "voice": voicename,
                    "username": username,
                    "language": language
                }
                files = {
                    "file": (voicedata.filename, voicedata.read(), voicedata.mimetype)
                }

                # Send the payload and files to the endpoint
                response = requests.post(url=f'{url}/ai/speech/voice', data=payload, files=files)
                return jsonify({"success": True, "response": response.json()})
                
            return jsonify({"success": False})

    def audio_generation(self) -> bytes:
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            description = prompt["description"]
            duration = int(prompt["duration"])

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            # Define the URL and the payload to send.
            url = "http://0.0.0.0:7000"

            payload = {
                "description": description,
                "duration": duration
            }

            # Send said payload to said URL through the API.
            response = requests.post(url=f'{url}/ai/audio', json=payload)
            return response.content
    
    def music_generation(self) -> bytes:
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            description = prompt["description"]
            duration = int(prompt["duration"])

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            # Define the URL and the payload to send.
            url = "http://0.0.0.0:7000"

            payload = {
                "description": description,
                "duration": duration
            }

            # Send said payload to said URL through the API.
            response = requests.post(url=f'{url}/ai/music', json=payload)
            return response.content

    # ++ endpoint POST "/ai/image" ++
    # Raw body:
    # {
    #    "userid": -1,
    #    "username": "username",
    #    "password": "password",
    #    "description": "A dog enjoying a chicken bone",
    #    "exclude": "",
    #    "steps": 50,
    #    "width": 512,
    #    "height": 512
    # }
    def image_generation(self) -> bytes:
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            provider = prompt["provider"]
            description = prompt["description"]
            exclude = prompt["exclude"]
            steps = int(prompt["steps"])
            width = int(prompt["width"])
            height = int(prompt["height"])
            # data = request.files['file'].read()

            self.init_sql_functions(username)

            if self.enable_user_check and not self.sqlFunctions.login_user_id(userID, username, password):
                return "Error: No matching user and password"            

            if provider == 1:
                # Define the URL and the payload to send.
                url = self.url_image_generation

                payload = {
                    "prompt": description,
                    "negative_prompt": exclude,
                    "steps": steps,
                    "width": width,
                    "height": height
                }

                self.store_last_operation_cost(username + "_cost", 0)

                # Send said payload to said URL through the API.
                response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
                r = response.json()
                # f.write(base64.b64decode(r['images'][0]))
                return base64.b64decode(r['images'][0])
            elif provider == 2:
                clientImagesOpenAI = OpenAI()
                response = clientImagesOpenAI.images.generate(
                                                      model="dall-e-2",
                                                      prompt=description,
                                                      size=str(width) + "x" + str(height),
                                                      quality="standard",
                                                      n=1
                                                    )
                print (response.data[0].url)
                # DALL-E 2
                # 1024×1024 ($0.020 / image)
                # 512×512 ($0.018 / image)
                # 256×256 ($0.016 / image)
                if width == 256:
                    self.store_last_operation_cost(username + "_cost", 0.016)
                elif width == 512:
                    self.store_last_operation_cost(username + "_cost", 0.018)
                else:
                    self.store_last_operation_cost(username + "_cost", 0.02)
                return requests.get(response.data[0].url).content
            elif provider == 3:
                clientImagesOpenAI = OpenAI()
                response = clientImagesOpenAI.images.generate(
                                                      model="dall-e-3",
                                                      prompt=description,
                                                      size=str(width) + "x" + str(height),
                                                      quality="standard",
                                                      n=1
                                                    )
                print (response.data[0].url)
                # DALL-E 3
                # Standard (1024×1024) $0.040 / image
                # Standard (1024×1792, 1792×1024) $0.080 / image
                # HD (1024×1024) $0.080 / image
                # HD (1024×1792, 1792×1024) $0.120 / image
                if width == 1024 and height == 1024:
                    self.store_last_operation_cost(username + "_cost", 0.04)
                else:
                    self.store_last_operation_cost(username + "_cost", 0.08)
                return requests.get(response.data[0].url).content
            elif provider == 4:
                url_scenario = self.scenario_base_url + "/generate/txt2img"
                model_id = self.scenario_model_landscape
                authorize_scenario = base64.b64encode(self.scenario_config.encode('ascii')).decode('ascii')
                return self.generate_scenario_image(url_scenario, model_id, authorize_scenario, description, width, height, False)
            elif provider == 5:
                url_scenario = self.scenario_base_url + "/generate/txt2img"
                model_id = self.scenario_model_character
                authorize_scenario = base64.b64encode(self.scenario_config.encode('ascii')).decode('ascii')
                return self.generate_scenario_image(url_scenario, model_id, authorize_scenario, description, width, height, True)
            elif provider == 6:
                response = requests.post(
                    self.stability_base_url,
                    headers={
                        "authorization": self.stability_config,
                        "accept": "image/*"
                    },
                    files={"none": ''},
                    data={
                        "prompt": description,
                        "model": self.stability_base_model,     
                        "aspect_ratio": self.closest_aspect_ratio(width, height),
                        "output_format": "png",
                    },
                )

                if response.status_code == 200:
                    return response.content
                else:
                    return None                
            else:
                client = Client(self.url_flux_image_generation)
                result = client.predict(
                                width=width,
                                height=height,
                                num_steps=steps,
                                guidance=3.5,
                                seed="-1",
                                prompt=description,
                                init_image=None,
                                image2image_strength=0.8,
                                add_sampling_metadata=True,
                                api_name="/generate_image"
                )
                print(result)

                self.store_last_operation_cost(username + "_cost", 0)
            
                img_webp_path = result[0]
                img_data_path = result[2]

                if img_data_path:
                    with open(img_data_path, 'rb') as file:
                        file_bytes = file.read()

                    length_of_bytes = len(file_bytes)
                    print(f"Length of file bytes: {length_of_bytes}")
                    
                    os.remove(img_webp_path)
                    os.remove(img_data_path)
                    return file_bytes
                else:
                    return None

    def closest_aspect_ratio(self, width, height):
        # Calculate the aspect ratio
        aspect_ratio = width / height
        
        # Predefined aspect ratios and their string representations
        aspect_ratios = {
            "16:9": 16 / 9,
            "1:1": 1 / 1,
            "21:9": 21 / 9,
            "2:3": 2 / 3,
            "3:2": 3 / 2,
            "4:5": 4 / 5,
            "5:4": 5 / 4,
            "9:16": 9 / 16,
            "9:21": 9 / 21
        }
        
        # Find the closest aspect ratio
        closest_ratio = min(aspect_ratios, key=lambda k: abs(aspect_ratios[k] - aspect_ratio))
        
        return closest_ratio
    
    def generate_scenario_image(self, url_scenario, model_id, authorize_scenario, description, width, height, should_remove_background):
        payload_scenario = {
            "modelId": model_id,
            "qualityBoost": False,
            "hideResults": False,
            "intermediateImages": False,
            "prompt": description,
            "numInferenceSteps": 30,
            "numSamples": 1,
            "guidance": 7.5,
            "width": width,                   
            "height": height
        }
        headers_scenario = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Basic <<"+authorize_scenario+">>"
        }
        response = requests.post(url_scenario, json=payload_scenario, headers=headers_scenario)
        if response.status_code == 200:
            data = response.json()
            print(data)
            inference_id = data['inference']['id']
            
            img_id, img_url = self.get_sceneario_image_url(self.scenario_base_url, model_id, inference_id, headers_scenario)
            if img_id == None:
                return None
            else:
                if should_remove_background:
                    img_background_url = self.remove_background_image(self.scenario_base_url, headers_scenario, img_id)
                    return requests.get(img_background_url, headers=headers_scenario).content
                else:
                    return requests.get(img_url, headers=headers_scenario).content
        else:
            print(f'Error: {response.status_code}')
            return None

    def image_derivation(self) -> bytes:
            args = request.args
            prompt = request.json
            userID = int(prompt["userid"])
            username = prompt["username"]
            password = prompt["password"]
            provider = prompt["provider"]
            description = prompt["description"]
            exclude = prompt["exclude"]
            steps = int(prompt["steps"])
            width = int(prompt["width"])
            height = int(prompt["height"])
            image_sixtyfour = str(prompt["data"])
                
            print ("image_derivation::IMAGE[" + str(len(image_sixtyfour))+ "]::prompt=" + description)
            # image_data = base64.b64decode(image_sixtyfour)
            # print ("IMAGE LENGTH=" + str(len(image_data)))
            
            url_scenario = self.scenario_base_url + "/generate/img2img"
            model_id = self.scenario_model_character
            authorize_scenario = base64.b64encode(self.scenario_config.encode('ascii')).decode('ascii')
            payload_scenario = {
                "modelId": model_id,
                "qualityBoost": False,
                "hideResults": False,
                "prompt": description,
                "image": "data:image/png;base64,"+image_sixtyfour, # Your image dataURL here                 
                "numInferenceSteps": 30,
                "numSamples": 1,
                "guidance": 7.5,
                "width": width,                   
                "height": height
            }
            headers_scenario = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": "Basic <<"+authorize_scenario+">>"
            }
            response = requests.post(url_scenario, json=payload_scenario, headers=headers_scenario)
            if response.status_code == 200:
                data = response.json()
                print(data)
                inference_id = data['inference']['id']
                
                img_id, img_url = self.get_sceneario_image_url(self.scenario_base_url, model_id, inference_id, headers_scenario)
                if img_id == None:
                    return None
                else:
                    img_background_url = self.remove_background_image(self.scenario_base_url, headers_scenario, img_id)
                    return requests.get(img_background_url, headers=headers_scenario).content                     
            else:
                return None
    
    def stop(self):
            return jsonify(status="ok")

    def status(self):
            return jsonify(status="ok")
        
    def start_webserver(self):
            self.app.run(host=self.host_address, port=self.port_number, threaded=False)
        

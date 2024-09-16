# AI Backend Service Endpoints

In order for the project to work you need a machine where to run AI endpoints. Follow the instructions on the main README to properly set up the system.

[Backend Setup Presentation](https://youtu.be/alOxMe5vhKE)

## GitHub\AI

	These are the scripts you will run in order for the project to work:
	
		- 1. **OpenAIEnglishServer.py** OpenAI ChatGPT4 Omni-Mini English
		- 2. **OpenAISpanishServer.py** OpenAI ChatGPT4 Omni-Mini Spanish
		- 3. **OpenAIProEnglishServer.py** OpenAI ChatGPT4 Omni English
		- 4. **OpenAIProSpanishServer.py** OpenAI ChatGPT4 Omni Spanish
		- 5. **MistralEnglishServer.py** Mistral-Nemo English
		- 6. **MistralSpanishServer.py** Mistral-Nemo Spanish
		- 7. **MistralProEnglishServer.py** Mistral-Large English
		- 8. **MistralProSpanishServer.py** Mistral-Large Spanish		
		- 9. **GoogleEnglishServer.py** Google's Gemini Flash English
		- 10. **GoogleSpanishServer.py** Google's Gemini Flash Spanish
		- 11. **GoogleProEnglishServer.py** Google's Gemini Pro English
		- 12. **GoogleProSpanishServer.py** Google's Gemini Pro Spanish		

## GitHub\AI\ai_endpoints

	These scripts contains the main logic of the AI backend endpoints:
	
		- 1. **AILLMEndpoints.py** Main script. Contains all the endpoints that the front-end is going to use.
		- 2. **AlchemySQLFunctions.py** Script that allows store in Alchemy database. Used in conversation operations.
		- 3. **EnglishInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in English.
		- 4. **SpanishInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in Spanish.
		- 4. **ServerSpeechGeneration.py** This script will process request for speech synthesis and upload new voice tracks.
		- 5. **ServerAudioGeneration.py** This script will process request for audio synthesis.
		- 5. **ClearDB_en.py** This script to empty the English local Alchemy database.
		- 5. **ClearDB_es.py** This script to empty the Spanish local Alchemy database.
		
		
# AI Backend Service Endpoints

In order for the project to work you need a machine where to run AI endpoints. Follow the instructions on the main README to properly set up the system.

[Backend Setup Presentation](https://youtu.be/alOxMe5vhKE)

## GitHub\AI

These are the scripts you will run in order for the project to work:
	
- 1. **OpenAIEnglishServer.py** OpenAI ChatGPT4 Omni-Mini English
- 2. **OpenAISpanishServer.py** OpenAI ChatGPT4 Omni-Mini Spanish
- 3. **OpenAIGermanServer.py** OpenAI ChatGPT4 Omni-Mini German
- 4. **OpenAIFrenchServer.py** OpenAI ChatGPT4 Omni-Mini French
- 5. **OpenAIItalianServer.py** OpenAI ChatGPT4 Omni-Mini Italian
- 6. **OpenAIProEnglishServer.py** OpenAI ChatGPT4 Omni English
- 7. **OpenAIProSpanishServer.py** OpenAI ChatGPT4 Omni Spanish
- 8. **OpenAIProGermanServer.py** OpenAI ChatGPT4 Omni German
- 9. **OpenAIProFrenchServer.py** OpenAI ChatGPT4 Omni French
- 10. **OpenAIProItalianServer.py** OpenAI ChatGPT4 Omni Italian
- 11. **MistralEnglishServer.py** Mistral-Nemo English
- 12. **MistralSpanishServer.py** Mistral-Nemo Spanish
- 13. **MistralGermanServer.py** Mistral-Nemo German
- 14. **MistralFrenchServer.py** Mistral-Nemo French
- 15. **MistralItalianServer.py** Mistral-Nemo Italian
- 16. **MistralProEnglishServer.py** Mistral-Large English
- 17. **MistralProSpanishServer.py** Mistral-Large Spanish		
- 18. **MistralProGermanServer.py** Mistral-Large German
- 19. **MistralProFrenchServer.py** Mistral-Large French		
- 20. **MistralProItalianServer.py** Mistral-Large Italian		
- 21. **GoogleEnglishServer.py** Google's Gemini Flash English
- 22. **GoogleSpanishServer.py** Google's Gemini Flash Spanish
- 23. **GoogleGermanServer.py** Google's Gemini Flash German
- 24. **GoogleFrenchServer.py** Google's Gemini Flash French
- 25. **GoogleItalianServer.py** Google's Gemini Flash Italian
- 26. **GoogleProEnglishServer.py** Google's Gemini Pro English
- 27. **GoogleProSpanishServer.py** Google's Gemini Pro Spanish		
- 28. **GoogleProGermanServer.py** Google's Gemini Pro German		
- 29. **GoogleProFrenchServer.py** Google's Gemini Pro French		
- 30. **GoogleProItalianServer.py** Google's Gemini Pro Italian		

## GitHub\AI\ai_endpoints

These scripts contains the main logic of the AI backend endpoints:
	
- 1. **AILLMEndpoints.py** Main script. Contains all the endpoints that the front-end is going to use.
- 2. **AlchemySQLFunctions.py** Script that allows store in Alchemy database. Used in conversation operations.
- 3. **EnglishInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in English.
- 4. **SpanishInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in Spanish.
- 4. **GermanInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in German.
- 4. **FrenchInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in French.
- 4. **ItalianInstructions.py** This script define the schemas that the LLM providers should follow to format a proper response in Italian.
- 5. **ServerSpeechGeneration.py** This script will process request for speech synthesis and upload new voice tracks.
- 6. **ServerAudioGeneration.py** This script will process request for audio synthesis.
- 7. **ClearDB_en.py** This script to empty the English local Alchemy database.
- 8. **ClearDB_es.py** This script to empty the Spanish local Alchemy database.
- 8. **ClearDB_de.py** This script to empty the German local Alchemy database.
- 8. **ClearDB_fr.py** This script to empty the French local Alchemy database.
- 8. **ClearDB_it.py** This script to empty the Italian local Alchemy database.
		
		
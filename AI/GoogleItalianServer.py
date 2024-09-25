from ai_endpoints.AILLMEndpoints import AILLMServer
from ai_endpoints.ItalianInstructions import InstructionsAI

# We need JSON prompts for each language
from pydantic import BaseModel, Field
from typing import List
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.chains import ConversationChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory 
from langchain_core.prompts.prompt import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
    
instructions_ai = InstructionsAI()    

# ************************************
# ************************************
# OLLAMA SERVER ENDPOINTS
# ************************************
# ************************************

if __name__ == '__main__':
    ai_llm_server = AILLMServer('0.0.0.0',
                            5304,
                            False, False, False, True, False, False, False, False,
                            instructions_ai.databaseAlchemy, 
                            instructions_ai.voicesLanguage, 
                            instructions_ai.urlSpeechGeneration,
                            instructions_ai.urlImageGeneration,
                            instructions_ai.urlFluxImageGeneration,
                            instructions_ai.templateQuestion,
                            instructions_ai.promptChapters,
                            instructions_ai.parserChapters,
                            instructions_ai.promptCharacters,
                            instructions_ai.parserCharacters,
                            instructions_ai.promptLocations,
                            instructions_ai.parserLocations,
                            instructions_ai.promptStoryPlots,
                            instructions_ai.parserStoryPlots,
                            instructions_ai.promptScene,
                            instructions_ai.parserScene,
                            instructions_ai.promptSceneCharacters,
                            instructions_ai.parserSceneCharacters,
                            instructions_ai.promptPlaces,
                            instructions_ai.parserPlaces,
                            instructions_ai.promptParagraphForCharacter,
                            instructions_ai.parserParagraphForCharacter,
                            instructions_ai.promptBaseCharacters,
                            instructions_ai.parserBaseCharacters,
                            instructions_ai.promptBaseLocations,
                            instructions_ai.parserBaseLocations,
                            instructions_ai.promptBasePlots, 
                            instructions_ai.parserBasePlots,
                            instructions_ai.promptBaseChapters,
                            instructions_ai.parserBaseChapters,                            
                            instructions_ai.promptFormatImage,
                            instructions_ai.parserFormatImage,
                            instructions_ai.promptFormatSoundFX,
                            instructions_ai.parserFormatSoundFX,
                            instructions_ai.promptFormatMusicLoop,
                            instructions_ai.parserFormatMusicLoop,                              
                            instructions_ai.promptFormatCharacterDialog,                            
                            instructions_ai.parserFormatCharacterDialog,                             
                            instructions_ai.promptFormatTranslateToken,
                            instructions_ai.parserFormatTranslateToken,
                            instructions_ai.templateTranslation
                            )
    ai_llm_server.start_webserver()

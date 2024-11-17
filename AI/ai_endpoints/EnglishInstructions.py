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

# ++++++++++++++++++++++
# ++++++++++++++++++++++
# STORY
# ++++++++++++++++++++++
# ++++++++++++++++++++++

# ++++++++++++++++++++++
# ++ CHAPTERS SUMMARY ++ 
class ChapterDescription(BaseModel):
    name: str = Field(description="Chapter's name")
    description: str = Field(description="Summary of the events and characters of the chapter with no less than 200 words")

# ++++++++++++++++++++++
# ++ CHARACTER SUMMARY ++ 
class CharacterActions(BaseModel):
    chapter: str = Field(description="Chapter's name")
    actions: str = Field(description="Description of the actions of the character in the chapter")
    
class CharacterRelationship(BaseModel):
    name: str = Field(description="Name of the related character")
    relationship: str = Field(description="Description of the relationship with the related character")

class CharacterStory(BaseModel):
    name: str = Field(description="Name of the character")
    description: str = Field(description="Description of the character")
    relationships: List[CharacterRelationship] = Field(description="List of relationships of the character with other characters")
    actions: List[CharacterActions] = Field(description="List of actions that perform the character for a chapter")

# ++++++++++++++++++++++
# ++ LOCATION SUMMARY ++ 
class ChapterLocation(BaseModel):
    chapter: str = Field(description="Chapter's name where the location appears")
    events: str = Field(description="Summary of the chapter's events that happen in this location")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Name of the location")
    description: str = Field(description="Description of the location")
    chapters: List[ChapterLocation] = Field(description="List of chapters where the location appears")

# ++++++++++++++++++
# ++ PLOT SUMMARY ++ 
class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Name of the chapter where the current stage of the plot happens")
    description: str = Field(description="Description the events that happen in the chapter for the current stage of the plot")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Location where the current stage of the plot happens")
    description: str = Field(description="Description of the positions of the characters involved in the current stage in that location")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Name of the character that participates in the current stage of the plot")
    description: str = Field(description="Description of the actions the character does in the current stage of the plot")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Name of the current stage of the plot")
    nextstage: str = Field(description="Name of the next stage of the plot")
    description: str = Field(description="Description of the events that happen on the current stage of the plot")
    location: PlotStageLocation = Field(description="Location where the current stage of the plot happens")
    chapter: PlotStageChapter = Field(description="Chapter where the current stage of the plot happens")
    characters: List[PlotStageCharacter] = Field(description="List of characters involved in the current stage of the plot")

class StoryPlot(BaseModel):
    name: str = Field(description="Name of the plot")
    stages: List[StoryPlotStage] = Field(description="List of stages where the plot is developed")
	
class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="List of the multiple plots that contain the story")

# ++++++++++++++++++++++
# ++++++++++++++++++++++
# SCENES
# ++++++++++++++++++++++
# ++++++++++++++++++++++

# -------------------
# -- SCENE SUMMARY --
class SceneDescription(BaseModel):
    name: str = Field(description="Scene's name")
    description: str = Field(description="Description of what happens in the scene")
    firstsentence: str = Field(description="The first sentence of the text where the scene starts")

# -------------------------------
# -- SCENE'S CHARACTER SUMMARY --
class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Scene's name")
    actions: str = Field(description="Description of the actions of the character in the scene")
    
class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Name of the related character")
    relationship: str = Field(description="Description of the relationship with the related character")

class CharacterScene(BaseModel):
    name: str = Field(description="Name of the character")
    description: str = Field(description="Description of the character")
    relationships: List[CharacterSceneRelationship] = Field(description="List of relationships of the character with other characters")
    actions: List[CharacterSceneActions] = Field(description="List of actions that perform the character for a scene")

# ---------------------------
# -- SCENE'S PLACE SUMMARY --
class ScenePlace(BaseModel):
    scene: str = Field(description="Scene's name where the place appears")
    events: str = Field(description="Summary of the scene's events that happen in this place")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Name of the place")
    description: str = Field(description="Description of the place")
    scenes: List[ScenePlace] = Field(description="List of scenes where the place appears")

# ++++++++++++++++++++++++++++++++++++
# ++ PARAGRAPH CHARACTER CONNECTION ++ 
class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Name of the character who this text paragraph belongs")
    paragraph: str = Field(description="Number identification of the text paragraph")
    emotion: str = Field(description="Description of the character's emotions to voice properly the paragraph for the audiobook")

# +++++++++++++++++++++++++++++
# ++ CHARACTER BASE CREATION ++
class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Name of the related character")
    relationship: str = Field(description="Description of the relationship with the related character")

class CharacterBase(BaseModel):
    name: str = Field(description="Name of the character")
    description: str = Field(description="Description of the character")
    relationships: List[CharacterBaseRelationship] = Field(description="List of relationships of the character with other characters")

# ++++++++++++++++++++++
# ++ LOCATION SUMMARY ++ 
class LocationBase(BaseModel):
    name: str = Field(description="Name of the location")
    description: str = Field(description="Description of the location")

# ++++++++++++++++++++++++
# ++ PLOT BASE CREATION ++ 
class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Name of the current stage of the plot")
    nextstage: str = Field(description="Name of the next stage of the plot")
    description: str = Field(description="Description of the events that happen on the current stage of the plot")
    location: PlotStageLocation = Field(description="Location where the current stage of the plot happens")
    characters: List[PlotStageCharacter] = Field(description="List of characters involved in the current stage of the plot")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Name of the plot")
    stages: List[StoryPlotStageItem] = Field(description="List of stages where the plot is developed")
	
class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="List of the multiple plots that contain the story")

# ++++++++++++++++++++++++++++
# ++ CHAPTERS BASE CREATION ++ 
class Location(BaseModel):
    name: str = Field(description="Name of the location")
    description: str = Field(description="Short description of the events of the current chapter that happen in the location")

class Character(BaseModel):
    name: str = Field(description="Name of the character")
    description: str = Field(description="Short description of the events that the character is involved in the current chapter")

class PlotStage(BaseModel):
    name: str = Field(description="Name of the stage of the plot")
    description: str = Field(description="Short description of the events related to the plot stage that happen in the current chapter")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Chapter's name")
    description: str = Field(description="Short description of the events that happen in the chapter considering the information provided about the plot stages, locations and characters with less than 400 words")
    locations: List[Location] = Field(description="Locations where the events of the current chapter happen")
    characters: List[Character] = Field(description="List of characters involved in the current chapter")
    plotsstages: List[PlotStage] = Field(description="List of the plot's stages that are developed in the current chapter")    

# /////////////////////////
# // FORMAT VISUAL IMAGE //
class ImageForScene(BaseModel):
    name: str = Field(description="Name of the image")
    scene: str = Field(description="Name of the scene")
    description: str = Field(description="Description of the image that represents the scene")

# /////////////////////
# // FORMAT SOUND FX //
class SoundFXForScene(BaseModel):
    name: str = Field(description="Name of the sound effect")
    paragraphid: int = Field(description="Identification number of paragraph where the sound effect plays")
    description: str = Field(description="Short description of 6 words that describes a sound effect of an event that happens in the paragraph")

# /////////////////////
# // FORMAT MUSIC LOOP //
class MusicLoopForScene(BaseModel):
    name: str = Field(description="Name of the music loop")
    scene: str = Field(description="Name of the scene")
    description: str = Field(description="Short description of 12 words that describes the style of the music loop linked to the mood of that scene")

# /////////////////////////////
# // FORMAT CHARACTER DIALOG //
class CharacterDialogState(BaseModel):
    name: str = Field(description="Name of the character")
    state: str = Field(description="State of the character")
    paragraphid: int = Field(description="Identification number of the character's dialog paragraph")
    
# ========================
# == FORMAT TRANSLATION ==
class TranslateToken(BaseModel):
    originaltext: str = Field(description="The text to translate")
    translatedtext: str = Field(description="The translated text")
    
# **************************************************************
# **************************************************************
# **************************************************************
# INSTRUCTIONS AI
# **************************************************************
# **************************************************************
# **************************************************************

class InstructionsAI:
    def __init__(self):
        self.urlSpeechGeneration = "http://0.0.0.0:6000"    
        self.urlImageGeneration = "http://0.0.0.0:7860"             
        self.urlFluxImageGeneration = "http://0.0.0.0:7869"
        # self.urlFluxImageGeneration = "https://f26be2c194c343be51.gradio.live"         
        self.databaseAlchemy = 'sqlite:///aibookeditordata_en.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/en'  # Set this to your desired directory
        self.templateQuestion = """In English language, the AI should follow the instructions and requests provided by the human.

                        Current conversation:
                        {history}
                        Human: {input}
                        AI Assistant:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserStoryPlots.get_format_instructions()},
        )

        # ++++++++++++++++++++++
        # ++++++++++++++++++++++
        # SCENES
        # ++++++++++++++++++++++
        # ++++++++++++++++++++++

        # -- SCENE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserScene = JsonOutputParser(pydantic_object=SceneDescription)
        self.promptScene = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="In English language, answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="The AI should translate the text to English language using the information provided by the user.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """The AI must translate the text contained within the XML tag <textsource> into English.

                    Current conversation:
                    {history}
                    <textsource> {input} </textsource>
                    AI Assistant:"""

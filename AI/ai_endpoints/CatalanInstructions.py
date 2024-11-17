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
# ++ RESUM DELS CAPÍTOLS ++ 
class ChapterDescription(BaseModel):
    name: str = Field(description="Nom del capítol")
    description: str = Field(description="Resum dels esdeveniments i personatges del capítol amb més de 200 paraules")

# ++++++++++++++++++++++
# ++ RESUM DELS PERSONATGES ++ 
class CharacterActions(BaseModel):
    chapter: str = Field(description="Nom del capítol")
    actions: str = Field(description="Descripció de les accions del personatge en el capítol")
    
class CharacterRelationship(BaseModel):
    name: str = Field(description="Nom del personatge relacionat")
    relationship: str = Field(description="Descripció de la relació amb el personatge relacionat")

class CharacterStory(BaseModel):
    name: str = Field(description="Nom del personatge")
    description: str = Field(description="Descripció del personatge")
    relationships: List[CharacterRelationship] = Field(description="Llista de relacions del personatge amb altres personatges")
    actions: List[CharacterActions] = Field(description="Llista d'accions realitzades pel personatge en el capítol")

# ++++++++++++++++++++++
# ++ RESUM DE LES LOCALITZACIONS ++ 
class ChapterLocation(BaseModel):
    chapter: str = Field(description="Nom del capítol on apareix la localització")
    events: str = Field(description="Resum dels esdeveniments que succeeixen a la localització")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Nom de la localització")
    description: str = Field(description="Descripció de la localització")
    chapters: List[ChapterLocation] = Field(description="Llista de capítols on apareix la localització")

# ++++++++++++++++++
# ++ RESUM DE LA TRAMA ++ 
class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Nom del capítol on l'actual fase de la trama succeeix")
    description: str = Field(description="Descripció dels esdeveniments que succeeixen en el capítol per a l'actual fase de la trama")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Localització on succeeix l'actual fase de la trama")
    description: str = Field(description="Descripció de les posicions dels personatges implicats en l'actual fase de la trama per a aquesta localització")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Nom del personatge que participa en l'actual fase de la trama")
    description: str = Field(description="Descripció de les accions del personatge en l'actual fase de la trama")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Nom de l'actual fase de la trama")
    nextstage: str = Field(description="Nom de la següent fase de la trama")
    description: str = Field(description="Descripció dels esdeveniments que succeeixen en l'actual fase de la trama")
    location: PlotStageLocation = Field(description="Localització on succeeix l'acció de l'actual fase de la trama")
    chapter: PlotStageChapter = Field(description="Capítol on succeeix l'actual fase de la trama")
    characters: List[PlotStageCharacter] = Field(description="Llista de personatges que participen en l'actual fase de la trama")

class StoryPlot(BaseModel):
    name: str = Field(description="Nom de la trama")
    stages: List[StoryPlotStage] = Field(description="Llista de fases on la trama es desenvolupa")
	
class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Llista de les múltiples trames on succeeix la història.")



# ++++++++++++++++++++++
# ++++++++++++++++++++++
# SCENES
# ++++++++++++++++++++++
# ++++++++++++++++++++++

# -------------------
# -- RESUM DE L'ESCENA --
class SceneDescription(BaseModel):
    name: str = Field(description="Nom de l'escena")
    description: str = Field(description="Descripció del que succeeix en l'escena")
    firstsentence: str = Field(description="Primera frase del text original on comença l'escena")

# -------------------------------
# -- RESUM DELS PERSONATGES DE L'ESCENA --
class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Nom de l'escena")
    actions: str = Field(description="Descripció de les accions del personatge en l'escena")
    
class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Nom del personatge relacionat")
    relationship: str = Field(description="Descripció de la relació amb el personatge relacionat")

class CharacterScene(BaseModel):
    name: str = Field(description="Nom del personatge")
    description: str = Field(description="Descripció del personatge")
    relationships: List[CharacterSceneRelationship] = Field(description="Llista de relacions del personatge amb altres personatges")
    actions: List[CharacterSceneActions] = Field(description="Llista d'accions que realitza el personatge per cada escena")

# ---------------------------
# -- RESUM DELS LLOCS DE L'ESCENA --
class ScenePlace(BaseModel):
    scene: str = Field(description="Nom de l'escena on apareix la localització")
    events: str = Field(description="Resum dels esdeveniments que succeeixen en l'escena per a aquesta localització")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Nom de la localització")
    description: str = Field(description="Descripció de la localització")
    scenes: List[ScenePlace] = Field(description="Llista d'escenes on apareix la localització")


# ++++++++++++++++++++++++++++++++++++
# ++ CONNEXIÓ PARÀGRAF-PERSONATGE ++ 
class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Nom del personatge a qui pertany el paràgraf de text")
    paragraph: str = Field(description="Identificació numèrica del paràgraf de text")
    emotion: str = Field(description="Descripció de les emocions del personatge per vocalitzar correctament el paràgraf per a l'audiollibre")

# +++++++++++++++++++++++++++++
# ++ CREACIÓ BÀSICA DE PERSONATGES ++
class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Nom del personatge relacionat")
    relationship: str = Field(description="Descripció de la relació amb el personatge relacionat")

class CharacterBase(BaseModel):
    name: str = Field(description="Nom del personatge")
    description: str = Field(description="Descripció del personatge")
    relationships: List[CharacterSceneRelationship] = Field(description="Llista de relacions del personatge amb altres personatges")

# ++++++++++++++++++++++
# ++ RESUM DE LOCALITZACIÓ ++ 
class LocationBase(BaseModel):
    name: str = Field(description="Nom de la localització")
    description: str = Field(description="Descripció de la localització")

# ++++++++++++++++++++++++
# ++ CREACIÓ BÀSICA DE LA TRAMA ++ 
class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Nom de l'actual fase de la trama")
    nextstage: str = Field(description="Nom de la següent fase de la trama")
    description: str = Field(description="Descripció dels esdeveniments que succeeixen en l'actual fase de la trama")
    location: PlotStageLocation = Field(description="Localització on succeeix l'acció de l'actual fase de la trama")
    characters: List[PlotStageCharacter] = Field(description="Llista de personatges que participen en l'actual fase de la trama")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Nom de la trama")
    stages: List[StoryPlotStageItem] = Field(description="Llista de fases on es desenvolupa la trama")
	
class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Llista de les múltiples trames on succeeix la història.")

# ++++++++++++++++++++++++++++
# ++ CREACIÓ BÀSICA DE CAPÍTOLS ++ 
class Location(BaseModel):
    name: str = Field(description="Nom de la ubicació")
    description: str = Field(description="Descripció breu dels esdeveniments que succeeixen a la ubicació per al capítol actual")

class Character(BaseModel):
    name: str = Field(description="Nom del personatge")
    description: str = Field(description="Descripció breu de les accions que succeeixen al capítol actual per a la ubicació")

class PlotStage(BaseModel):
    name: str = Field(description="Nom de la fase de la trama argumental")
    description: str = Field(description="Descripció breu dels esdeveniments que succeeixen en la fase de la trama argumental per al capítol actual")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Nom del capítol")
    description: str = Field(description="Descripció breu dels esdeveniments que succeeixen en el capítol considerant la informació proporcionada sobre les fases de la trama, ubicacions i personatges en menys de 400 paraules")
    locations: List[Location] = Field(description="Ubicacions on succeeixen els esdeveniments per al capítol actual")
    characters: List[Character] = Field(description="Llista de personatges involucrats en el capítol actual")
    plotsstages: List[PlotStage] = Field(description="Llista de trames argumentals on es desenvolupa el capítol actual")    

# /////////////////////////
# // FORMAT VISUAL IMATGE //
class ImageForScene(BaseModel):
    name: str = Field(description="Nom de la imatge")
    scene: str = Field(description="Nom de l'escena")
    description: str = Field(description="Descripció de la imatge que representa l'escena")

# /////////////////////
# // FORMAT SO FX //
class SoundFXForScene(BaseModel):
    name: str = Field(description="Nom de l'efecte de so")
    paragraphid: int = Field(description="Número d'identificació del paràgraf on es reprodueix l'efecte de so")
    description: str = Field(description="Descripció breu de 6 paraules que descriu l'efecte de so associat a un esdeveniment que succeeix al paràgraf")

# /////////////////////
# // FORMAT BUCLE MUSICAL //
class MusicLoopForScene(BaseModel):
    name: str = Field(description="Nom de la música")
    scene: str = Field(description="Nom de l'escena")
    description: str = Field(description="Descripció breu de 12 paraules que descriu l'estil del bucle musical associat a l'ambient de l'escena")
    
# /////////////////////////////
# // FORMAT DIÀLEG DEL PERSONATGE //
class CharacterDialogState(BaseModel):
    name: str = Field(description="Nom del personatge")
    state: str = Field(description="Estat del personatge")
    paragraphid: int = Field(description="Número d'identificació del paràgraf de diàleg del personatge")

# ========================
# == FORMAT TRADUCCIÓ ==
class TranslateToken(BaseModel):
    originaltext: str = Field(description="El text a traduir")
    translatedtext: str = Field(description="El text traduït")
    
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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_ca.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/ca'  # Ajusta això al directori que desitges
        self.templateQuestion = """En idioma Català, la IA ha de seguir les instruccions i preguntes que rep de l'humà.

                            Conversa actual:
                            {history}
                            Humà: {input}
                            Assistent IA:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
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
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="En idioma Català, respon a la següent petició de l'usuari.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRADUCCIÓ ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="La IA ha de traduir el text a l'idioma Català utilitzant la informació proporcionada per l'humà.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRADUIR TEXT ++ 
        self.templateTranslation = """La IA ha de traduir el text contingut dins de l'etiqueta XML <textsource> a l'idioma català.

                        Conversa actual:
                        {history}
                        <textsource> {input} </textsource>
                        Assistent IA:"""


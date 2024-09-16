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
    name: str = Field(description="Nombre del capítulo")
    description: str = Field(description="Resumen de los eventos y personajes del capítulo con mas de 200 palabras")

# ++++++++++++++++++++++
# ++ CHARACTER SUMMARY ++ 
class CharacterActions(BaseModel):
    chapter: str = Field(description="Nombre del capítulo")
    actions: str = Field(description="Descripción de las acciones del personaje en el capítulo")
    
class CharacterRelationship(BaseModel):
    name: str = Field(description="Nombre del personaje relacionado")
    relationship: str = Field(description="Descripción de la relación con el personaje relacionado")

class CharacterStory(BaseModel):
    name: str = Field(description="Nombre del personaje")
    description: str = Field(description="Descripción del personaje")
    relationships: List[CharacterRelationship] = Field(description="Lista de relaciones del personaje con los otros personajes")
    actions: List[CharacterActions] = Field(description="Lista de acciones realizadas por el personaje en el capítulo")

# ++++++++++++++++++++++
# ++ LOCATION SUMMARY ++ 
class ChapterLocation(BaseModel):
    chapter: str = Field(description="Nombre del capítulo donde aparece la localización")
    events: str = Field(description="Resumen de los eventos que suceden en la localización")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Nombre de la localización")
    description: str = Field(description="Descripción de la localización")
    chapters: List[ChapterLocation] = Field(description="Lista de capítulos donde aparece la localización")

# ++++++++++++++++++
# ++ PLOT SUMMARY ++ 
class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Nombre del capítulo donde la actual fase de la trama sucede")
    description: str = Field(description="Descripción de los eventos que suceden en el capítulo para la actual fase de la trama")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Localización donde sucede la actual fase de la trama")
    description: str = Field(description="Descripción de las posiciones de los personajes involucrados en la actual fase de la trama para esa localización")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Nombre del personaje que participa en la actual fase de la trama")
    description: str = Field(description="Descripción de las acciones del personaje en la actual fase de la trama")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Nombre de la actual fase de la trama")
    nextstage: str = Field(description="Nombre de la siguiente fase de la trama")
    description: str = Field(description="Descripción de los eventos que suceden en la actual fase de la trama")
    location: PlotStageLocation = Field(description="Localización donde sucede la acción de la actual fase de la trama")
    chapter: PlotStageChapter = Field(description="Capítulo donde sucede la actual fase de la trama")
    characters: List[PlotStageCharacter] = Field(description="Lista de personajes que participan en la actual fase de la trama")

class StoryPlot(BaseModel):
    name: str = Field(description="Nombre de la trama")
    stages: List[StoryPlotStage] = Field(description="Lista de fases donde la trama es desarrollada")
	
class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Lista de las multiples tramas donde sucede la historia.")

# ++++++++++++++++++++++
# ++++++++++++++++++++++
# SCENES
# ++++++++++++++++++++++
# ++++++++++++++++++++++

# -------------------
# -- SCENE SUMMARY --
class SceneDescription(BaseModel):
    name: str = Field(description="Nombre de la escena")
    description: str = Field(description="Descripción de lo que sucede en la escena")
    firstsentence: str = Field(description="Primera frase del texto original donde empieza la escena")

# -------------------------------
# -- SCENE'S CHARACTER SUMMARY --
class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Nombre de la escena")
    actions: str = Field(description="Descripción de las acciones del personaje en la escena")
    
class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Nombre del personaje relacionado")
    relationship: str = Field(description="Descripción de la relación con el personaje relacionado")

class CharacterScene(BaseModel):
    name: str = Field(description="Nombre del personaje")
    description: str = Field(description="Descripción del personaje")
    relationships: List[CharacterSceneRelationship] = Field(description="Lista de relaciones del personajes con otros personajes")
    actions: List[CharacterSceneActions] = Field(description="Lista de acciones de realiza el personaje para por cada escena")

# ---------------------------
# -- SCENE'S PLACE SUMMARY --
class ScenePlace(BaseModel):
    scene: str = Field(description="Nombre de la escena donde la localización aparece")
    events: str = Field(description="Resumen de los eventos que suceden en la escena para esa localización")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Nombre de la localización")
    description: str = Field(description="Descripción de la localización")
    scenes: List[ScenePlace] = Field(description="Lista de escenas donde sucede la localización aparece")

# ++++++++++++++++++++++++++++++++++++
# ++ PARAGRAPH CHARACTER CONNECTION ++ 
class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Nombre del personaje a quien pertenece el parágrafo de texto")
    paragraph: str = Field(description="Identificación numerica del parágrafo de texto")
    emotion: str = Field(description="Descripción de las emociones del personaje para vocalizar correctamente el parágrafo para el audiolibro")

# +++++++++++++++++++++++++++++
# ++ CHARACTER BASE CREATION ++
class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Nombre del personaje relacionado")
    relationship: str = Field(description="Descripción de la relación con el personaje relacionado")

class CharacterBase(BaseModel):
    name: str = Field(description="Nombre del personaje")
    description: str = Field(description="Descripción del personaje")
    relationships: List[CharacterSceneRelationship] = Field(description="Lista de relaciones del personajes con otros personajes")

# ++++++++++++++++++++++
# ++ LOCATION SUMMARY ++ 
class LocationBase(BaseModel):
    name: str = Field(description="Nombre de la localización")
    description: str = Field(description="Descripción de la localización")

# ++++++++++++++++++++++++
# ++ PLOT BASE CREATION ++ 
class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Nombre de la actual fase de la trama")
    nextstage: str = Field(description="Nombre de la siguiente fase de la trama")
    description: str = Field(description="Descripción de los eventos que suceden en la actual fase de la trama")
    location: PlotStageLocation = Field(description="Localización donde sucede la acción de la actual fase de la trama")
    characters: List[PlotStageCharacter] = Field(description="Lista de personajes que participan en la actual fase de la trama")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Nombre de la trama")
    stages: List[StoryPlotStageItem] = Field(description="Lista de fases donde la trama es desarrollada")
	
class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Lista de las multiples tramas donde sucede la historia.")

# ++++++++++++++++++++++++++++
# ++ CHAPTERS BASE CREATION ++ 
class Location(BaseModel):
    name: str = Field(description="Nombre de la ubicación")
    description: str = Field(description="Descripción breve de los eventos que suceden en la ubicación para el capítulo actual")

class Character(BaseModel):
    name: str = Field(description="Nombre del personaje")
    description: str = Field(description="Descripción breve de las acciones que suceden en el capítulo actual para la ubicación")

class PlotStage(BaseModel):
    name: str = Field(description="Nombre de la fase de la trama argumental")
    description: str = Field(description="Descripción breve de los eventos que suceden en la fasa de la trama argumental para el capítulo actual")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Nombre del capítulo")
    description: str = Field(description="Descripción breve de los eventos que suceden en el capítulo considerando la información proporcionada sobre las fases de la trama, ubicaciones y caracteres en menos de 400 palabras")
    locations: List[Location] = Field(description="Ubicaciones donde suceden los eventos para el capítulo actual")
    characters: List[Character] = Field(description="Lista de personajes involucrados en el capítulo actual")
    plotsstages: List[PlotStage] = Field(description="Lista de tramas argumentales donde se desarrolla el capítulo actual")    

# /////////////////////////
# // FORMAT VISUAL IMAGE //
class ImageForScene(BaseModel):
    name: str = Field(description="Nombre de la imagen")
    scene: str = Field(description="Nombre de la escena")
    description: str = Field(description="Descripción de la imagen que representa la escena")

# /////////////////////
# // FORMAT SOUND FX //
class SoundFXForScene(BaseModel):
    name: str = Field(description="Nombre del efecto de sonido")
    paragraphid: int = Field(description="Número de identificación del parágrafo donde se reproduce el efecto de sonido")
    description: str = Field(description="Descripción breve de 6 palabras que describe el efecto de sonido asociado a un evento que sucede en el parágrafo")

# /////////////////////
# // FORMAT MUSIC LOOP //
class MusicLoopForScene(BaseModel):
    name: str = Field(description="Nombre de la música")
    scene: str = Field(description="Nombre de la escena")
    description: str = Field(description="Descripción breve de 12 palabras que describe el estilo del bucle musical asociado al ambiente de la escena")
    
# /////////////////////////////
# // FORMAT CHARACTER DIALOG //
class CharacterDialogState(BaseModel):
    name: str = Field(description="Nombre del personaje")
    state: str = Field(description="Estado del personaje")
    paragraphid: int = Field(description="Número de identificación del parágrafo de diálogo del personaje")

# ========================
# == FORMAT TRANSLATION ==
class TranslateToken(BaseModel):
    originaltext: str = Field(description="El texto a traducir")
    translatedtext: str = Field(description="El texto traducido")
    
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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_es.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/es'  # Set this to your desired directory
        self.templateQuestion = """En idioma Español, la IA debe seguir las intrucciones y preguntas que recibe del humano.

                            Conversación actual:
                            {history}
                            Humano: {input}
                            Asistente IA:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
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
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="En idioma Español, responde a la siguiente petición del usuario.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="La IA debe traducir el texto al idioma Español utilizando la información proporcionada por el humano.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """La IA debe traducir el texto al idioma Español utilizando la información proporcionada por el humano.

                    Conversación actual:
                    {history}
                    Humano: {input}
                    Asistente IA:"""   

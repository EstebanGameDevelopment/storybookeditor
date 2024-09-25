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

class ChapterDescription(BaseModel):
    name: str = Field(description="Nome del capitolo")
    description: str = Field(description="Riassunto degli eventi e dei personaggi del capitolo con almeno 200 parole")

class CharacterActions(BaseModel):
    chapter: str = Field(description="Nome del capitolo")
    actions: str = Field(description="Descrizione delle azioni del personaggio nel capitolo")

class CharacterRelationship(BaseModel):
    name: str = Field(description="Nome del personaggio correlato")
    relationship: str = Field(description="Descrizione della relazione con il personaggio correlato")

class CharacterStory(BaseModel):
    name: str = Field(description="Nome del personaggio")
    description: str = Field(description="Descrizione del personaggio")
    relationships: List[CharacterRelationship] = Field(description="Elenco delle relazioni del personaggio con altri personaggi")
    actions: List[CharacterActions] = Field(description="Elenco delle azioni compiute dal personaggio in un capitolo")

class ChapterLocation(BaseModel):
    chapter: str = Field(description="Nome del capitolo in cui appare la location")
    events: str = Field(description="Riassunto degli eventi del capitolo che si svolgono in questa location")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Nome della location")
    description: str = Field(description="Descrizione della location")
    chapters: List[ChapterLocation] = Field(description="Elenco dei capitoli in cui appare la location")

class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Nome del capitolo in cui avviene l'attuale fase della trama")
    description: str = Field(description="Descrizione degli eventi che si svolgono nel capitolo durante l'attuale fase della trama")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Location in cui avviene l'attuale fase della trama")
    description: str = Field(description="Descrizione delle posizioni dei personaggi coinvolti nell'attuale fase della trama in quella location")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Nome del personaggio che partecipa all'attuale fase della trama")
    description: str = Field(description="Descrizione delle azioni che il personaggio compie nell'attuale fase della trama")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Nome dell'attuale fase della trama")
    nextstage: str = Field(description="Nome della prossima fase della trama")
    description: str = Field(description="Descrizione degli eventi che si svolgono nell'attuale fase della trama")
    location: PlotStageLocation = Field(description="Location in cui avviene l'attuale fase della trama")
    chapter: PlotStageChapter = Field(description="Capitolo in cui avviene l'attuale fase della trama")
    characters: List[PlotStageCharacter] = Field(description="Elenco dei personaggi coinvolti nell'attuale fase della trama")

class StoryPlot(BaseModel):
    name: str = Field(description="Nome della trama")
    stages: List[StoryPlotStage] = Field(description="Elenco delle fasi in cui si sviluppa la trama")

class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Elenco delle trame multiple che compongono la storia")

class SceneDescription(BaseModel):
    name: str = Field(description="Nome della scena")
    description: str = Field(description="Descrizione di ciò che accade nella scena")
    firstsentence: str = Field(description="La prima frase del testo in cui inizia la scena")

class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Nome della scena")
    actions: str = Field(description="Descrizione delle azioni del personaggio nella scena")

class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Nome del personaggio correlato")
    relationship: str = Field(description="Descrizione della relazione con il personaggio correlato")

class CharacterScene(BaseModel):
    name: str = Field(description="Nome del personaggio")
    description: str = Field(description="Descrizione del personaggio")
    relationships: List[CharacterSceneRelationship] = Field(description="Elenco delle relazioni del personaggio con altri personaggi")
    actions: List[CharacterSceneActions] = Field(description="Elenco delle azioni compiute dal personaggio in una scena")

class ScenePlace(BaseModel):
    scene: str = Field(description="Nome della scena in cui appare il luogo")
    events: str = Field(description="Riassunto degli eventi della scena che si svolgono in questo luogo")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Nome del luogo")
    description: str = Field(description="Descrizione del luogo")
    scenes: List[ScenePlace] = Field(description="Elenco delle scene in cui appare il luogo")

class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Nome del personaggio a cui appartiene questo paragrafo di testo")
    paragraph: str = Field(description="Numero identificativo del paragrafo di testo")
    emotion: str = Field(description="Descrizione delle emozioni del personaggio per dare la giusta intonazione al paragrafo nell'audiolibro")

class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Nome del personaggio correlato")
    relationship: str = Field(description="Descrizione della relazione con il personaggio correlato")

class CharacterBase(BaseModel):
    name: str = Field(description="Nome del personaggio")
    description: str = Field(description="Descrizione del personaggio")
    relationships: List[CharacterBaseRelationship] = Field(description="Elenco delle relazioni del personaggio con altri personaggi")

class LocationBase(BaseModel):
    name: str = Field(description="Nome della location")
    description: str = Field(description="Descrizione della location")

class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Nome dell'attuale fase della trama")
    nextstage: str = Field(description="Nome della prossima fase della trama")
    description: str = Field(description="Descrizione degli eventi che si svolgono nell'attuale fase della trama")
    location: PlotStageLocation = Field(description="Location in cui avviene l'attuale fase della trama")
    characters: List[PlotStageCharacter] = Field(description="Elenco dei personaggi coinvolti nell'attuale fase della trama")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Nome della trama")
    stages: List[StoryPlotStageItem] = Field(description="Elenco delle fasi in cui si sviluppa la trama")

class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Elenco delle trame multiple che compongono la storia")

class Location(BaseModel):
    name: str = Field(description="Nome della location")
    description: str = Field(description="Breve descrizione degli eventi del capitolo corrente che accadono nella location")

class Character(BaseModel):
    name: str = Field(description="Nome del personaggio")
    description: str = Field(description="Breve descrizione degli eventi in cui è coinvolto il personaggio nel capitolo corrente")

class PlotStage(BaseModel):
    name: str = Field(description="Nome della fase della trama")
    description: str = Field(description="Breve descrizione degli eventi correlati alla fase della trama che accadono nel capitolo corrente")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Nome del capitolo")
    description: str = Field(description="Breve descrizione degli eventi che accadono nel capitolo considerando le informazioni fornite sulle fasi della trama, le location e i personaggi in meno di 400 parole")
    locations: List[Location] = Field(description="Location in cui si svolgono gli eventi del capitolo corrente")
    characters: List[Character] = Field(description="Elenco dei personaggi coinvolti nel capitolo corrente")
    plotsstages: List[PlotStage] = Field(description="Elenco delle fasi della trama sviluppate nel capitolo corrente")

class ImageForScene(BaseModel):
    name: str = Field(description="Nome dell'immagine")
    scene: str = Field(description="Nome della scena")
    description: str = Field(description="Descrizione dell'immagine che rappresenta la scena")

class SoundFXForScene(BaseModel):
    name: str = Field(description="Nome dell'effetto sonoro")
    paragraphid: int = Field(description="Numero identificativo del paragrafo in cui viene riprodotto l'effetto sonoro")
    description: str = Field(description="Breve descrizione di 6 parole che descrive un effetto sonoro di un evento che accade nel paragrafo")

class MusicLoopForScene(BaseModel):
    name: str = Field(description="Nome del loop musicale")
    scene: str = Field(description="Nome della scena")
    description: str = Field(description="Breve descrizione di 12 parole che descrive lo stile del loop musicale legato all'atmosfera di quella scena")

class CharacterDialogState(BaseModel):
    name: str = Field(description="Nome del personaggio")
    state: str = Field(description="Stato del personaggio")
    paragraphid: int = Field(description="Numero identificativo del paragrafo del dialogo del personaggio")

class TranslateToken(BaseModel):
    originaltext: str = Field(description="Il testo da tradurre")
    translatedtext: str = Field(description="Il testo tradotto")

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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_it.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/it'  # Set this to your desired directory
        self.templateQuestion = """Nella lingua italiana l’AI deve seguire le istruzioni e le richieste impartite dall’utente umano.

                        Conversazione corrente:
                        {history}
                        Utente: {input}
                        Assistente IA:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
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
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="In italiano, rispondere alla richiesta dell'utente.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="L'IA deve tradurre il testo in italiano utilizzando le informazioni fornite dagli esseri umani.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """L'AI deve tradurre il testo in italiano utilizzando le informazioni fornite dall'utente.

                    Conversazione corrente:
                    {history}
                    Utente: {input}
                    Assistente IA:"""   

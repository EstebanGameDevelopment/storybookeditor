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
    name: str = Field(description="Name des Kapitels")
    description: str = Field(description="Zusammenfassung der Ereignisse und Charaktere des Kapitels mit mindestens 200 Wörtern")

class CharacterActions(BaseModel):
    chapter: str = Field(description="Name des Kapitels")
    actions: str = Field(description="Beschreibung der Handlungen des Charakters im Kapitel")

class CharacterRelationship(BaseModel):
    name: str = Field(description="Name des verwandten Charakters")
    relationship: str = Field(description="Beschreibung der Beziehung zum verwandten Charakter")

class CharacterStory(BaseModel):
    name: str = Field(description="Name des Charakters")
    description: str = Field(description="Beschreibung des Charakters")
    relationships: List[CharacterRelationship] = Field(description="Liste der Beziehungen des Charakters zu anderen Charakteren")
    actions: List[CharacterActions] = Field(description="Liste der Handlungen, die der Charakter in einem Kapitel ausführt")

class ChapterLocation(BaseModel):
    chapter: str = Field(description="Name des Kapitels, in dem der Ort erscheint")
    events: str = Field(description="Zusammenfassung der Ereignisse des Kapitels, die an diesem Ort stattfinden")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Name des Ortes")
    description: str = Field(description="Beschreibung des Ortes")
    chapters: List[ChapterLocation] = Field(description="Liste der Kapitel, in denen der Ort erscheint")

class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Name des Kapitels, in dem der aktuelle Abschnitt der Handlung stattfindet")
    description: str = Field(description="Beschreibung der Ereignisse, die im Kapitel im Rahmen des aktuellen Handlungsabschnitts geschehen")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Ort, an dem der aktuelle Abschnitt der Handlung stattfindet")
    description: str = Field(description="Beschreibung der Positionen der beteiligten Charaktere im aktuellen Handlungsabschnitt an diesem Ort")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Name des Charakters, der im aktuellen Handlungsabschnitt mitspielt")
    description: str = Field(description="Beschreibung der Handlungen des Charakters im aktuellen Handlungsabschnitt")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Name des aktuellen Handlungsabschnitts")
    nextstage: str = Field(description="Name des nächsten Handlungsabschnitts")
    description: str = Field(description="Beschreibung der Ereignisse im aktuellen Handlungsabschnitt")
    location: PlotStageLocation = Field(description="Ort, an dem der aktuelle Handlungsabschnitt stattfindet")
    chapter: PlotStageChapter = Field(description="Kapitel, in dem der aktuelle Handlungsabschnitt stattfindet")
    characters: List[PlotStageCharacter] = Field(description="Liste der Charaktere, die im aktuellen Handlungsabschnitt beteiligt sind")

class StoryPlot(BaseModel):
    name: str = Field(description="Name der Handlung")
    stages: List[StoryPlotStage] = Field(description="Liste der Abschnitte, in denen die Handlung entwickelt wird")

class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Liste der mehreren Handlungen, die die Geschichte enthalten")

class SceneDescription(BaseModel):
    name: str = Field(description="Name der Szene")
    description: str = Field(description="Beschreibung dessen, was in der Szene passiert")
    firstsentence: str = Field(description="Der erste Satz des Textes, in dem die Szene beginnt")

class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Name der Szene")
    actions: str = Field(description="Beschreibung der Handlungen des Charakters in der Szene")

class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Name des verwandten Charakters")
    relationship: str = Field(description="Beschreibung der Beziehung zum verwandten Charakter")

class CharacterScene(BaseModel):
    name: str = Field(description="Name des Charakters")
    description: str = Field(description="Beschreibung des Charakters")
    relationships: List[CharacterSceneRelationship] = Field(description="Liste der Beziehungen des Charakters zu anderen Charakteren")
    actions: List[CharacterSceneActions] = Field(description="Liste der Handlungen, die der Charakter in einer Szene ausführt")

class ScenePlace(BaseModel):
    scene: str = Field(description="Name der Szene, in der der Ort erscheint")
    events: str = Field(description="Zusammenfassung der Ereignisse der Szene, die an diesem Ort stattfinden")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Name des Ortes")
    description: str = Field(description="Beschreibung des Ortes")
    scenes: List[ScenePlace] = Field(description="Liste der Szenen, in denen der Ort erscheint")

class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Name des Charakters, zu dem dieser Textabschnitt gehört")
    paragraph: str = Field(description="Nummer des Textabschnitts")
    emotion: str = Field(description="Beschreibung der Emotionen des Charakters, um den Abschnitt für das Hörbuch richtig zu vertonen")

class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Name des verwandten Charakters")
    relationship: str = Field(description="Beschreibung der Beziehung zum verwandten Charakter")

class CharacterBase(BaseModel):
    name: str = Field(description="Name des Charakters")
    description: str = Field(description="Beschreibung des Charakters")
    relationships: List[CharacterBaseRelationship] = Field(description="Liste der Beziehungen des Charakters zu anderen Charakteren")

class LocationBase(BaseModel):
    name: str = Field(description="Name des Ortes")
    description: str = Field(description="Beschreibung des Ortes")

class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Name des aktuellen Handlungsabschnitts")
    nextstage: str = Field(description="Name des nächsten Handlungsabschnitts")
    description: str = Field(description="Beschreibung der Ereignisse, die im aktuellen Handlungsabschnitt geschehen")
    location: PlotStageLocation = Field(description="Ort, an dem der aktuelle Handlungsabschnitt stattfindet")
    characters: List[PlotStageCharacter] = Field(description="Liste der Charaktere, die im aktuellen Handlungsabschnitt beteiligt sind")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Name der Handlung")
    stages: List[StoryPlotStageItem] = Field(description="Liste der Abschnitte, in denen die Handlung entwickelt wird")

class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Liste der verschiedenen Handlungen, die die Geschichte enthalten")

class Location(BaseModel):
    name: str = Field(description="Name des Ortes")
    description: str = Field(description="Kurze Beschreibung der Ereignisse des aktuellen Kapitels, die an diesem Ort geschehen")

class Character(BaseModel):
    name: str = Field(description="Name des Charakters")
    description: str = Field(description="Kurze Beschreibung der Ereignisse, an denen der Charakter im aktuellen Kapitel beteiligt ist")

class PlotStage(BaseModel):
    name: str = Field(description="Name des Handlungsabschnitts")
    description: str = Field(description="Kurze Beschreibung der Ereignisse, die mit dem Handlungsabschnitt im aktuellen Kapitel zusammenhängen")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Name des Kapitels")
    description: str = Field(description="Kurze Beschreibung der Ereignisse, die im Kapitel passieren, unter Berücksichtigung der Informationen über die Handlungsabschnitte, Orte und Charaktere, mit weniger als 400 Wörtern")
    locations: List[Location] = Field(description="Orte, an denen die Ereignisse des aktuellen Kapitels stattfinden")
    characters: List[Character] = Field(description="Liste der Charaktere, die im aktuellen Kapitel beteiligt sind")
    plotsstages: List[PlotStage] = Field(description="Liste der Handlungsabschnitte, die im aktuellen Kapitel entwickelt werden")

class ImageForScene(BaseModel):
    name: str = Field(description="Name des Bildes")
    scene: str = Field(description="Name der Szene")
    description: str = Field(description="Beschreibung des Bildes, das die Szene darstellt")

class SoundFXForScene(BaseModel):
    name: str = Field(description="Name des Soundeffekts")
    paragraphid: int = Field(description="Identifikationsnummer des Abschnitts, in dem der Soundeffekt abgespielt wird")
    description: str = Field(description="Kurze Beschreibung von 6 Wörtern, die einen Soundeffekt eines Ereignisses beschreibt, das im Abschnitt passiert")

class MusicLoopForScene(BaseModel):
    name: str = Field(description="Name der Musikschleife")
    scene: str = Field(description="Name der Szene")
    description: str = Field(description="Kurze Beschreibung von 12 Wörtern, die den Stil der Musikschleife im Zusammenhang mit der Stimmung der Szene beschreibt")

class CharacterDialogState(BaseModel):
    name: str = Field(description="Name des Charakters")
    state: str = Field(description="Zustand des Charakters")
    paragraphid: int = Field(description="Identifikationsnummer des Dialogabschnitts des Charakters")

class TranslateToken(BaseModel):
    originaltext: str = Field(description="Der zu übersetzende Text")
    translatedtext: str = Field(description="Der übersetzte Text")

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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_de.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/de'  # Set this to your desired directory
        self.templateQuestion = """In der deutsch Sprache soll die KI den Anweisungen und Anfragen des Menschen folgen.
                        Aktuelles Gespräch:
                        {history}
                        Mensch: {input}
                        KI-Assistent:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
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
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="In deutsch Sprache, beantworte die Anfrage des Nutzers.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="Die KI muss den Text unter Verwendung der vom Menschen bereitgestellten Informationen ins Deutsche übersetzen.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """Die KI soll den Text auf Deutsch übersetzen, basierend auf den Informationen des Nutzers.
                    Aktuelles Gespräch:
                    {history}
                    Mensch: {input}
                    KI-Assistent:"""   

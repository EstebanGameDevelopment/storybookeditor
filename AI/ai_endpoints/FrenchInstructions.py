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
    name: str = Field(description="Nom du chapitre")
    description: str = Field(description="Résumé des événements et des personnages du chapitre avec un minimum de 200 mots")

class CharacterActions(BaseModel):
    chapter: str = Field(description="Nom du chapitre")
    actions: str = Field(description="Description des actions du personnage dans le chapitre")

class CharacterRelationship(BaseModel):
    name: str = Field(description="Nom du personnage lié")
    relationship: str = Field(description="Description de la relation avec le personnage lié")

class CharacterStory(BaseModel):
    name: str = Field(description="Nom du personnage")
    description: str = Field(description="Description du personnage")
    relationships: List[CharacterRelationship] = Field(description="Liste des relations du personnage avec d'autres personnages")
    actions: List[CharacterActions] = Field(description="Liste des actions effectuées par le personnage dans un chapitre")

class ChapterLocation(BaseModel):
    chapter: str = Field(description="Nom du chapitre où le lieu apparaît")
    events: str = Field(description="Résumé des événements du chapitre qui se déroulent à cet endroit")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Nom de l'emplacement")
    description: str = Field(description="Description de l'emplacement")
    chapters: List[ChapterLocation] = Field(description="Liste des chapitres où le lieu apparaît")

class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Nom du chapitre où se déroule l'étape actuelle de l'intrigue")
    description: str = Field(description="Description des événements qui se déroulent dans le chapitre à l'étape actuelle de l'intrigue")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Lieu où se déroule l'étape actuelle de l'intrigue")
    description: str = Field(description="Description des positions des personnages impliqués dans cette étape de l'intrigue à cet endroit")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Nom du personnage participant à l'étape actuelle de l'intrigue")
    description: str = Field(description="Description des actions du personnage dans cette étape de l'intrigue")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Nom de l'étape actuelle de l'intrigue")
    nextstage: str = Field(description="Nom de l'étape suivante de l'intrigue")
    description: str = Field(description="Description des événements qui se déroulent à l'étape actuelle de l'intrigue")
    location: PlotStageLocation = Field(description="Lieu où se déroule l'étape actuelle de l'intrigue")
    chapter: PlotStageChapter = Field(description="Chapitre où se déroule l'étape actuelle de l'intrigue")
    characters: List[PlotStageCharacter] = Field(description="Liste des personnages impliqués dans cette étape de l'intrigue")

class StoryPlot(BaseModel):
    name: str = Field(description="Nom de l'intrigue")
    stages: List[StoryPlotStage] = Field(description="Liste des étapes où l'intrigue se développe")

class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Liste des intrigues multiples qui composent l'histoire")

class SceneDescription(BaseModel):
    name: str = Field(description="Nom de la scène")
    description: str = Field(description="Description de ce qui se passe dans la scène")
    firstsentence: str = Field(description="La première phrase du texte où commence la scène")

class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Nom de la scène")
    actions: str = Field(description="Description des actions du personnage dans la scène")

class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Nom du personnage lié")
    relationship: str = Field(description="Description de la relation avec le personnage lié")

class CharacterScene(BaseModel):
    name: str = Field(description="Nom du personnage")
    description: str = Field(description="Description du personnage")
    relationships: List[CharacterSceneRelationship] = Field(description="Liste des relations du personnage avec d'autres personnages")
    actions: List[CharacterSceneActions] = Field(description="Liste des actions effectuées par le personnage dans une scène")

class ScenePlace(BaseModel):
    scene: str = Field(description="Nom de la scène où le lieu apparaît")
    events: str = Field(description="Résumé des événements de la scène qui se déroulent à cet endroit")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Nom du lieu")
    description: str = Field(description="Description du lieu")
    scenes: List[ScenePlace] = Field(description="Liste des scènes où le lieu apparaît")

class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Nom du personnage auquel appartient ce paragraphe")
    paragraph: str = Field(description="Numéro d'identification du paragraphe du texte")
    emotion: str = Field(description="Description des émotions du personnage pour vocaliser correctement le paragraphe dans l'audiobook")

class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Nom du personnage lié")
    relationship: str = Field(description="Description de la relation avec le personnage lié")

class CharacterBase(BaseModel):
    name: str = Field(description="Nom du personnage")
    description: str = Field(description="Description du personnage")
    relationships: List[CharacterBaseRelationship] = Field(description="Liste des relations du personnage avec d'autres personnages")

class LocationBase(BaseModel):
    name: str = Field(description="Nom de l'emplacement")
    description: str = Field(description="Description de l'emplacement")

class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Nom de l'étape actuelle de l'intrigue")
    nextstage: str = Field(description="Nom de l'étape suivante de l'intrigue")
    description: str = Field(description="Description des événements qui se déroulent à l'étape actuelle de l'intrigue")
    location: PlotStageLocation = Field(description="Lieu où se déroule l'étape actuelle de l'intrigue")
    characters: List[PlotStageCharacter] = Field(description="Liste des personnages impliqués dans l'étape actuelle de l'intrigue")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Nom de l'intrigue")
    stages: List[StoryPlotStageItem] = Field(description="Liste des étapes où l'intrigue se développe")

class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Liste des intrigues multiples qui composent l'histoire")

class Location(BaseModel):
    name: str = Field(description="Nom de l'emplacement")
    description: str = Field(description="Courte description des événements du chapitre actuel qui se déroulent à cet endroit")

class Character(BaseModel):
    name: str = Field(description="Nom du personnage")
    description: str = Field(description="Courte description des événements auxquels le personnage participe dans le chapitre actuel")

class PlotStage(BaseModel):
    name: str = Field(description="Nom de l'étape de l'intrigue")
    description: str = Field(description="Courte description des événements liés à cette étape de l'intrigue qui se déroulent dans le chapitre actuel")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Nom du chapitre")
    description: str = Field(description="Courte description des événements qui se déroulent dans le chapitre en fonction des informations fournies sur les étapes de l'intrigue, les lieux et les personnages, en moins de 400 mots")
    locations: List[Location] = Field(description="Lieux où se déroulent les événements du chapitre actuel")
    characters: List[Character] = Field(description="Liste des personnages impliqués dans le chapitre actuel")
    plotsstages: List[PlotStage] = Field(description="Liste des étapes de l'intrigue développées dans le chapitre actuel")

class ImageForScene(BaseModel):
    name: str = Field(description="Nom de l'image")
    scene: str = Field(description="Nom de la scène")
    description: str = Field(description="Description de l'image qui représente la scène")

class SoundFXForScene(BaseModel):
    name: str = Field(description="Nom de l'effet sonore")
    paragraphid: int = Field(description="Numéro d'identification du paragraphe où l'effet sonore est joué")
    description: str = Field(description="Courte description de 6 mots qui décrit un effet sonore d'un événement qui se produit dans le paragraphe")

class MusicLoopForScene(BaseModel):
    name: str = Field(description="Nom de la boucle musicale")
    scene: str = Field(description="Nom de la scène")
    description: str = Field(description="Courte description de 12 mots qui décrit le style de la boucle musicale liée à l'humeur de la scène")

class CharacterDialogState(BaseModel):
    name: str = Field(description="Nom du personnage")
    state: str = Field(description="État du personnage")
    paragraphid: int = Field(description="Numéro d'identification du paragraphe de dialogue du personnage")

class TranslateToken(BaseModel):
    originaltext: str = Field(description="Texte à traduire")
    translatedtext: str = Field(description="Texte traduit")

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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_fr.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/fr'  # Set this to your desired directory
        self.templateQuestion = """En langue française, l’IA doit suivre les instructions et demandes fournies par l’utilisateur.

                      Conversation actuelle :
                      {history}
                      Utilisateur : {input}
                      Assistant IA :"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
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
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="En langue française, répondre à la question de l'utilisateur.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="L’IA doit traduire le texte en français en utilisant les informations fournies par les humains.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """L'IA doit traduire le texte en français en fonction des informations de l'utilisateur.
                    Conversation en cours :
                    {history}
                    Humain: {input}
                    Assistant IA:"""   

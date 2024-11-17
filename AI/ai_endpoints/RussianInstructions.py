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
    name: str = Field(description="Название главы")
    description: str = Field(description="Резюме событий и персонажей главы не менее 200 слов")

class CharacterActions(BaseModel):
    chapter: str = Field(description="Название главы")
    actions: str = Field(description="Описание действий персонажа в главе")

class CharacterRelationship(BaseModel):
    name: str = Field(description="Имя связанного персонажа")
    relationship: str = Field(description="Описание отношений с этим персонажем")

class CharacterStory(BaseModel):
    name: str = Field(description="Имя персонажа")
    description: str = Field(description="Описание персонажа")
    relationships: List[CharacterRelationship] = Field(description="Список отношений персонажа с другими персонажами")
    actions: List[CharacterActions] = Field(description="Список действий, выполняемых персонажем в главе")

class ChapterLocation(BaseModel):
    chapter: str = Field(description="Название главы, в которой появляется локация")
    events: str = Field(description="Резюме событий главы, происходящих в этой локации")

class PhysicalLocation(BaseModel):
    name: str = Field(description="Название локации")
    description: str = Field(description="Описание локации")
    chapters: List[ChapterLocation] = Field(description="Список глав, в которых появляется эта локация")

class PlotStageChapter(BaseModel):
    chapter: str = Field(description="Название главы, где происходит текущий этап сюжета")
    description: str = Field(description="Описание событий, происходящих в главе на текущем этапе сюжета")

class PlotStageLocation(BaseModel):
    location: str = Field(description="Локация, где происходит текущий этап сюжета")
    description: str = Field(description="Описание позиций персонажей, участвующих в текущем этапе сюжета в этой локации")

class PlotStageCharacter(BaseModel):
    character: str = Field(description="Имя персонажа, участвующего в текущем этапе сюжета")
    description: str = Field(description="Описание действий персонажа на текущем этапе сюжета")

class StoryPlotStage(BaseModel):
    stage: str = Field(description="Название текущего этапа сюжета")
    nextstage: str = Field(description="Название следующего этапа сюжета")
    description: str = Field(description="Описание событий, происходящих на текущем этапе сюжета")
    location: PlotStageLocation = Field(description="Локация, где происходит текущий этап сюжета")
    chapter: PlotStageChapter = Field(description="Глава, где происходит текущий этап сюжета")
    characters: List[PlotStageCharacter] = Field(description="Список персонажей, участвующих в текущем этапе сюжета")

class StoryPlot(BaseModel):
    name: str = Field(description="Название сюжета")
    stages: List[StoryPlotStage] = Field(description="Список этапов, на которых развивается сюжет")

class StoryPlots(BaseModel):
    plots: List[StoryPlot] = Field(description="Список различных сюжетов, составляющих историю")

class SceneDescription(BaseModel):
    name: str = Field(description="Название сцены")
    description: str = Field(description="Описание того, что происходит в сцене")
    firstsentence: str = Field(description="Первая фраза текста, с которой начинается сцена")

class CharacterSceneActions(BaseModel):
    scene: str = Field(description="Название сцены")
    actions: str = Field(description="Описание действий персонажа в сцене")

class CharacterSceneRelationship(BaseModel):
    name: str = Field(description="Имя связанного персонажа")
    relationship: str = Field(description="Описание отношений с этим персонажем")

class CharacterScene(BaseModel):
    name: str = Field(description="Имя персонажа")
    description: str = Field(description="Описание персонажа")
    relationships: List[CharacterSceneRelationship] = Field(description="Список отношений персонажа с другими персонажами")
    actions: List[CharacterSceneActions] = Field(description="Список действий, выполняемых персонажем в сцене")

class ScenePlace(BaseModel):
    scene: str = Field(description="Название сцены, в которой появляется место")
    events: str = Field(description="Резюме событий сцены, происходящих в этом месте")

class PhysicalPlace(BaseModel):
    name: str = Field(description="Название места")
    description: str = Field(description="Описание места")
    scenes: List[ScenePlace] = Field(description="Список сцен, в которых появляется это место")

class ParagraphForCharacter(BaseModel):
    character: str = Field(description="Имя персонажа, которому принадлежит этот текстовый абзац")
    paragraph: str = Field(description="Идентификационный номер абзаца текста")
    emotion: str = Field(description="Описание эмоций персонажа, чтобы правильно озвучить абзац для аудиокниги")

class CharacterBaseRelationship(BaseModel):
    name: str = Field(description="Имя связанного персонажа")
    relationship: str = Field(description="Описание отношений с этим персонажем")

class CharacterBase(BaseModel):
    name: str = Field(description="Имя персонажа")
    description: str = Field(description="Описание персонажа")
    relationships: List[CharacterBaseRelationship] = Field(description="Список отношений персонажа с другими персонажами")

class LocationBase(BaseModel):
    name: str = Field(description="Название локации")
    description: str = Field(description="Описание локации")

class StoryPlotStageItem(BaseModel):
    stage: str = Field(description="Название текущего этапа сюжета")
    nextstage: str = Field(description="Название следующего этапа сюжета")
    description: str = Field(description="Описание событий, происходящих на текущем этапе сюжета")
    location: PlotStageLocation = Field(description="Локация, где происходит текущий этап сюжета")
    characters: List[PlotStageCharacter] = Field(description="Список персонажей, участвующих в текущем этапе сюжета")

class StoryPlotItem(BaseModel):
    name: str = Field(description="Название сюжета")
    stages: List[StoryPlotStageItem] = Field(description="Список этапов, на которых развивается сюжет")

class StoryPlotsItems(BaseModel):
    plots: List[StoryPlotItem] = Field(description="Список различных сюжетов, составляющих историю")

class Location(BaseModel):
    name: str = Field(description="Название локации")
    description: str = Field(description="Краткое описание событий текущей главы, происходящих в локации")

class Character(BaseModel):
    name: str = Field(description="Имя персонажа")
    description: str = Field(description="Краткое описание событий, в которых участвует персонаж в текущей главе")

class PlotStage(BaseModel):
    name: str = Field(description="Название этапа сюжета")
    description: str = Field(description="Краткое описание событий, связанных с этапом сюжета, которые происходят в текущей главе")

class ChapterBaseDescription(BaseModel):
    name: str = Field(description="Название главы")
    description: str = Field(description="Краткое описание событий, происходящих в главе, с учетом информации о этапах сюжета, локациях и персонажах, менее 400 слов")
    locations: List[Location] = Field(description="Локации, где происходят события текущей главы")
    characters: List[Character] = Field(description="Список персонажей, участвующих в текущей главе")
    plotsstages: List[PlotStage] = Field(description="Список этапов сюжета, развивающихся в текущей главе")

class ImageForScene(BaseModel):
    name: str = Field(description="Название изображения")
    scene: str = Field(description="Название сцены")
    description: str = Field(description="Описание изображения, которое представляет сцену")

class SoundFXForScene(BaseModel):
    name: str = Field(description="Название звукового эффекта")
    paragraphid: int = Field(description="Идентификационный номер абзаца, в котором звучит звуковой эффект")
    description: str = Field(description="Краткое описание в 6 слов, которое описывает звуковой эффект события, происходящего в абзаце")

class MusicLoopForScene(BaseModel):
    name: str = Field(description="Название музыкального фона")
    scene: str = Field(description="Название сцены")
    description: str = Field(description="Краткое описание в 12 слов, которое описывает стиль музыкального фона, соответствующего настроению этой сцены")

class CharacterDialogState(BaseModel):
    name: str = Field(description="Имя персонажа")
    state: str = Field(description="Состояние персонажа")
    paragraphid: int = Field(description="Идентификационный номер абзаца диалога персонажа")

class TranslateToken(BaseModel):
    originaltext: str = Field(description="Текст для перевода")
    translatedtext: str = Field(description="Переведенный текст")

class TranslationOperation(BaseModel):
    instructions: str = Field(description=)
    operation: str = Field(description="")
    translation: str = Field(description=)

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
        self.databaseAlchemy = 'sqlite:///aibookeditordata_ru.db'
        self.voicesLanguage = '/home/esteban/Workspace/Flask/wav_voices/ru'  # Set this to your desired directory
        self.templateQuestion = """По-русски искусственный интеллект должен следовать инструкциям и запросам человека.

                        Текущий разговор:
                        {history}
                        Человек: {input}
                        ИИ-ассистент:"""

        # ++ CHAPTERS SUMMARY ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserChapters = JsonOutputParser(pydantic_object=ChapterDescription)
        self.promptChapters = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserChapters.get_format_instructions()},
        )

        # ++ CHARACTER SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserCharacters = JsonOutputParser(pydantic_object=CharacterStory)
        self.promptCharacters = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserLocations = JsonOutputParser(pydantic_object=PhysicalLocation)
        self.promptLocations = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserLocations.get_format_instructions()},
        )

        # ++ PLOT SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserStoryPlots = JsonOutputParser(pydantic_object=StoryPlots)
        self.promptStoryPlots = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
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
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserScene.get_format_instructions()},
        )

        # -- SCENE'S CHARACTER SUMMARY --    
        # Set up a parser + inject instructions into the prompt template.
        self.parserSceneCharacters = JsonOutputParser(pydantic_object=CharacterScene)
        self.promptSceneCharacters = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserSceneCharacters.get_format_instructions()},
        )

        # -- SCENE'S PLACE SUMMARY --
        # Set up a parser + inject instructions into the prompt template.
        self.parserPlaces = JsonOutputParser(pydantic_object=PhysicalPlace)
        self.promptPlaces = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserPlaces.get_format_instructions()},
        )

        # ++ PARAGRAPH CHARACTER CONNECTION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserParagraphForCharacter = JsonOutputParser(pydantic_object=ParagraphForCharacter)
        self.promptParagraphForCharacter = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserParagraphForCharacter.get_format_instructions()},
        )

        # ++ CHARACTER BASE CREATION ++
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseCharacters = JsonOutputParser(pydantic_object=CharacterBase)
        self.promptBaseCharacters = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseCharacters.get_format_instructions()},
        )

        # ++ LOCATION SUMMARY ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseLocations = JsonOutputParser(pydantic_object=LocationBase)
        self.promptBaseLocations = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseLocations.get_format_instructions()},
        )

        # ++ PLOT BASE CREATION ++     
        # Set up a parser + inject instructions into the prompt template.
        self.parserBasePlots = JsonOutputParser(pydantic_object=StoryPlotsItems)
        self.promptBasePlots = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBasePlots.get_format_instructions()},
        )

        # ++ CHAPTERS BASE CREATION ++ 
        # Set up a parser + inject instructions into the prompt template.
        self.parserBaseChapters = JsonOutputParser(pydantic_object=ChapterBaseDescription)
        self.promptBaseChapters = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserBaseChapters.get_format_instructions()},
        )

        # /////////////////////////
        # // FORMAT VISUAL IMAGE //
        self.parserFormatImage = JsonOutputParser(pydantic_object=ImageForScene)
        self.promptFormatImage = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatImage.get_format_instructions()},
        )

        # /////////////////////
        # // FORMAT SOUND FX //
        self.parserFormatSoundFX = JsonOutputParser(pydantic_object=SoundFXForScene)
        self.promptFormatSoundFX = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatSoundFX.get_format_instructions()},
        )

        # ///////////////////////
        # // FORMAT MUSIC LOOP //
        self.parserFormatMusicLoop = JsonOutputParser(pydantic_object=MusicLoopForScene)
        self.promptFormatMusicLoop = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )

        # ////////////////////////////
        # // FORMAT CHARACTER STATE //
        self.parserFormatCharacterDialog = JsonOutputParser(pydantic_object=CharacterDialogState)
        self.promptFormatCharacterDialog = PromptTemplate(
            template="Ответьте на запрос пользователя на русском языке.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatMusicLoop.get_format_instructions()},
        )
        
        # ========================
        # == FORMAT TRANSLATION ==
        self.parserFormatTranslateToken = JsonOutputParser(pydantic_object=TranslateToken)
        self.promptFormatTranslateToken = PromptTemplate(
            template="Искусственный интеллект должен перевести текст на русский язык, используя информацию, предоставленную человеком.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": self.parserFormatTranslateToken.get_format_instructions()},
        )

        # ++++++++++++++++++++
        # ++ TRANSLATE TEXT ++ 
        self.templateTranslation = """ИИ должен перевести текст, содержащийся внутри тега XML <textsource>, на русский язык.

                    Текущий разговор:
                    {history}
                    <textsource> {input} </textsource>
                    ИИ-ассистент:"""   

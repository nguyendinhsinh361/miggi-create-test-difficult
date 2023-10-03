from pydantic import BaseModel


class LanguageModel(BaseModel):
    vi: str
    en: str


class GeneralModel(BaseModel):
    G_text: list
    G_text_translate: LanguageModel
    G_text_audio: str
    G_text_audio_translate: LanguageModel
    G_audio: list
    G_image: list[str]


class ContentModel(BaseModel):
    Q_text: str
    Q_audio: str
    Q_image: str
    A_text: list[int]
    A_audio: list
    A_image: list
    A_correct: list[int]
    explain: LanguageModel


class QuestionModel(BaseModel):
    id: int
    kind: int
    general: GeneralModel
    content: list[ContentModel]
    scores: list[int]


class ContentModel(BaseModel):
    kind: int
    Questions: list[QuestionModel]


class HSKPartModel(BaseModel):
    time: int = 0
    name: str
    content: list[ContentModel]


class HSKModel(BaseModel):
    title: str
    parts: list[HSKPartModel]
    level: int
    groups: list
    score: int
    pass_score: int
    pass_score: int
    active: int
    time: int

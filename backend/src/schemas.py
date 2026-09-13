from typing import Literal

from pydantic import BaseModel, Field


class Respondent(BaseModel):
    number: int
    name: str


class Deponent(BaseModel):
    name: str
    designation: str
    address: str


class Exhibit(BaseModel):
    label: str
    description: str


class CaseInformation(BaseModel):
    # case information
    forum: str
    jurisdiction_type: str
    case_type: str
    case_number: str
    year: int

    # parties
    petitioner: str
    respondents: list[Respondent]
    answering_respondent_number: int

    # deponent
    respondent_is_org: bool
    deponent: Deponent

    # verification
    verification_verb: str
    jurat_verb: str

    # exhibits
    exhibits: list[Exhibit] = Field(default_factory=list)

    # document details
    place: str
    date: str

    # advocate
    advocate_firm: str

    # reply content
    reply_points: list[str] = Field(default_factory=list, min_length=1)

    # prayer
    prayer_points: list[str] = Field(default_factory=list, min_length=1)


class TemplateSection(BaseModel):
    name: str
    order: int
    placeholder: str
    instruction: str
    numbering: str | None = None
    alignment: str | None = None
    formatting: str | None = None


class DocumentStructure(BaseModel):
    sections: list[TemplateSection] = Field(default_factory=list, min_length=1)


class DocumentSection(BaseModel):
    type: Literal[
        "heading",
        "cause_title",
        "affidavit_title",
        "deponent",
        "numbered_paragraph",
        "prayer_heading",
        "prayer_intro",
        "prayer_item",
        "jurat",
        "verification",
        "advocate",
    ]

    content: str = ""
    number: int | None = None
    label: str | None = None
    bold: bool = False
    alignment: str | None = None


class GeneratedDocument(BaseModel):
    sections: list[DocumentSection] = Field(default_factory=list, min_length=1)


class GeneratedReplyContent(BaseModel):
    paragraphs: list[str] = Field(default_factory=list, min_length=1)

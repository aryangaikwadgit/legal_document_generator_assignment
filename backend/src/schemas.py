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
    # Court and case information
    forum: str
    jurisdiction_type: str
    case_type: str
    case_number: str
    year: int

    #parties
    petitioner: str
    respondents: list[Respondent]
    answering_respondent_number: int

    #deponent
    respondent_is_org: bool
    deponent: Deponent

    #verification 
    verification_verb: str
    jurat_verb: str

    #exhibits
    exhibits: list[Exhibit] = Field(default_factory=list)

    #document details
    place: str
    date: str

    #advocate details
    advocate_firm: str

    #reply content
    reply_points: list[str] = Field(default_factory=list)

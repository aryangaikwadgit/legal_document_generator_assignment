from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.config import ollama_model
from src.prompts import TEMPLATE_ANALYSIS_PROMPT
from src.schemas import DocumentStructure


class TemplateAnalyzer:

    def __init__(self, token_tracker=None):

        self.model = ChatOllama(model=ollama_model)

        self.parser = PydanticOutputParser(pydantic_object=DocumentStructure)

        self.token_tracker = token_tracker

        self.prompt = PromptTemplate(
            template=TEMPLATE_ANALYSIS_PROMPT,
            input_variables=["format_document", "sample_document"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.chain = self.prompt | self.model | self.parser

    def analyze(self, format_document, sample_document):

        response = self.chain.invoke(
            {"format_document": format_document, "sample_document": sample_document}
        )

        if self.token_tracker and hasattr(response, "usage_metadata"):
            usage = response.usage_metadata
            self.token_tracker.add(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
            )

        return response

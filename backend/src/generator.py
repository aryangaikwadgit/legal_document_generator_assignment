from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.config import ollama_model
from src.prompts import GENERATION_PROMPT
from src.schemas import GeneratedDocument


class AffidavitGenerator:

    def __init__(self, token_tracker=None):

        self.model = ChatOllama(model=ollama_model)

        self.parser = PydanticOutputParser(pydantic_object=GeneratedDocument)

        self.token_tracker = token_tracker

        self.prompt = PromptTemplate(
            template=GENERATION_PROMPT,
            input_variables=["document_structure", "mapped_content"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.chain = self.prompt | self.model | self.parser

    def generate(self, mapped_content, document_structure):

        response = self.chain.invoke(
            {
                "document_structure": document_structure.model_dump(),
                "mapped_content": mapped_content,
            }
        )

        if self.token_tracker and hasattr(response, "usage_metadata"):
            usage = response.usage_metadata
            self.token_tracker.add(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
            )

        return response

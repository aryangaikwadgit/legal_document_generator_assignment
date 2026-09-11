from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.config import ollama_model
from src.prompts import EXTRACTION_PROMPT
from src.schemas import CaseInformation


class CaseExtractor:

    def __init__(self):
        self.model = ChatOllama(model=ollama_model)
        self.parser = PydanticOutputParser(pydantic_object=CaseInformation)
        self.batch_size = 3

        self.prompt = PromptTemplate(
            template=EXTRACTION_PROMPT,
            input_variables=["document_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Create the extraction chain
        self.chain = self.prompt | self.model | self.parser

    def extract(self, chunks):

        extracted_data = []

        # Process the document in batches of 3 chunks
        for i in range(0, len(chunks), self.batch_size):

            batch = chunks[i : i + self.batch_size]

            # Join the chunks in the current batch
            document_text = "\n\n".join(batch)

            # Run the extraction chain
            batch_data = self.chain.invoke({"document_text": document_text})

            extracted_data.append(batch_data)

        return extracted_data

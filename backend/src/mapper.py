class ContentMapper:

    def map_content(self, case_information, document_structure):

        mapped_content = case_information.model_dump()

        mapped_content["sections"] = document_structure.sections

        return mapped_content

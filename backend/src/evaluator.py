class AffidavitEvaluator:

    def calculate_score(self, validation_result):
        passed = validation_result["passed_checks"]
        total = validation_result["total_checks"]

        return round((passed / total) * 100, 2) if total else 0

    def find_errors(self, validation_result):
        return [
            result for result in validation_result["checks"] if not result["passed"]
        ]

    def calculate_dimension_scores(self, validation_result):

        checks = validation_result["checks"]

        def passed(name):
            return any(check["check"] == name and check["passed"] for check in checks)

        groups = {
            "entity_accuracy": ["entity_accuracy"],
            "completeness": [
                "required_sections",
                "verification_range",
                "exhibit_references",
            ],
            "structure": [
                "paragraph_numbering",
                "section_order",
            ],
            "consistency": [
                "consistency",
                "verification_range",
            ],
            "template_fidelity": [
                "prayer_format",
                "section_order",
            ],
            "hallucination": ["hallucination"],
        }

        scores = {}

        for dimension, names in groups.items():
            scores[dimension] = round(
                sum(passed(name) for name in names) / len(names) * 100,
                2,
            )

        return scores

    def build_observations(
        self,
        case_information,
        validation_result,
        dimension_scores,
    ):

        observations = []

        expected_count = len(case_information.reply_points) + 1

        if dimension_scores["entity_accuracy"] == 100:
            observations.append(
                "All supplied case entities were preserved in the generated document."
            )
        else:
            observations.append(
                "One or more supplied case entities were not found in the generated document."
            )

        if passed_check(
            validation_result,
            "paragraph_numbering",
        ):
            observations.append(
                f"The document contains {expected_count} sequential numbered body paragraphs."
            )

        if dimension_scores["structure"] == 100:
            observations.append(
                "Required document sections appear in the expected structural order."
            )

        if dimension_scores["template_fidelity"] == 100:
            observations.append(
                "The generated document follows the main formatting conventions of the reference affidavit."
            )

        if passed_check(
            validation_result,
            "hallucination",
        ):
            observations.append("No unsupported case-specific facts were detected.")

        if passed_check(
            validation_result,
            "exhibit_references",
        ):
            observations.append("All supplied exhibit references were detected.")

        return observations

    def evaluate(
        self,
        case_information,
        validation_result,
    ):

        dimension_scores = self.calculate_dimension_scores(validation_result)

        return {
            "document_type": "Affidavit in Reply",
            "overall_score": self.calculate_score(validation_result),
            "dimension_scores": dimension_scores,
            "passed_checks": validation_result["passed_checks"],
            "total_checks": validation_result["total_checks"],
            "errors": self.find_errors(validation_result),
            "observations": self.build_observations(
                case_information,
                validation_result,
                dimension_scores,
            ),
        }


def passed_check(validation_result, name):
    return any(
        check["check"] == name and check["passed"]
        for check in validation_result["checks"]
    )

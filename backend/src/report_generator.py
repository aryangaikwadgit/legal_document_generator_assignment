import json


class EvaluationReportGenerator:

    def generate(self, evaluation, output_path):

        report = {
            "document_type": evaluation["document_type"],
            "overall_score": evaluation["overall_score"],
            "dimension_scores": evaluation["dimension_scores"],
            "validation_summary": {
                "passed_checks": evaluation["passed_checks"],
                "total_checks": evaluation["total_checks"],
            },
            "detected_issues": evaluation["errors"],
            "observations": evaluation.get("observations", []),
            "score_calculation": (
                "Overall score is calculated as "
                "the percentage of deterministic "
                "validation checks that passed: "
                f"{evaluation['passed_checks']} / "
                f"{evaluation['total_checks']} × 100."
            ),
        }

        with open(output_path, "w", encoding="utf-8") as file:

            json.dump(report, file, indent=4, ensure_ascii=False)

        return report

import re


class AccessibilityChecker:

    def check(self, html: str):

        issues = []
        warnings = []
        passed = []

        html_lower = html.lower()


        # -----------------------------
        # Image Accessibility
        # -----------------------------

        images = re.findall(
            r"<img[^>]*>",
            html_lower
        )

        for image in images:

            if "alt=" not in image:

                issues.append(
                    "Image is missing an alt attribute."
                )

        if not images:

            passed.append(
                "No images detected."
            )


        # -----------------------------
        # Button Accessibility
        # -----------------------------

        buttons = re.findall(
            r"<button[^>]*>(.*?)</button>",
            html_lower,
            re.DOTALL
        )

        for button in buttons:

            if not button.strip():

                issues.append(
                    "Button does not contain accessible text."
                )


        # -----------------------------
        # Input Accessibility
        # -----------------------------

        inputs = re.findall(
            r"<input[^>]*>",
            html_lower
        )

        for input_tag in inputs:

            if (
                "aria-label" not in input_tag
                and "id=" not in input_tag
            ):

                warnings.append(
                    "Input may need an accessible label."
                )


        # -----------------------------
        # Semantic HTML
        # -----------------------------

        semantic_tags = [
            "<main",
            "<nav",
            "<header",
            "<footer",
            "<section"
        ]

        if any(
            tag in html_lower
            for tag in semantic_tags
        ):

            passed.append(
                "Semantic HTML elements detected."
            )

        else:

            warnings.append(
                "Consider using semantic HTML."
            )


        # -----------------------------
        # Keyboard Navigation
        # -----------------------------

        if (
            "tabindex" in html_lower
            or "<button" in html_lower
            or "<a " in html_lower
        ):

            passed.append(
                "Interactive elements detected."
            )

        else:

            warnings.append(
                "Verify keyboard navigation."
            )


        score = self.calculate_score(
            issues,
            warnings
        )


        return {
            "issues": issues,
            "warnings": warnings,
            "passed": passed,
            "score": score
        }


    def calculate_score(
        self,
        issues,
        warnings
    ):

        score = 100

        score -= len(issues) * 15

        score -= len(warnings) * 5

        return max(0, score)

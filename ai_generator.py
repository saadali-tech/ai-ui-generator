import os

from openai import OpenAI
from pydantic import BaseModel
from typing import List


class UIComponent(BaseModel):

    name: str
    description: str

    html: str
    css: str
    javascript: str

    accessibility_notes: List[str]


class UIGenerator:

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key
        )


    def generate_ui(
        self,
        description: str,
        framework: str,
        responsive: bool,
        accessibility: bool
    ):

        if responsive:

            responsive_instruction = """
            Make the design fully responsive.
            Support desktop, tablet and mobile screens.
            """

        else:

            responsive_instruction = """
            Responsive design is optional.
            """


        if accessibility:

            accessibility_instruction = """
            Follow WCAG accessibility principles.

            Use:
            - Semantic HTML
            - Accessible labels
            - Keyboard navigation
            - ARIA where appropriate
            - Good color contrast
            - Meaningful button text
            """

        else:

            accessibility_instruction = """
            Follow normal usability practices.
            """


        prompt = f"""
You are an expert UX/UI designer and frontend engineer.

Convert this user requirement into a functional UI:

{description}

Target framework:

{framework}

{responsive_instruction}

{accessibility_instruction}

Generate:

1. Component name
2. Component description
3. Complete HTML
4. Complete CSS
5. JavaScript if required
6. Accessibility recommendations

The design should be:
- Modern
- Clean
- Professional
- User friendly
- Production oriented

Return only structured data matching the required schema.
"""


        response = self.client.chat.completions.parse(

            model="gpt-5",

            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert UI/UX designer,
                    frontend developer and accessibility specialist.
                    """
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            response_format=UIComponent
        )


        result = response.choices[0].message.parsed

        return result

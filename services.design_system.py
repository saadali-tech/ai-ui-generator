class DesignSystem:

    def __init__(self):

        self.colors = {

            "primary": "#4F46E5",

            "secondary": "#7C3AED",

            "success": "#16A34A",

            "danger": "#DC2626",

            "background": "#FFFFFF",

            "text": "#111827"
        }


        self.typography = {

            "font_family":
                "Inter, Arial, sans-serif",

            "heading":
                "32px",

            "body":
                "16px",

            "small":
                "14px"
        }


        self.spacing = {

            "xs": "4px",

            "sm": "8px",

            "md": "16px",

            "lg": "24px",

            "xl": "40px"
        }


    def generate_css(self):

        return f"""

:root {{

    --primary:
        {self.colors["primary"]};

    --secondary:
        {self.colors["secondary"]};

    --success:
        {self.colors["success"]};

    --danger:
        {self.colors["danger"]};

    --background:
        {self.colors["background"]};

    --text:
        {self.colors["text"]};


    --spacing-xs:
        {self.spacing["xs"]};

    --spacing-sm:
        {self.spacing["sm"]};

    --spacing-md:
        {self.spacing["md"]};

    --spacing-lg:
        {self.spacing["lg"]};

    --spacing-xl:
        {self.spacing["xl"]};


    --font-family:
        {self.typography["font_family"]};
}}


* {{
    box-sizing: border-box;
}}


body {{

    font-family:
        var(--font-family);

    color:
        var(--text);

    background:
        var(--background);
}}
"""

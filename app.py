import streamlit as st
from services.ai_generator import UIGenerator
from services.accessibility import AccessibilityChecker
from services.design_system import DesignSystem


st.set_page_config(
    page_title="AI UX/UI Design Generator",
    page_icon="🎨",
    layout="wide"
)


# -----------------------------
# Page Styling
# -----------------------------

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #4F46E5;
}

.subtitle {
    font-size: 18px;
    color: #64748B;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">🎨 AI UX/UI Design Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Generate responsive and accessible UI components
    from natural-language descriptions.
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("⚙️ Design Settings")

framework = st.sidebar.selectbox(
    "Target Framework",
    [
        "HTML/CSS/JavaScript",
        "React",
        "Bootstrap",
        "Tailwind CSS"
    ]
)

responsive = st.sidebar.checkbox(
    "Responsive Design",
    value=True
)

accessibility_enabled = st.sidebar.checkbox(
    "WCAG Accessibility",
    value=True
)

st.sidebar.divider()

st.sidebar.subheader("🎨 Design System")

primary_color = st.sidebar.color_picker(
    "Primary Color",
    "#4F46E5"
)

secondary_color = st.sidebar.color_picker(
    "Secondary Color",
    "#7C3AED"
)


# -----------------------------
# UI Description
# -----------------------------

st.subheader("1️⃣ Describe Your UI")

description = st.text_area(
    "Natural Language Requirement",
    placeholder="""
Example:

Create a modern SaaS dashboard.

Include:
- Sidebar navigation
- Top navigation
- Statistics cards
- Project table
- Progress indicators
- User profile
- Responsive mobile layout
""",
    height=220
)


# -----------------------------
# Wireframe
# -----------------------------

st.subheader("2️⃣ Upload Wireframe")

uploaded_file = st.file_uploader(
    "Upload PNG or JPG wireframe",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Wireframe",
        use_container_width=True
    )

    st.info(
        "Wireframe uploaded successfully. "
        "A production version can connect this image "
        "to a vision model for automatic UI extraction."
    )


# -----------------------------
# Generate UI
# -----------------------------

if st.button(
    "🚀 Generate UI",
    type="primary",
    use_container_width=True
):

    if not description.strip():

        st.error(
            "Please describe the interface first."
        )

    else:

        try:

            with st.spinner(
                "🤖 AI is designing your interface..."
            ):

                generator = UIGenerator()

                result = generator.generate_ui(
                    description=description,
                    framework=framework,
                    responsive=responsive,
                    accessibility=accessibility_enabled
                )

                st.session_state["ui_result"] = result

            st.success(
                "UI generated successfully!"
            )

        except Exception as error:

            st.error(
                f"Generation failed: {error}"
            )


# -----------------------------
# Results
# -----------------------------

if "ui_result" in st.session_state:

    result = st.session_state["ui_result"]

    st.divider()

    st.header(f"🧩 {result.name}")

    st.write(result.description)

    preview_tab, code_tab, accessibility_tab, design_tab, ab_tab = st.tabs(
        [
            "👁️ Live Preview",
            "💻 Generated Code",
            "♿ Accessibility",
            "🎨 Design System",
            "🧪 A/B Testing"
        ]
    )


    # =========================
    # Live Preview
    # =========================

    with preview_tab:

        st.subheader("Live UI Preview")

        preview = f"""
        <!DOCTYPE html>

        <html>

        <head>

        <meta name="viewport"
              content="width=device-width,
              initial-scale=1.0">

        <style>

        {result.css}

        </style>

        </head>

        <body>

        {result.html}

        <script>

        {result.javascript}

        </script>

        </body>

        </html>
        """

        st.components.v1.html(
            preview,
            height=700,
            scrolling=True
        )


    # =========================
    # Generated Code
    # =========================

    with code_tab:

        st.subheader("HTML")

        st.code(
            result.html,
            language="html"
        )

        st.subheader("CSS")

        st.code(
            result.css,
            language="css"
        )

        if result.javascript.strip():

            st.subheader("JavaScript")

            st.code(
                result.javascript,
                language="javascript"
            )

        complete_code = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<style>

{result.css}

</style>

</head>

<body>

{result.html}

<script>

{result.javascript}

</script>

</body>

</html>
"""

        st.download_button(
            "📥 Download Generated UI",
            data=complete_code,
            file_name="generated_ui.html",
            mime="text/html"
        )


    # =========================
    # Accessibility
    # =========================

    with accessibility_tab:

        checker = AccessibilityChecker()

        report = checker.check(
            result.html
        )

        st.metric(
            "Accessibility Score",
            f"{report['score']}/100"
        )

        if report["score"] >= 80:

            st.success(
                "Good accessibility score."
            )

        elif report["score"] >= 50:

            st.warning(
                "Some accessibility improvements are recommended."
            )

        else:

            st.error(
                "Significant accessibility improvements are required."
            )


        st.subheader("❌ Issues")

        if report["issues"]:

            for issue in report["issues"]:
                st.error(issue)

        else:

            st.success(
                "No major issues detected."
            )


        st.subheader("⚠️ Warnings")

        for warning in report["warnings"]:
            st.warning(warning)


        st.subheader("✅ Passed Checks")

        for item in report["passed"]:
            st.success(item)


        st.subheader(
            "AI Accessibility Recommendations"
        )

        for note in result.accessibility_notes:
            st.info(note)


    # =========================
    # Design System
    # =========================

    with design_tab:

        design_system = DesignSystem()

        design_system.colors["primary"] = primary_color
        design_system.colors["secondary"] = secondary_color

        st.subheader("🎨 Color Palette")

        col1, col2 = st.columns(2)

        with col1:

            st.color_picker(
                "Primary",
                primary_color,
                disabled=True
            )

        with col2:

            st.color_picker(
                "Secondary",
                secondary_color,
                disabled=True
            )


        st.subheader("Typography")

        st.write("Font Family: Inter")
        st.write("Heading: 32px")
        st.write("Body: 16px")


        st.subheader("Spacing")

        st.write(
            "XS: 4px | SM: 8px | MD: 16px | "
            "LG: 24px | XL: 40px"
        )


        st.subheader("Design Tokens")

        st.code(
            design_system.generate_css(),
            language="css"
        )


    # =========================
    # A/B Testing
    # =========================

    with ab_tab:

        st.subheader(
            "🧪 A/B Testing Calculator"
        )

        st.write(
            "Compare conversion rates for two UI variants."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Variant A")

            visitors_a = st.number_input(
                "Visitors A",
                min_value=1,
                value=100,
                key="visitors_a"
            )

            conversions_a = st.number_input(
                "Conversions A",
                min_value=0,
                value=10,
                key="conversions_a"
            )


        with col2:

            st.markdown("### Variant B")

            visitors_b = st.number_input(
                "Visitors B",
                min_value=1,
                value=100,
                key="visitors_b"
            )

            conversions_b = st.number_input(
                "Conversions B",
                min_value=0,
                value=12,
                key="conversions_b"
            )


        if st.button(
            "📊 Compare Variants"
        ):

            rate_a = (
                conversions_a / visitors_a
            ) * 100

            rate_b = (
                conversions_b / visitors_b
            ) * 100

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Variant A",
                    f"{rate_a:.2f}%"
                )

            with col2:

                st.metric(
                    "Variant B",
                    f"{rate_b:.2f}%"
                )


            if rate_a > rate_b:

                st.success(
                    "Variant A currently performs better."
                )

            elif rate_b > rate_a:

                st.success(
                    "Variant B currently performs better."
                )

            else:

                st.info(
                    "Both variants have the same conversion rate."
                )

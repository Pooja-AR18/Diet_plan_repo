import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from fpdf import FPDF
import textwrap



# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Personalized Diet Plan Generator",
    page_icon="🥗",
    layout="wide"
)

# Application title and description
st.title("🥗 Personalized Diet Plan Generator")
st.markdown("""
Generate a customized diet plan based on your personal information, goals, and dietary preferences.
Fill out the form below and click 'Create Diet Plan' to get started!
""")

# Sidebar with app information
with st.sidebar:
    st.markdown("### About")
    st.info("""
    This application uses Groq's LLM to generate personalized diet plans.
    Your data is used only for plan generation and is not stored.
    """)


# Function to create LLM chain
def create_llm_chain():
    # Get API key from environment variables
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.5
    )

    prompt_template = ChatPromptTemplate.from_template("""
    You are a professional nutritionist and dietitian. Create a personalized diet plan for a client with the following details:

    - Name: {name}
    - Age: {age}
    - Gender: {gender}
    - Weight: {weight} {weight_unit}
    - Height: {height} {height_unit}
    - Activity Level: {activity_level}
    - Goal: {goal}
    - Plan Duration: {plan_duration}
    - Dietary Restrictions: {dietary_restrictions}
    - Food Preferences: {food_preferences}
    - Number of Meals Per Day: {meals_per_day}
    - Allergies: {allergies}
    - Health Conditions: {health_conditions}
    - Budget Constraints: {budget}
    - Cooking Time Available: {cooking_time}

    
    IMPORTANT INSTRUCTIONS:
    1. You MUST create a complete day-by-day meal plan for the ENTIRE {plan_duration} period.
    2. Each day MUST be clearly numbered (Day 1, Day 2, etc.) up to the total number of days.
    3. Include ALL days sequentially with NO skipping any days.
    4. Keep meal descriptions concise but complete.
    5. If token limits are a concern, reduce the complexity of individual recipes rather than skipping days.
    
    For each day in sequence from Day 1 to the last day of the {plan_duration}, provide:
    1. Day number and brief overview (keep this to 1-2 sentences)
    2. Each meal with simple recipe instructions, main ingredients, and basic nutritional info
    3. Suggested timing for each meal (brief)
    4. 1-2 snack options
    5. Brief hydration recommendation
    
    Structure the plan as follows:
    
    ## Introduction
    [Brief introduction about the plan approach - keep under 100 words]
    
    ## Day 1
    [Day 1 content]
    
    ## Day 2
    [Day 2 content]
    
    [Continue for ALL days in the plan duration with NO SKIPPING]
    
    ## Conclusion
    [Brief conclusion with 3-4 key tips for success - keep under 100 words]
    
    ## Shopping List
    [Simple list for first week only]
    """)

    return LLMChain(llm=llm, prompt=prompt_template)


def create_pdf(text_content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Set margins
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)

    # Split text into lines and add to PDF
    lines = text_content.split('\n')
    for line in lines:
        # Handle long lines by wrapping text
        wrapped_lines = textwrap.wrap(line, width=85)  # Adjust width as needed
        if not wrapped_lines:  # Empty line
            pdf.ln()
            continue
        for wrapped_line in wrapped_lines:
            # Check if line starts with #, if so make it bold
            if line.strip().startswith('#'):
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, wrapped_line, ln=True)
                pdf.set_font("Arial", size=12)
            else:
                pdf.cell(0, 10, wrapped_line, ln=True)

    return pdf.output(dest='S').encode('latin1')

# Main form for user input
with st.form("diet_plan_form"):
    st.subheader("Personal Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name", placeholder="John Doe")
        age = st.number_input("Age", min_value=12, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])

    with col2:
        weight = st.number_input("Weight", min_value=30, max_value=300, value=70)
        weight_unit = st.selectbox("Weight Unit", ["kg", "lbs"])
        height = st.number_input("Height", min_value=100, max_value=250, value=170)
        height_unit = st.selectbox("Height Unit", ["cm", "inches"])

    with col3:
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        )
        goal = st.selectbox(
            "Primary Goal",
            ["Weight Loss", "Weight Maintenance", "Weight Gain", "Muscle Building", "Improve Overall Health",
             "Boost Energy"]
        )

    st.subheader("Diet Preferences")
    col1, col2 = st.columns(2)

    with col1:
        plan_duration = st.selectbox(
            "Plan Duration",
            ["1 week", "2 weeks", "3 weeks", "1 month"]
        )
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Low-Carb", "Paleo", "Gluten-Free", "Dairy-Free"]
        )
        if "None" in dietary_restrictions and len(dietary_restrictions) > 1:
            dietary_restrictions.remove("None")

        food_preferences = st.text_area("Food Preferences (foods you like)",
                                        placeholder="e.g., I love berries, nuts, and grilled chicken")

    with col2:
        meals_per_day = st.slider("Number of Meals Per Day", 2, 6, 3)
        allergies = st.text_input("Allergies", placeholder="e.g., nuts, shellfish, etc.")
        health_conditions = st.text_input("Health Conditions", placeholder="e.g., diabetes, hypertension, etc.")

    st.subheader("Lifestyle Factors")
    col1, col2 = st.columns(2)

    with col1:
        budget = st.select_slider(
            "Budget Constraints",
            options=["Low", "Medium", "High", "No Constraints"]
        )

    with col2:
        cooking_time = st.select_slider(
            "Available Time for Cooking",
            options=["Minimal (15 min or less)", "Moderate (30 min)", "Flexible (1 hour+)"]
        )

    submit_button = st.form_submit_button("Create Diet Plan")

# Process the form submission
if submit_button:
    if not name:
        st.error("Please enter your name.")
    else:
        try:
            with st.spinner("Generating your personalized diet plan..."):
                # Prepare the inputs for the LLM chain
                chain = create_llm_chain()

                # Format dietary restrictions
                dietary_restrictions_str = ", ".join(dietary_restrictions) if dietary_restrictions else "None"

                # Run the chain
                result = chain.run(
                    name=name,
                    age=age,
                    gender=gender,
                    weight=weight,
                    weight_unit=weight_unit,
                    height=height,
                    height_unit=height_unit,
                    activity_level=activity_level,
                    goal=goal,
                    plan_duration=plan_duration,
                    dietary_restrictions=dietary_restrictions_str,
                    food_preferences=food_preferences if food_preferences else "No specific preferences",
                    meals_per_day=meals_per_day,
                    allergies=allergies if allergies else "None",
                    health_conditions=health_conditions if health_conditions else "None",
                    budget=budget,
                    cooking_time=cooking_time
                )

                # Display the result
                st.success("Your personalized diet plan has been generated!")

                # Create tabs for better organization
                tab1, tab2 = st.tabs(["Diet Plan", "Save Options"])

                with tab1:
                    st.markdown("## Your Personalized Diet Plan")
                    st.markdown(result)

                with tab2:
                    st.markdown("## Save Your Diet Plan")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label="Download as Text",
                            data=result,
                            file_name=f"{name.replace(' ', '_')}_diet_plan_{datetime.now().strftime('%Y-%m-%d')}.txt",
                            mime="text/plain"
                        )

                    with col2:
                        pdf_data = create_pdf(result, f"{name.replace(' ', '_')}_diet_plan_{datetime.now().strftime('%Y-%m-%d')}.pdf")
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_data,
                            file_name=f"{name.replace(' ', '_')}_diet_plan_{datetime.now().strftime('%Y-%m-%d')}.pdf",
                            mime="application/pdf"
                        )

#                    with col2:
#                        st.markdown("""
#                        ### Print Instructions
#                        To print your diet plan:
#                        1. Click the menu button (⋮) in the top-right corner
#                        2. Select 'Print'
#                        3. Choose your printer and settings
#                        """)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your API key and try again. If the problem persists, try with different inputs.")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("""
---
### Tips for Success
- Be as specific as possible with your inputs for a more tailored plan
- Consider your daily schedule when selecting the number of meals
- The more information you provide about preferences and restrictions, the better your plan will be
""")
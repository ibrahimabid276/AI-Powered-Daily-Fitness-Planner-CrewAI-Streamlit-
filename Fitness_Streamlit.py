import os
import time
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import streamlit as st
from google.genai.errors import APIError

load_dotenv()

st.set_page_config(
    page_title="Fitness Planner AI",
    page_icon="💪🏼",
    layout="wide"
)

st.title("Daily Fitness Planner 🏋🏻‍♀️")

st.sidebar.header("Your Details")
name = st.sidebar.text_input("Your Name", placeholder="Enter your name")
age = st.sidebar.text_input("Your Age", placeholder="Enter your age")
level = st.sidebar.selectbox("Fitness Level", ["beginner", "intermediate"])
time = st.sidebar.text_input("Workout Time (minutes)", placeholder="e.g. 30")

if st.button("Generate Fitness Plan 💪🏼"):
    if not name:
        st.error("Please enter your name")
        st.stop()
    if not age:
        st.error("Please enter your age")
        st.stop()
    if not time:
        st.error("Please enter workout time")
        st.stop()

    # Reload environment variables to get the latest API key
    load_dotenv(override=True)

    with st.spinner('Generating your fitness plan...'):
        try:
            llm = LLM(
                model="gemini/gemini-2.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )

            fitness_planner = Agent(
                role="fitness planner",
                goal="create a simple daily workout plan",
                backstory="creates easy fitness routines for daily life",
                llm=llm
            )

            warmup_coach = Agent(
                role="warmup coach",
                goal="add warm-up exercises",
                backstory="helps prevent injury with proper warm-ups",
                llm=llm
            )

            recovery_advisor = Agent(
                role="recovery advisor",
                goal="add cool-down and recovery tips",
                backstory="focuses on rest and muscle recovery",
                llm=llm
            )

            reviewer = Agent(
                role="reviewer",
                goal="check if workout is safe and realistic",
                backstory="simplifies workouts for normal people",
                llm=llm
            )

            final_writer = Agent(
                role="final workout writer",
                goal="write the final daily workout plan",
                backstory="prepares clear and simple fitness plans",
                llm=llm
            )

            task1 = Task(
                description=f"Create a daily workout plan for {name}, age {age}, fitness level {level}, for {time} minutes.",
                expected_output="workout plan",
                agent=fitness_planner
            )

            task2 = Task(
                description="Add simple warm-up exercises suitable for daily workouts.",
                expected_output="warm-up routine",
                agent=warmup_coach
            )

            task3 = Task(
                description="Add cool-down and recovery advice after workout.",
                expected_output="recovery tips",
                agent=recovery_advisor
            )

            task4 = Task(
                description="Review the workout plan and make it safe and realistic.",
                expected_output="reviewed plan",
                agent=reviewer
            )

            task5 = Task(
                description=f"Write the final daily workout plan clearly for {name}.",
                expected_output="final workout plan",
                agent=final_writer
            )

            crew = Crew(
                agents=[fitness_planner, warmup_coach, recovery_advisor, reviewer, final_writer],
                tasks=[task1, task2, task3, task4, task5],
                verbose=True,
                memory=True
            )

            result = crew.kickoff()

            st.subheader("Your Daily Fitness Plan")
            st.write(result)
            
        except APIError as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                st.error("⚠️ API rate limit exceeded. Please wait ~20 seconds and try again.")
                st.info("💡 Tip: You can create a new free Gemini API key at https://aistudio.google.com/app/apikey")
            else:
                st.error(f"API Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
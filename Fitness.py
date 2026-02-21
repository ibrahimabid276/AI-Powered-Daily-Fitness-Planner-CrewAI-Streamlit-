from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

print("==" * 15)
print("     Daily Fitness Planner")
print("==" * 15)

name = input("Your name: ")
if name == "":
    name = "User"

age = input("Your age: ")
level = input("Fitness level (beginner/intermediate): ")
time = input("Workout time per day (minutes): ")

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
    memory=True,
    output_log_file="crew_logs.txt", 
    embedder={
            "provider": "sentence-transformer",
            "config": {
                "model": "all-MiniLM-L6-v2"
         }
        }
)

result = crew.kickoff()

print("\nYour Daily Fitness Plan:\n")
print(result)

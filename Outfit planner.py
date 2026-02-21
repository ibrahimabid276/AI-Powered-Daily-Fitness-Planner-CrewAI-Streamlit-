from crewai import Task,Crew,Agent,LLM
from dotenv import load_dotenv
import os
load_dotenv ()

 # Tools
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("AIzaSyDn1YVsKRi0KX8gtpRAB81ogTOIbhPvLc4")
)

# -----------------------INTRO -------------------------
print("=" * 50)
print("Outfit Planner")
print("=" * 50)

 # Input
name = input("What 's your name ?")
occasion=input("What's your ocassion?")
preference=input("What's your style preference?")
Weather=input("What's current weather ?")

# -----------------------  AGEnt 1 : TIPS ----------------------------
researcher = Agent(
    role='Fashion Research Expert',
    goal='Find appropriate fashion tips for the occasion',
    backstory='You research clean, appropriate fashion advice.',
    
    verbose=True
)

# ---------------- AGENT 2: OUTFIT PLANNER ----------------
planner = Agent(
    role='Outfit Planner',
    goal='Create a stylish and appropriate outfit',
    backstory='You combine clothes into clean and stylish outfits.',
    verbose=True
)


# ---------------- AGENT 3: STYLE REVIEWER ----------------
reviewer = Agent(
    role='Style Reviewer',
    goal='Review outfit and suggest improvements',
    backstory='You make sure outfits are appropriate and well-matched.',
    verbose=True
)



# ---------------- TASKS ----------------
research_task = Task(
    description=(
        f"Research fashion tips for a {preference} outfit suitable for "
        f"{occasion} in {Weather} weather."
    ),
    expected_output="Fashion tips and clothing suggestions",
    agent=researcher
)

plan_task = Task(
    description=(
        f"Create a full outfit plan for {name} using the researched fashion tips."
    ),
    expected_output="A complete outfit plan",
    agent=planner
)

review_task = Task(
    description=(
        f"Review the outfit plan and improve it if needed. "
        f"Ensure it is modest and appropriate."
    ),
    expected_output="Reviewed and improved outfit plan",
    agent=reviewer
)

# ---------------- RUN CREW ----------------
crew = Crew(
    agents=[researcher, planner, reviewer],
    tasks=[research_task, plan_task, review_task]
)

result = crew.kickoff()
# ---------------- SAVE TO FILE ----------------
filename = f"{name}_outfit_plan.txt"

with open(filename, "w") as f:
    f.write(f"OUTFIT PLAN FOR {name.upper()}\n")
    f.write(f"Occasion: {occasion}\n")
    f.write(f"Weather: {Weather}\n")
    f.write(f"Style Preference: {preference}\n\n")
    f.write(str(result))

# ---------------- OUTPUT ----------------
print(result)
print(f"\nSaved to {filename}!")

# ----------------  END     ---------------
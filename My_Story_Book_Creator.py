
from crewai import Agent, Task, Crew,LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()
save_tool = SerperDevTool()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"))

print("^^" * 16)
print("      My Story Book Creator")
print("^^" * 16)

n = input("Name of hero: ")
if n == "":
    n = "Hero"

print("1 adventure")
print("2 mystery")
print("3 funny")
print("4 scary")

t = input("choose story type: ")

if t == "2":
    kind = "Mystery"
elif t == "3":
    kind = "Funny"
elif t == "4":
    kind = "Scary"
else:
    kind = "Adventure"

p = input("power: ")
loc = input("place: ")

writerGuy = Agent(
    role="writer",
    goal="make a kids story",
    backstory="writes simple stories for kids",
    llm=llm
)

checker = Agent(
    role="review person",
    goal="check if story is okay",
    backstory="helps improve stories a bit",
    llm=llm
)

finisher = Agent(
    role="final editor",
    goal="finish the story and save it",
    backstory="prepares final version",
    llm=llm
)

task1 = Task(
    description=f"Write a {kind} story with {n} who has {p} power in {loc}.",
    expected_output="story text",
    agent=writerGuy
)

task2 = Task(
    description="Read story and say what can be better.",
    expected_output="feedback",
    agent=checker
)

task3 = Task(
    description=f"Make final story for {n}.",
    expected_output="final story",
    agent=finisher
)

task4 = Task(
    description=f"Save story in file {n}_storybook.txt",
    expected_output="saved",
    agent=finisher,
    tools=[save_tool]
)

crew = Crew(
    agents=[writerGuy, checker, finisher],
    tasks=[task1, task2, task3, task4]
)

out = crew.kickoff()

print(out)
print("saved in", n + "_storybook.txt")


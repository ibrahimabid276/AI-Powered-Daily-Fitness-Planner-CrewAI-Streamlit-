from crewai import Agent, Task, Crew, LLM
import os

# LLM setup
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Agent 1: Joke Writer
joke_writer = Agent(
    role="Joke Writer",
    goal="Write a funny joke for kids",
    backstory="You are creative and good at writing clean jokes.",
    llm=llm
)

# Agent 2: Joke Reviewer
joke_reviewer = Agent(
    role="Joke Reviewer",
    goal="Make sure the joke is clean and suitable for kids",
    backstory="You check jokes for clarity, humor, and kid-friendliness.",
    llm=llm
)

# Task 1: Write the joke
write_joke_task = Task(
    description="Write a 5-line funny joke about a granny",
    expected_output="A 5-line funny joke",
    agent=joke_writer
)

# Task 2: Review and improve the joke
review_joke_task = Task(
    description="Review the joke and improve it if needed, keeping it kid-friendly",
    expected_output="A polished, kid-friendly joke",
    agent=joke_reviewer
)

# Create crew (multi-agent)
crew = Crew(
    agents=[joke_writer, joke_reviewer],
    tasks=[write_joke_task, review_joke_task],
    verbose=True
)

# Run
result = crew.kickoff()
print(result)

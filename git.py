from crewai import Agent,Task,Crew,LLM

# Single agent
# LLM setup(Brain of agent)
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key="YOUR_API_KEY_HERE"
)

# Create an agent(Define what agent is)
joke_agent = Agent(
    role="Joke Writer",
    goal="Tell a funny joke for kids",
    backstory="You are good at writing clean, simple, funny jokes.",
    llm=llm
)

# Create a task( giving tasks)
joke_task = Task(
    description="Write a 5-line funny joke about a granny",
    expected_output="A short, funny joke suitable for kids",
    agent=joke_agent
)

# Create crew(Managing execution)
crew = Crew(
    agents=[joke_agent],
    tasks=[joke_task],
    verbose=True
)

# Run
result = crew.kickoff()
print(result)


from crewai import Agent, Task, Crew
from crewai.llms import groq

llm = groq(
    model="",
    api_key="HUGGINGFACE_API_KEY"
)
story_agent = Agent(
    role = "storyteller",
    goal = "tell a fun story for kids",
    backstory = "a creative story for kids about traveling and bedtime stories"
)

story_task = Task(
    description = "create a 5 line story which should be funny story talking about a cat",
    agent = story_agent
)
crew = Crew(
    agents=[story_agent],
    tasks=[story_task]
)

result = crew.kickoff()
print(result)

from crewai import Agent, Task, Crew, Process

# -------------------------
# 1. Create Agents
# -------------------------

joke_writer = Agent(
    role="Joke Writer",
    goal="Create a funny one-sentence joke about a given topic",
    backstory="You are a creative comedian who loves making people laugh.",
    verbose=True
)

joke_judge = Agent(
    role="Joke Judge",
    goal="Rate the joke from 1 to 10 and give friendly feedback",
    backstory="You are a kind and supportive comedy judge.",
    verbose=True
)

# -------------------------
# 2. Create Tasks
# -------------------------

write_joke_task = Task(
    description="Write ONE sentence joke about school.",
    expected_output="A single sentence joke.",
    agent=joke_writer
)

judge_joke_task = Task(
    description="Rate the joke from 1 to 10 and give short, friendly feedback.",
    expected_output="Score and feedback.",
    agent=joke_judge
)

# -------------------------
# 3. Create the Crew
# -------------------------

crew = Crew(
    agents=[joke_writer, joke_judge],
    tasks=[write_joke_task, judge_joke_task],
    process=Process.sequential  # run tasks one after another
)

# -------------------------
# 4. Run the Crew
# -------------------------

result = crew.kickoff()

print("\n🎉 FINAL OUTPUT:")
print(result)



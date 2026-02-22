import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Cold Email Generator 🎌",
    page_icon="📧",
    layout="wide"
)

st.title("Cold Email AI🤖")

# User inputs for customization
st.sidebar.header("Your Information")
your_name = st.sidebar.text_input("Your Name", "Your Name")
your_company = st.sidebar.text_input("Your Company", "Your Company")
your_service = st.sidebar.text_area("Your Service/Offering", "Describe what service or product you offer...")

st.header("Target Company Information")
target_url = st.text_input("Enter Target Company Website URL", placeholder="https://example.com")
target_company_name = st.text_input("Target Company Name (optional)", placeholder="Leave blank to auto-detect")


def get_gemini_api_key() -> str | None:
    # Streamlit Cloud commonly stores secrets in st.secrets instead of .env files.
    return os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if st.button("Generate Cold Email 🤖"):
    if not target_url:
        st.error("Please enter a target company URL")
        st.stop()
    
    if not your_service or your_service == "Describe what service or product you offer...":
        st.error("Please describe your service in the sidebar")
        st.stop()

    gemini_api_key = get_gemini_api_key()
    if not gemini_api_key:
        st.error(
            "Missing GEMINI_API_KEY. Add it to Streamlit Secrets or environment variables."
        )
        st.stop()

    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=gemini_api_key,
        use_native=False
    )

    scrape_tool = ScrapeWebsiteTool()

    researcher = Agent(
        role='Business Intelligence Analyst',
        goal='Analyze the target company website and identify their core business and potential weaknesses.',
        backstory="You are an expert at analyzing businesses just by looking at their landing page. You look for what they do and where they might be struggling.",
        tools=[scrape_tool],
        verbose=True,
        allow_delegation=True,
        memory=True,
        llm=llm
    )

    strategist = Agent(
        role='Service Strategist',
        goal='Match the target company needs with the service being offered.',
        backstory=f"""You are an expert at identifying business needs and matching them with solutions.
Your goal is to read the analysis of a prospect and determine how the following service can help them:

SERVICE BEING OFFERED:
{your_service}

You must explain why this service is a good fit for the target company based on their website analysis.""",
        verbose=True,
        memory=True,
        llm=llm
    )

    writer = Agent(
        role='Senior Sales Copywriter',
        goal='Write a personalized cold email that sounds human and professional.',
        backstory="""You write emails that get replies. You never sound robotic.
You mention specific details found by the Researcher to prove we actually looked at their site.""",
        verbose=True,
        llm=llm
    )

    task_analyze = Task(
        description=f"Scrape the website {target_url}. Summarize what the company does and identify 1 key area where they could improve (e.g., design, traffic, automation).",
        expected_output="A brief summary of the company and their potential pain points.",
        agent=researcher
    )

    task_strategize = Task(
        description="Based on the analysis, pick ONE service from our Agency Knowledge Base that solves their problem. Explain the match.",
        expected_output="The selected service and the reasoning for the match.",
        agent=strategist
    )

    task_write = Task(
        description=f"""Draft a personalized cold email from {your_name} at {your_company} to the target company.
        
Key requirements:
- Mention specific details found from their website to prove you researched them
- Explain how {your_service} can help solve their specific pain points
- Keep it under 150 words
- Make it sound human and professional, not robotic
- Include a clear call-to-action""",
        expected_output="A professional cold email ready to send.",
        agent=writer
    )

    sales_crew = Crew(
        agents=[researcher, strategist, writer],
        tasks=[task_analyze, task_strategize, task_write],
        process=Process.sequential,
        verbose=True
    )

    result = sales_crew.kickoff()

    st.subheader("Generated Cold Email")
    st.write(result)

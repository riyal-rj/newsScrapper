from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from utils.config import OPENAI_API_KEY
from typing import List, Dict

def create_summarizer_agent() -> Agent:
    """
    Create a CrewAI agent for summarizing news articles.
    
    Returns:
        Configured summarizer agent.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    return Agent(
        role="News Summarizer",
        goal="Summarize stock and market-related news articles for a given company.",
        backstory="Skilled in condensing large amounts of text into concise, informative summaries.",
        llm=llm,
        verbose=True
    )

def summarize_articles(company: str, articles: List[Dict]) -> str:
    """
    Summarize a list of news articles for a company.
    
    Args:
        company: Name of the company.
        articles: List of article dictionaries with title and content.
    
    Returns:
        Concise summary of the articles (150-200 words).
    """
    summarizer_agent = create_summarizer_agent()
    summary_input = "\n\n".join([f"Title: {article['title']}\nContent: {article['content']}" for article in articles])
    
    summary_task = Task(
        description=f"Summarize the following articles for {company}:\n{summary_input}",
        agent=summarizer_agent,
        expected_output=f"A concise summary (150-200 words) of stock and market news for {company}."
    )
    
    crew = Crew(agents=[summarizer_agent], tasks=[summary_task], verbose=True)
    summary = crew.kickoff()
    
    return str(summary)
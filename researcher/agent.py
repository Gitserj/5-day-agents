import os
from google.adk.models.lite_llm import LiteLlm
import litellm

from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

litellm.model_alias_map = {
    "gemini-2.5-flash": "openrouter/google/gemini-2.5-flash",
    "gemini-2.5-flash-lite": "openrouter/google/gemini-2.5-flash-lite"
}

# Tech Researcher: Focuses on AI and ML trends.
tech_researcher = Agent(
    name="TechResearcher",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key="tech_research", # The result of this agent will be stored in the session state with this key.
)

# Health Researcher: Focuses on medical breakthroughs.
health_researcher = Agent(
    name="HealthResearcher",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="health_research", # The result will be stored with this key.
)

# Finance Researcher: Focuses on fintech trends.
finance_researcher = Agent(
    name="FinanceResearcher",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""Research current fintech trends. Include 3 key trends,
their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="finance_research", # The result will be stored with this key.
)

# The AggregatorAgent runs *after* the parallel step to synthesize the results.
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these three research findings into a single executive summary:

    **Technology Trends:**
    {tech_research}
    
    **Health Breakthroughs:**
    {health_research}
    
    **Finance Innovations:**
    {finance_research}
    
    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary", # This will be the final output of the entire system.
)

# The ParallelAgent runs all its sub-agents simultaneously.
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher],
)

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)
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

# Outline Agent: Creates the initial blog post outline.
outline_agent = Agent(
    name="OutlineAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""Создайте план блога по заданной теме, включающий:
    1. Цепляющий заголовок
    2. Вступительную завязку
    3. 3–5 основных разделов с 2–3 тезисами в каждом
    4. Заключительную мысль""",
    output_key="blog_outline", # The result of this agent will be stored in the session state with this key.
)

# Writer Agent: Writes the full blog post based on the outline from the previous agent.
writer_agent = Agent(
    name="WriterAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    # The `{blog_outline}` placeholder automatically injects the state value from the previous agent's output.
    instruction="""Строго следуйте этому плану: {blog_outline}
    Напишите краткую запись в блоге объёмом 200–300 слов, содержательную и увлекательную.""",
    output_key="blog_draft", # The result of this agent will be stored with this key.
)

# Editor Agent: Edits and polishes the draft from the writer agent.
editor_agent = Agent(
    name="EditorAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    # This agent receives the `{blog_draft}` from the writer agent's output.
    instruction="""Отредактируй этот черновик: {blog_draft}
    Ваша задача — отшлифовать текст, исправив грамматические ошибки, улучшив последовательность и структуру предложений, а также повысив общую ясность.""",
    output_key="final_blog", # This is the final output of the entire pipeline.
)

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)

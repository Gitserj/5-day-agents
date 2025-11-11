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

# This agent runs ONCE at the beginning to create the first draft.
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key="current_story", # Stores the first draft in the state.
)

critic_agent = Agent(
    name="CriticAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}
    
    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique", # Stores the feedback in the state.
)

# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

# This agent refines the story based on critique OR calls the exit_loop function.
refiner_agent = Agent(
    name="RefinerAgent",
    model=LiteLlm(
        # Specify the OpenRouter model using 'openrouter/' prefix
        model="gemini-2.5-flash-lite",
        # Explicitly provide the API key from environment variables
        api_key=os.getenv("OPENROUTER_API_KEY"),
        # Explicitly provide the OpenRouter API base URL
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    
    output_key="current_story", # It overwrites the story with the new, refined version.
    tools=[FunctionTool(exit_loop)], # The tool is now correctly initialized with the function reference.
)


# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2, # Prevents infinite loops
)

# The root agent is a SequentialAgent that defines the overall workflow: Initial Write -> Refinement Loop.
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import (
    AgentExecutor,
    AgentType,
    Tool,
    create_react_agent,
)
from langchain import hub

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    """Lookup the LinkedIn URL of a person based on their name"""
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

    prompt = hub.pull("hwchase17/react")

    agent_tools = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            description="Useful for when you need to get the LinkedIn profile URL",
            func=get_profile_url,
        )
    ]

    agent = create_react_agent(
        llm,
        agent_tools,
        prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=True
    )

    linkedin_url = agent_executor.invoke({
        "input": f'Give me the LinkedIn profile URL of {name}, your answer should contain only the URL'
    })

    return linkedin_url['output']

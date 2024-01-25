from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import (
    AgentExecutor,
    AgentType,
    Tool,
    create_react_agent,
    initialize_agent,
)
from langchain import hub

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    """Lookup the LinkedIn URL of a person based on their name"""
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    template = """given the full name {name} of a person, I want you to get me a link to their Linkedin profile page. Your answer should contain only a URL"""

    prompt = hub.pull("hwchase17/react")

    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            description="Useful for when you need to get the LinkedIn profile URL",
            func=get_profile_url,
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(input_variables=["name"], template=template)

    linkedin_url = agent.run(prompt_template.format_prompt(name=name))

    return linkedin_url

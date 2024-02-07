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

    template = """given the full name {name_of_person} I want you to get me a link to their
    LinkedIn profile page. Your answer should contain only a URL"""
    prompt_template = PromptTemplate.from_template(template)

    prompt = hub.pull("hwchase17/react")

    agent_tools = [
        get_profile_url
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
        "input": template.format(name_of_person=name)
    })

    return linkedin_url['output']

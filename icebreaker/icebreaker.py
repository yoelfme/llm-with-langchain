import urllib.parse

from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from thidparties.linkedin import scrape_linkedin_profile
from thidparties.twitter import scrape_user_tweets
from output_parsers import person_intel_parser, PersonIntel


def ice_break(name: str) -> tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)

    # if the linkedin_profile_url is not a valid url, then we need to stop the program
    if not urllib.parse.urlparse(linkedin_profile_url).scheme:
        raise ValueError("The LinkedIn profile URL is not valid")

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary of the person
        2. the interesting facts about the person
        3. the topics of interest of the person
        4. 2 creative ice breakers to open a conversation with them

        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        }
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

    chain = LLMChain(prompt=summary_prompt_template, llm=llm)

    output = chain.invoke({"information": linkedin_data})

    return person_intel_parser.parse(output["text"]), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Icebreaker is running...")
    result = ice_break("Eden Marco")

    print(result)

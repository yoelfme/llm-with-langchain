from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from thidparties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

if __name__ == "__main__":
    print("Icebreaker is running...")

    linkedin_profile_url = linkedin_lookup_agent('Eden Marco')

    # if the linkedin_profile_url is not a valid url, then we need to stop the program
    if "linkedin.com" not in linkedin_profile_url:
        raise ValueError("The LinkedIn profile URL is not valid")

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary of the person
        2. the interesting facts about the person
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

    chain = LLMChain(prompt=summary_prompt_template, llm=llm)

    output = chain.invoke({
        "information": linkedin_data
    })

    print(output['text'])

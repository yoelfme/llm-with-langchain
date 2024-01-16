from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from thidparties.linkedin import scrape_linkedin_profile

information = """
    Elon Musk is a business magnate, industrial designer, and engineer. He is the founder, CEO, CTO, and chief designer of SpaceX; early investor, CEO, and product architect of Tesla, Inc.; founder of The Boring Company; co-founder of Neuralink; and co-founder and initial co-chairman of OpenAI. A centibillionaire, Musk is one of the richest people in the world.
"""

if __name__ == "__main__":
    print("Icebreaker is running...")

    linkedin_data = scrape_linkedin_profile("https://www.linkedin.com/in/elonmusk/")

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

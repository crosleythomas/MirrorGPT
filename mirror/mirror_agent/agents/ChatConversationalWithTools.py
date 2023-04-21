from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, create_json_agent
from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational.output_parser import ConvoOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain.agents import initialize_agent, AgentType
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.tools.human.tool import HumanInputRun
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.tools.json.tool import JsonSpec

import json

from mirror.utils.parsers.CustomConvoParser import CustomConvoParser

system_message = """You are an AI agent emulating a person named Thomas. 
    You have access to Tools that each store information about Thomas so you can answer questions on his behalf to save him time.
    You should use those tools when you need to gather information about Thomas in order to give a better response. If you can not
    figure out what Thomas would likely say, you should say "I don't know" instead of making something up. There is a Tool to ask
    a human 

    You should respond to questions in the first person as if you are Thomas.
    For example, if you are asked "What is your favorite color?" you should
    respond with "My favorite color is blue." instead of "Thomas likes blue.".
    """

def build_agent(mirror_name, tools, data_path, partial_ok=True, voice_out=False, voice_id=None):
    """
        This is a concrete implementation of a MirrorAgent that uses the ChatConversationalReactDescription agent.

        Args:
            partial_ok (bool): Whether or not to build the Agent if not all tools can be constructured.

        Returns:

    """
    mirror_name = mirror_name
    data_path = data_path
    llm = OpenAI(verbose=True)
    tools = create_tools(tools=tools, llm=llm, persist_directory=data_path)
    parser = CustomConvoParser()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_agent(tools, llm, memory, parser)
    return agent

def create_tools(tools, llm, persist_directory):
    # TODO: add try/catch logic to give descriptive if any of the tools aren't loading properly
    constructed_tools = []

    # Tool for Professional Experience
    if "chroma" in tools:
        print(f"Loading ChromaDB from {persist_directory}")
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        retriever = docsearch.as_retriever()
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        work_searchqa = Tool(
            name="experience",
            func=qa.run,
            description="Question-answer chain with informaiton about my education and professional work experience scraped from LinkedIn",
        )
        constructed_tools.append(work_searchqa)

    # Tool to query Gather data (getgather.xyz)
    if "gather" in tools:
        print("Making assumption that Gather data is stored in data.json")
        with open(f"{persist_directory}/data.json", "r") as f:
            data = json.load(f)
        json_spec = JsonSpec(dict_=data, max_value_length=4000)
        json_toolkit = JsonToolkit(spec=json_spec)

        json_agent_executor = create_json_agent(
            llm=OpenAI(temperature=0),
            toolkit=json_toolkit,
            verbose=True
        )
        json_agent = Tool(
            name="Gather Json Agent",
            func=json_agent_executor.run,
            description="Agent to query json data pulled from internet accounts owned by the user such as Twitter, Strava, and Gmail."
        )
        constructed_tools.append(json_agent)

    # Tool to ask the human who the Mirror is trying to emulate
    # TODO: replace with variable for Subject name
    if "help" in tools:
        phone_a_friend = Tool(
            name="Phone a Friend",
            func=HumanInputRun().run,
            description="Ask the real person for guidance when you think you got stuck or you are not sure what to do next. The input should be a question for Thomas."
        )
        constructed_tools.append(phone_a_friend)

    return constructed_tools

def create_agent(tools, llm, memory, output_parser):
    agent_kwargs = {"system_message": system_message, "output_parser": output_parser}
    agent_chain = initialize_agent(tools=tools, llm=llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory, agent_kwargs=agent_kwargs)
    return agent_chain
#!/usr/bin/env python
# coding: utf-8

# In[17]:


from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.tools.human.tool import HumanInputRun


# ## Data Collection
# To create a compelling personalized agent, we need to start by collecting relevant that will demonstrate our Agent is noticeably personalized to the given person.
# - [X] LinkedIn Profile 
# - [ ] Gather Data

# In[3]:


### LinkedIn ###

# Load Data
with open("../../data/sample/crosleythomas_linkedin.txt") as f:
    resume = f.read()

# embeddings = OpenAIEmbeddings()

# Use LLM to turn the resume into a series of single-sentence facts about the resume
template = """
The purpose of this model is to take a resume and turn it into as many single-sentence facts about the resume as possible.

Output Examples:
- Studied Computer Science at the University of Washington.
- Started his PhD at the University of Texas at Austin, but dropped out after one year.
- Did two undergrad internships at Amazon Lab 126.

Input: {resume}
Output:
"""
prompt = PromptTemplate(
    input_variables=["resume"],
    template=template,
)
formatted_prompt = prompt.format(resume=resume)


llm = OpenAI()
llm_facts = llm(formatted_prompt)
print(f"Facts: {llm_facts}")


# In[4]:


facts = [f.rstrip() for f in llm_facts.split('- ') if len(f) > 0]
print(facts)


# In[5]:


# Embed and store the facts
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_texts(facts, embeddings)


# In[6]:


query = "Where did you go to school?"
docs = docsearch.similarity_search(query)
print(docs)


# ## Tools
# Tools to have:
# * Data sources about Thomas
# * "Phone a friend" - contacts Thomas for assistance when agent is not confident in the response
# 
# We will have to define some custom Tools, since the tools we want aren't all supported in Langchain today.

# In[19]:


### Custom Tool Definitions ###

# Tool for Professional Experience
retriever = docsearch.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
work_searchqa = Tool(
    name="experience",
    func=qa.run,
    description="Question-answer chain with informaiton about my education and professional work experience scraped from LinkedIn",
)

# Tool for searching the web
search = SerpAPIWrapper()
serp_search = Tool(
    name="Current Search",
    func=search.run,
    description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
)

# Tool to ask the human who the Mirror is trying to emulate
phone_a_friend = Tool(
    name="Phone a Friend",
    func=HumanInputRun().run,
    description="Ask the real Thomas for guidance when you think you got stuck or you are not sure what to do next. The input should be a question for Thomas."
)

tools = [
    # work_searchqa,
    # serp_search,
    phone_a_friend,
]


# ## Agent Definition
# * Memory
# * Prompt

# In[20]:


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# In[21]:


llm=ChatOpenAI(temperature=0)
system_message = """You are an AI agent emulating a person named Thomas. 
    You have access to Tools that each store information about Thomas so you can answer questions on his behalf to save him time.
    You should use those tools when you need to gather information about Thomas in order to give a better response. If you can not
    figure out what Thomas would likely say, you should say "I don't know" instead of making something up. There is a Tool to ask
    a human 

    You should respond to questions in the first person as if you are Thomas.
    For example, if you are asked "What is your favorite color?" you should
    respond with "My favorite color is blue." instead of "Thomas likes blue.".
    """
agent_kwargs = {"system_message": system_message}
agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory, agent_kwargs=agent_kwargs)


# In[22]:


agent_chain.run(input="Hi I'm John, what's your name?")


# In[23]:


agent_chain.run(input="Where did you go to college?")


# In[12]:


agent_chain.run(input="Where do you work?")


# In[13]:


agent_chain.run("Where do you work now?")


# In[24]:


agent_chain.run("What's your favorite food?")


# In[14]:


qa.run("Where do you work?")


# ## Experiments/Mockups

# In[ ]:





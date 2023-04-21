"""
InterviewAgent is a langchain agent that interacts conversationally with a Subject
to learn about them. It has access to one tool, a data store, which it uses to
store the information it learns about the Subject.

Need:
- Prompt to start conversation, use tools, create facts
- Set up data store(s) as Tool
- Write full conversation history to data store
- Write facts to data store
"""
import langchain

class InterviewAgent(object):
    def __init__(self, agent, mirror_name, topic):
        return None
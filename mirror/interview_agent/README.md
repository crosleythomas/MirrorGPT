# Interview Agent

This directory contains code for the "Interview Agent" (IA) - a conversational agent whose role is to have a conversation with the Subject and learn facts about them that can be used by the Mirror Agent later on.

The IA has 3 functions:
1. **Asking useful questions** - e.g. "What is your favorite food?"
2. [Future] **Using tools to gather information** - e.g. after asking "Do you use Spotify?" the agent could query your Spotify account to get data that expresses your music tastes
3. **Formatting and Storing Data** - there are many ways to store the interview conversation and facts about a person. We should support and test different methods to do this that optimize for how the Mirror Agent will want to query the data later.

The Agent goes through the following chain:
1. Start conversation with explanation of what it is doing
2. Given chat history and topic, decide whether it should (1) look up information from data store (2) Ask a question (3) write information to data store, (4) Respond

## Sample Conversation

```
$ python3 teach_mirror.py <args>

Hi, I'm an interview agent responsible for learning about you. It looks like you want to talk about Food today. I see I don't have very much information stored about you on this topic yet, so let's start with some of the basics?

Question: Do you have any dietary restrictions?
Answer: I'm gluten-free and lactose intolerant

Got it - I'm adding the following facts to the knowledge base:
- is gluten-free
- is lactose intolerant

Question: What are your favorite 3 fruits?
Answer: raspberries, strawberries, blackberries

Got it - I'm adding the following facts to the knowledge base:
- favorite fruit is raspberries
- likes strawberries
- likes blackberries
- likes raspberries more than strawberries
- likes strawberries more than blackberries

...
```
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv


load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ", state["messages"])
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

agent = graph.compile()

conversations_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversations_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversations_history})
    conversations_history = result['messages']
    user_input = input("Enter: ")

with open("logging.txt", 'w') as file:
    file.write("your Conversation Log:\n")

    for message in conversations_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}")

    file.write("End of Conversation")
import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

class AgentState(TypedDict):
    messages: List[HumanMessage]

# 2. Thay đổi khởi tạo Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

print("Bot đã sẵn sàng (Gõ 'exit' để thoát)")
user_input = input("Enter: ")

while user_input != "exit":
    # Gọi agent
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
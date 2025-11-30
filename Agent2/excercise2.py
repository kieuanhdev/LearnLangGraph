import math
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END



class agentState(TypedDict):
    name: str
    values: List[int]
    operation: str
    result: str

def greeting_node(state: agentState) -> agentState:
    if state["operation"] == "+":
        state["result"] = f"Hi {state['name']}, your answer is: {sum(state['values'])}"
    elif state["operation"] == "*":
        state["result"] = f"Hi {state['name']}, your answer is: {math.prod(state['values'])}"
    else:
        state["result"] = "Invalid!"

    return state

graph = StateGraph(agentState)

graph.add_node(greeting_node)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", END)

app = graph.compile()

answer = app.invoke({"name": "kieuanhdev", "values": [1,2,3,4], "operation": "*"})

print(answer)

print(answer['result'])
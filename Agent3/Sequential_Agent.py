from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state: AgentState) -> AgentState:
    state['final'] = f"hi {state['name']} !"
    return state

def second_node(state: AgentState) -> AgentState:
    state['final'] += f"You are {state["age"]} years old!"
    return state

graph = StateGraph(AgentState)
graph.add_node(first_node)
graph.add_node(second_node)

graph.add_edge(START, "first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", END)

app = graph.compile()

print(app.get_graph().draw_ascii())

result = app.invoke({"name": "kieuanhdev", "age": 22})

print(result)
print(result["final"])
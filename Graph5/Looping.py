from typing import List, TypedDict
import random
from langgraph.graph import StateGraph, END, START

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    state["name"] = f"Hi there, {state['name']}"
    state['counter'] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    state["number"].append(random.randint(0,10))
    state["counter"] += 1
    return state

def should_continue(state: AgentState):
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"
    else:
        return "exit"


graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",     # Source node
    should_continue, # Action
    {
        "loop": "random",
        "exit": END
    }
)


app = graph.compile()

# print(app.get_graph().draw_ascii())
# Instead of draw_ascii()
# print(app.get_graph().draw_mermaid())

print(app.invoke({"name":"Vaibhav", "number":[], "counter":-100}))
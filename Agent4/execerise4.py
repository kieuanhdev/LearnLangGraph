from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number1: int
    operator: str
    number2: int
    number3: int
    operator2: str
    number4: int
    finalNumber1: int
    finalNumber2: int

def add_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = state["number1"] + state["number2"]
    return state

def subtract_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = state["number1"] - state["number2"]
    return state

def router(state: AgentState):
    if(state["operator"] == "+"):
        return "addition_operation"
    elif(state['operator'] == "-"):
        return "subtraction_operation"

def add_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = state["number3"] + state["number4"]
    return state

def subtract_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = state["number3"] - state["number4"]
    return state

def router2(state: AgentState):
    if(state["operator2"] == "+"):
        return "addition_operation2"
    elif(state['operator2'] == "-"):
        return "subtraction_operation2"

graph = StateGraph(AgentState)
graph.add_node("add_node", add_node)
graph.add_node("subtract_node", subtract_node)
graph.add_node("add_node2", add_node2)
graph.add_node("subtract_node2", subtract_node2)

graph.add_node("router", lambda state:state)
graph.add_node("router2", lambda state:state)



graph.add_edge(START, "router")

graph.add_conditional_edges(
        "router",
        router,
        {
            "addition_operation": "add_node",
            "subtraction_operation": "subtract_node"
        }
)

graph.add_edge("add_node", "router2")
graph.add_edge("subtract_node", "router2")

graph.add_conditional_edges(
        "router2",
        router2,
        {
            "addition_operation2": "add_node2",
            "subtraction_operation2": "subtract_node2"
        }
)

graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)


app = graph.compile()

print(app.get_graph().draw_ascii())


initial_state = AgentState(number1=10, operator="-", number2=5, number3=7, operator2="+", number4=2, finalNumber1=0, finalNumber2=0)

result = app.invoke(initial_state)
print(result)


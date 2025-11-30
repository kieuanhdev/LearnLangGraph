from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    age: str
    skills: List[str]
    final: str

def first_node(state: AgentState) -> AgentState:
    state['final'] = f"{state['name']}, welcome to the system! "
    return state

def second_node(state: AgentState) -> AgentState:
    state['final'] += f"You are {state['age']} years old! "
    return state

def third_node(state: AgentState) -> AgentState:
    state['final'] += f"You have skills in : {", ".join(state['skills']) }"
    return state

graph = StateGraph(AgentState)
graph.add_node(first_node)
graph.add_node(second_node)
graph.add_node(third_node)


graph.add_edge(START, "first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.add_edge("third_node", END)

app = graph.compile()

print(app.get_graph().draw_ascii())

result = app.invoke({"name": "kieuanhdev", "age": "22", "skills": ["c++", "c", "java", "python"]})
print(result)


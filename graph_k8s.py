import json
from typing import Literal, Union

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.globals import set_verbose

from agents.engineer import get_k8s_engineer
from agents.expert import get_k8s_expert
from state_k8s import K8sState
from agents.k8s_tools import k8s_tool_node

set_verbose(True)

def get_graph():
    graph_builder = StateGraph(K8sState)
    graph_builder.add_node("k8s_expert", get_k8s_expert)
    graph_builder.add_node("k8s_engineer", get_k8s_engineer)
    graph_builder.add_node("k8s_tool_node", k8s_tool_node)
    graph_builder.add_edge(START, "k8s_expert")
    graph_builder.add_edge("k8s_expert", "k8s_engineer")
    graph_builder.add_edge("k8s_engineer", "k8s_tool_node")
    graph_builder.add_edge("k8s_tool_node", END)
    
    memory = MemorySaver()

    return graph_builder.compile(checkpointer=memory)


def run(question: Union[str, None]):
    graph = get_graph()
    thread: RunnableConfig = {"configurable": {"thread_id": "default"}}
    if question == None:
        question = input("Enter request: ")

    for event in graph.stream({"messages": [question]}, thread):
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)

    return graph.get_state(thread).values["messages"][-1].content

if __name__ == "__main__":
    run(None)
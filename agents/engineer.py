from langchain_core.messages import SystemMessage

from agents.k8s_tools import k8s_tools
from helpers import get_model
from state_k8s import K8sState

system_message = SystemMessage(
        """You are a helpful AI Assistant who calls the right function to complete the task
        Carefully identify the final parameters to be used to call the function. Pay attention to each message in the conversation.
        """
    )

def get_k8s_engineer(state: K8sState):
    model = get_model().bind_tools(k8s_tools)
    messages = [system_message] + state["messages"]

    return {"messages": [model.invoke(messages)]}

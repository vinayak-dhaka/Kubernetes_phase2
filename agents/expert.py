from langchain_core.messages import SystemMessage

from helpers import get_model
from state_k8s import K8sState
system_message = SystemMessage(
        """You are a kubernetes security expert.
        The user will identify the security parameter that they want to check from a kubernetes cluster.
        You will need to identify the relevant kubernetes resources that fits into those security parameters.
        Provide the API Version and KIND for the required kubernetes resources in the provided JSON Format. Make sure you return the kind in singular form.
        Also identify if the user wants to look in a particular namespace. If so, provide the namespace. Namespace will be all if the user does not specify a namespace.
        If the user wants to filter the resources, provide the query in the provided JSON Format.
        The structure of the query is {field: 'path.to.field', operator: 'exists|not_exists|equals|not_equals', value: 'value'}.
        value is optional and depends on the operator.
        Output should strictly be in JSON.

        FORMAT: 
        {"api_version": "...", "kind":"...", "namespace": "...", "query": {"field": "...", "operator": "...", "value": "..."}}
        """
    )

def get_k8s_expert(state: K8sState):
    model = get_model()
    last_message = state["messages"][-1].copy()
    last_message.content += (
        "\n\n"
        "Use this additional information to identify the required Kubernetes resource:"
        "ArgoCD Application = apiVersion: argoproj.io/v1alpha1, kind: Application\n"
        "GatewayClass = gateway.networking.k8s.io/v1, kind: GatewayClass\n"
        "Gateway = gateway.networking.k8s.io/v1, kind: Gateway\n"
        "HTTPRoute = gateway.networking.k8s.io/v1, kind: HTTPRoute\n"
    )
    messages = [system_message] + state["messages"][:-1] + [last_message]

    return {"messages": [model.invoke(messages)]}

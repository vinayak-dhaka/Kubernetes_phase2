from typing import Dict, Any, Optional, Annotated
from yaml import safe_dump
from kubernetes import config, dynamic
from kubernetes.client import api_client
from kubernetes.dynamic.exceptions import ResourceNotFoundError
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

client = dynamic.DynamicClient(
    api_client.ApiClient(configuration=config.load_kube_config())
)

def get_resources(
    api_version: str,
    kind: str,
    namespace: str,
    query: Optional[Dict[str, Any]] = None
) -> str:
    """
    Get Kubernetes resources with flexible querying capability.
    
    Args:
        api_version: API version of the resource
        kind: Resource kind
        namespace: Namespace ("all" for all namespaces)
        query: Query dict with structure:
            {
                "field": "path.to.field",  # Use [*] for array items
                "operator": "exists|not_exists|equals|not_equals",
                "value": Any  # Optional, used for comparison operators
            }
    """
    try:
        api = client.resources.get(api_version=api_version, kind=kind)
        klist = api.get(namespace=namespace if namespace != "all" else None)
        resources = []

        for item in klist.items:
            if query and not _evaluate_resource(item.to_dict(), query):
                continue
            
            resources.append({
                "namespace": item.metadata.namespace,
                "name": item.metadata.name,
                # "resource": item.to_dict()
            })

        return safe_dump(resources)

    except Exception as e:
        return safe_dump({"error": str(e)})

def _evaluate_resource(resource: Dict[str, Any], query: Dict[str, Any]) -> bool:
    """Evaluate if a resource matches the query."""
    try:
        field_path = query['field'].split('.')
        value = _get_field_value(resource, field_path)
        
        operator = query['operator']
        if operator == 'exists':
            return value is not None
        elif operator == 'not_exists':
            return value is None
        elif operator == 'equals':
            return value == query.get('value')
        elif operator == 'not_equals':
            return value != query.get('value')
        else:
            return False
    except Exception:
        return False

def _get_field_value(data: Dict[str, Any], path: list) -> Any:
    """Get value from nested dictionary using path list."""
    current = data
    
    for part in path:
        if '[*]' in part:
            # Handle array wildcards
            base_part = part.replace('[*]', '')
            if isinstance(current, list):
                return [_get_field_value(item, [base_part]) for item in current]
            elif isinstance(current, dict):
                if base_part in current:
                    return _get_field_value(current[base_part], [])
        else:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
                
        if current is None:
            return None
            
    return current

@tool
def get_resources_tool(
    api_version: Annotated[str, "The api version is the group along with the version that defines the resource"],
    kind: Annotated[str, "The kind is the type of resource you want to fetch"],
    namespace: Annotated[str, "The namespace the resource is in"],
    query: Annotated[Optional[Dict[str, Any]], "The query is a dictionary of field, operator, and value to filter the resources based on the type of filters. The structure of the query is {field: 'path.to.field', operator: 'exists|not_exists|equals|not_equals', value: 'value'}. The field is the path to the field in the resource, the operator is the type of filter, and the value is the value to filter the resource by"] = None
):
    "Get list of resources from the provided api version, kind, namespace, and query"
    return get_resources(api_version, kind, namespace, query)


k8s_tools = [get_resources_tool]

k8s_tool_node = ToolNode(k8s_tools)
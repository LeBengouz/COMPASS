import networkx as nx

from src.models import PrerequisiteMap



TARGET_ID = "__TARGET__"


def build_prerequisite_graph(prerequisite_map: PrerequisiteMap) -> nx.DiGraph:
    graph = nx.DiGraph()

    concept_names = {prerequisite.concept for prerequisite in prerequisite_map.prerequisites}

    for prerequisite in prerequisite_map.prerequisites:
        graph.add_node(prerequisite.concept, node_type="prerequisite", data=prerequisite)

    for prerequisite in prerequisite_map.prerequisites:
        for dependency in prerequisite.depends_on:

            # error of LLM : depend on not defined concept
            if dependency not in concept_names:
                raise ValueError(f"Unknown dependency: {dependency}")

            graph.add_edge(dependency, prerequisite.concept)

    terminal_concepts = [
        prerequisite.concept 
        for prerequisite in prerequisite_map.prerequisites 
        if graph.out_degree(
            prerequisite.concept
        ) == 0
    ]

    graph.add_node(TARGET_ID, node_type="target", label=prerequisite_map.target)

    #  Enfin connecter a la target
    for concept in terminal_concepts:
        graph.add_edge(concept, TARGET_ID)

    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("The built graph contains a cycle.")

    return graph


def validate_graph(graph):
    """
    Verify if the graph is oriented, if a cycle is detected, returns False.
    """
    return nx.is_directed_acyclic_graph(graph)


def graph_to_dot(graph, target_text):

    lines = [
        "digraph G {",
        'rankdir="TB";',
        'graph [pad="0.5", nodesep="0.6", ranksep="0.8"];',
        'node [fontname="Arial"];',
        'edge [fontname="Arial"];',
    ]

    for node in graph.nodes:
        if node == TARGET_ID:
            label = target_text.replace(
                '"',
                '\\"'
            )

            lines.append(
                f'"{TARGET_ID}" '
                f'[label="{label}", '
                f'shape="box", '
                f'style="rounded,bold"];'
            )

        else:
            label = node.replace(
                '"',
                '\\"'
            )
            lines.append(
                f'"{node}" '
                f'[label="{label}", '
                f'shape="box", '
                f'style="rounded"];'
            )

    for source, destination in graph.edges:
        lines.append(f'"{source}" -> "{destination}";')

    lines.append("}")

    return "\n".join(lines)
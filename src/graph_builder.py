import networkx as nx
import textwrap
from graphviz import Source
from io import BytesIO

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


def wrap_label(text: str, width: int = 28) -> str:
    lines = textwrap.wrap(text, width=width)

    return "\\n".join(lines)


def graph_to_dot(graph, target_text):

    lines = [
        "digraph G {",
        'rankdir="BT";',

        # Global graph spacing
        'graph [pad="0.5", nodesep="0.55", ranksep="0.8", bgcolor="transparent"];',

        # Default node configuration
        'node ['
        'shape="box", '
        'style="rounded,filled", '
        'fontname="Arial", '
        'fontsize="11", '
        'margin="0.18,0.12"'
        '];',

        # Default edge configuration
        'edge ['
        'arrowsize="0.7", '
        'penwidth="1.4"'
        '];',
    ]

    for node, attributes in graph.nodes(data=True):
        if node == TARGET_ID:
            target_label = wrap_label(target_text, width=45)
            target_label = ("TARGET\\n\\n"+ target_label)

            label = target_text.replace(
                '"',
                '\\"'
            )

            lines.append(
                f'"{TARGET_ID}" '
                f'['
                f'label="{target_label}", '
                f'shape="box", '
                f'style="rounded,bold,filled", '
                f'penwidth="2.2", '
                f'margin="0.25,0.18"'
                f'];'
            )

        else:
            prerequisite = attributes.get("data")
            label = wrap_label(node, width=24)


            label = node.replace(
                '"',
                '\\"'
            )

            if (prerequisite and prerequisite.source_type == "inferred"):
                style = ("rounded,dashed,filled")

            else :
                style = ("rounded,filled")


            lines.append(
                f'"{node}" '
                f'['
                f'label="{label}", '
                f'style="{style}"'
                f'];'
            )

    for source, destination in graph.edges:
        lines.append(f'"{source}" -> "{destination}";')

    lines.append("}")

    return "\n".join(lines)



def dot_to_png_bytes(dot):
    # Convert a DOT graph description to PNG bytes.
    source = Source(dot)
    return source.pipe(format="png")
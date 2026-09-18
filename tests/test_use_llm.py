from src.use_llm import generate_prerequisite_map

target_passage = """
An attention function can be described as mapping
a query and a set of key-value pairs to an output.
"""


local_context = """
An attention function can be described as mapping
a query and a set of key-value pairs to an output,
where the query, keys, values, and output are all vectors.
"""


semantic_context = """
We compute the dot products of the query with all keys,
divide each by the square root of the dimension of the
keys, and apply a softmax function.
"""


background = """
Basic linear algebra.
Basic probability.
Classical machine learning.
Little knowledge of deep learning.
"""


result = generate_prerequisite_map(
    target_passage=target_passage,
    local_context=local_context,
    semantic_context=semantic_context,
    background=background,
)


print(result.model_dump_json(indent=2))
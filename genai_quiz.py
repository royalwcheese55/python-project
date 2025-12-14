# 1. fine tuning is that you update the model to perform a specific task, the base model is adjust using specific examples or instruactions.
# RAG is LLM + external search, when you search from RAG model, it retrieve text from an external database and feed them as prompt.
# the knowledge lives in an external tool in RAG rather than tuned in fine tuning model.
# use RAG when building a help bot for a webpage to answer store policies that can update externally
# use fine tuning when you need a specific style like a ai helper.

#2. document(whole file) -> page(1 page) -> block(logical unit on page) -> chucnk(vector tokens you embed)
# heading use to build heading_path, section hierarchy, table use to build structure data. paragraph is the main content.

#3. Fixed-size overlapping vs. structure-aware, fix size is simple but ignore text structure, structure aware is more work but respect logic.
# missing context and hallucinations
# large chunk have better recall but less precision, it cost much and have more latency, small chunk may lose text and info.

#4. {"context": retriever(take user question and retrieve useful info) | format_docs(convert to single string), "question": RunnablePassthrough(forward the message unchanged)()}
#| prompt (prompt templte) prompt
#| llm (model that generate answer). generator 
#| parser (post process llm output). post process

#5. 1. define tool 2. model decide to call tool 3. app execute tool 4. return result to model 5. model generage final answer
# chain: fixed steps, easy to use, you can design the flow. agent: llm decide which tool to use and when to stop.

#6. retrieval relevance/ answer relevance/ grounding
# llm understand semantic searches, check correctness against context, evalutate faithfulness.
# run a batch of question thru system, use llm-as-judge to test retrieval + faithfulness, sample a subset and let human review it.

def make_chunks(blocks, max_token: int = 300, overlap_token: int = 50): 
    chunks = []
    current = []

    for block in blocks: 
        if token_len(current + [block.text]) > max_token:
            chunk.append({"text": join(current)})
            current = last_token(current, overlap)
        current.append(block.text)

    if current:
        chunk.append({"text": join(current)})
    return chunks



from math import sqrt
def embed(text):
    return[len(text) % 7, len(text) % 11]
store = []
docs = [
    {"id": "1", "text": "Router troubleshooting guide."},
    {"id": "2", "text": "How to reset the X200 device."},
]

for doc in docs:
    vec = embed(doc["text"])
    store.append({"id": doc["id"], "vector": vec, "text": doc["text"]})

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm = lambda v: sqrt(sum(x*x for x in v))
    return dot / (norm(a) * norm(b) + 1e-8)

def answer(question):
    q_vec = embed(question)

    ranked = sorted(
        store,
        key = lambda item: cosine(q_vec, item["vector"]),
        reverse = True
    )
    top = ranked[:2]

    context = "\n".join(t["text"] for t in top)

    prompt = f"Use only this context: \n{context}\nA:"
    return llm(prompt)

            






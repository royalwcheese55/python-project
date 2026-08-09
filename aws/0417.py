'''
1. token is a small unit of text or character piece that LLM process.
token reflect actual compute cost better than words. context window is the max number of tokens the model can process at once. in RAG it limits the chunks you can retrieve in a prompt.

2. temp is the randomness. the higher the more random
top-k is pick from top k tokens
top-p is prick from smallest set which probability >= p

a. temp 0-0.3 top-k small top-p 0.8
b. temp = ~1 top=k larger top-p 0.9

3. document ingestion- load raw docs
chuncking  split into smaller pieces
embedding- convert chunks to vectors
indexing- store vectors for retrieval
query embedding- convert user query to vector
retrieval- find top-k similar chunks
generation= send context = query to llm

4. large: more context but lower precision
small: better precision but lose context

naive split cut one sentence in half, 

5. don't know HyDE
(hypothetical document embeddings) it generate fake answer and embed it and retrieve similar docs, good for vague or semantic query

subquery decomposition; break complex query into smaller parts, good for multi-step queries.

6. close: exact correct answer
open: subjective output live summaries

human evaluation: accurate but slow and expensive
llm: scalable and fast

'''


tool = {
    "name": "search_internal_docs",
    "description": (
        "Search internal company documents such as handbooks, tickets, or code. "
        "Use this tool when the user asks about internal policies, past issues, or technical documentation. "
        "Do NOT use it for general knowledge questions."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "User question in natural language"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return (default 5)"
            },
            "doc_type": {
                "type": "string",
                "enum": ["handbook", "ticket", "code"],
                "description": "Optional filter for document type"
            }
        },
        "required": ["query"]
    }
}

from openai import OpenAI

client = OpenAI()


user_query = "What is the company refund policy?"
messages = [{"role": "user", "content": user_query}]


response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=[tool]
)

msg = response.choices[0].message


if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    name = tool_call.function.name
    args = tool_call.function.arguments


    result = run_tool(name, args)


    messages.append(msg)
    messages.append({
        "role": "tool",
        "name": name,
        "content": result
    })

    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    print(final_response.choices[0].message.content)

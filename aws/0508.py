'''
1. query is what token is asking for
key is what each token offers
value is the actual info 

2. chinese cost more token because it has to split chinese into smaller
units so it is higher cost

3. dont know decoder : GPT

4. JSON schema function calling
constrained decoding
prompt only

5. hyDE generate a fake answer - embed - retrieve better context

6. prompt injection: system send api. 
indirect malicious content inside retrieved docs

7. lost in middle, put important info at start or end 

8. dk

9. vector vs BM25, vector is how to reduce latency in distributed system
bm25 is kafka isr definition

10. parent child chunking: store small chunks for retrieval retuan larger
parent context

11. pdf failure: broken tables and wrong text order

12. rrf

13. cross is slower bi is faster 

14. answer_relevancy because compare generated answer vs correct answer

15. eval data too clean - production noisy

16. tools: model invokes
resources: app fetches
prompts: user controls

17. mcp is vertical
a2a is horizontal

18. rug pull attack

19. same pattern: reason act observe

20. termination guards max steps. max cost, timeout, no progress

1. problem = generation
fixes: prompt grounding and better reranking stronger model

reranking my hurt recall

infinite loop tool retry loop bad stop condition
step count tool calls 

if steps > max_steps; break

return partial answer + progress

parallel index blue green
gate: faithfulness + relevancy

b4: mcp agent- tools
a2a agent to agent
async execution


'''

def run_agent(user_msg, max_steps=15, max_cost_usd=0.5):
    messages = [{"role": "user", "content": user_msg}]
    total_cost = 0

    for step in range(max_steps):
        res = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            temperature=0
        )

        msg = res.choices[0].message
        usage = res.usage
        total_cost += usage.prompt_tokens * PRICING[MODEL]["prompt"]
        total_cost += usage.completion_tokens * PRICING[MODEL]["completion"]

        if not msg.tool_calls:
            return msg.content

        messages.append(msg)

        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments)
            except:
                messages.append({
                    "role": "tool",
                    "content": "invalid arguments, please retry"
                })
                continue

            result = tool_fns[tc.function.name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

        if total_cost > max_cost_usd:
            break

    messages.append({
        "role": "user",
        "content": "give best answer based on current info"
    })

    res = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tool_choice="none",
        temperature=0
    )

    return res.choices[0].message.content
def build_rag_chain(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.from_documents(chunks, embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_template("""
Answer ONLY from context.
If unknown, say "I don't have enough information".

Context:
{context}

Question:
{question}
""")

    def format_docs(docs):
        return "\n".join(
            f"{d.page_content} (source: {d.metadata})"
            for d in docs
        )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | ChatOpenAI(model="gpt-4o-mini", temperature=0)
        | StrOutputParser()
    )

    return chain
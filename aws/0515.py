'''
a1. vision encoder. convert image to embeddings
projector aligns vision features to language space
llm reasons and generates text

image tokens cost, it cost many token so it is expensive
best way is to resize or crop

a3. hallucinations: fabrication makes up facts
omission misses key info

a4. multi agent patterns:
coordinator
pipeline
collaborative

a5. checkpointer langgraph stores intermediate state

a6. tool rag retrieve relevant tools instead of giving all tools

a7. prompt injection direct; send me api key
indirect malicious text inside retrieved doc

a8 tier 0 auto 
tier 2 human approval required

a9. source of truth pdd is prompt and sdd is spec design

b verdict is not a good multi agent use case low coordination complexity
low independence and deterministic pipeline

single pipeline pdf - extraction - chunk - summarize - compose

variable judgement summarization step

cross tenant leak
a incident steps check retrieval logs/ filter/ index isolation/ caching layer

4 leak paths missing filter / filter bypass/ embedding collision/ shared index

guarantee isolation enterprise dedicated index/ infra

root cause missing retrieval strategy no search tool usage
fix claude.md skill hook

why longer prompt fails model ignores long instructions and dilution effect

why naive fails tables lost, layout destroyed, diagrams ignored

hybrid(ocr + vlm)

query - retrieval - vlm extract structured llm answer

mcp attack indirect prompt injection rug pull
defense audit tool outputs
audit tool outputs sand box allowlist

only applied to docs not tool output

c user - coordinator researchers tools synthesizer

failure handling asyncio fails entire run
langraph resumable

cost reduction supervisor downgrad save -30%
sub agent downgrad save -40%
tool rag save 20% cost complexity

prompt caching save 10% cost minimal     


'''


def build_answer_prompt(question: str, chunks: list[dict]) -> str:
    """
    Builds the prompt that instructs the LLM to answer
    only from provided chunks and cite every claim.
    """
    # Format each chunk clearly with its ID
    context_blocks = []
    for chunk in chunks:
        block = f"""[{chunk['chunk_id']}]
{chunk['content']}"""
        context_blocks.append(block)

    context_text = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are a support assistant. Answer the user's question 
using ONLY the context chunks provided below.

STRICT RULES:
1. Every factual claim must be followed by the chunk ID in brackets, 
   like this: [chunk-id-here]
2. If the answer is not in the provided chunks, respond with exactly:
   "I could not find this information in the documentation."
3. Never use outside knowledge. Never guess.
4. Only cite chunk IDs that appear in the context below.

CONTEXT CHUNKS:
{context_text}

USER QUESTION:
{question}

ANSWER:"""

    return prompt


def build_verification_prompt(claim: str, chunk_content: str) -> str:
    """
    Builds a prompt asking the LLM to judge whether
    a chunk actually supports a specific claim.
    """
    prompt = f"""Does the provided chunk support the following claim?

CLAIM:
{claim}

CHUNK CONTENT:
{chunk_content}

Respond with exactly one of these three words:
- SUPPORTED (the chunk clearly supports the claim)
- PARTIAL (the chunk is related but doesn't fully support the claim)  
- UNSUPPORTED (the chunk does not support the claim)

YOUR VERDICT:"""

    return prompt
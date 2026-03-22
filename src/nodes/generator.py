from openai import OpenAI

client = OpenAI()


class RAGGenerator:
    def generate(self, query: str, documents: list):
        context = "\n\n".join([doc["text"] for doc in documents])

        prompt = f"""
You are a helpful AI assistant.

Use the provided context to answer the question.

Rules:
- Answer clearly and concisely
- Use the context as primary source
- You may rephrase and summarize
- Do NOT say "I don't know" if context contains relevant info

Context:
{context}

Question:
{query}

Answer:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content
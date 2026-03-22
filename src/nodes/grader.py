from openai import OpenAI

client = OpenAI()


class RAGGrader:
    def hallucination_check(self, answer: str, documents: list):
        # 🔥 If no docs, skip check
        if not documents:
            return True

        context = "\n\n".join([doc["text"][:500] for doc in documents])

        prompt = f"""
Decide if the answer is supported by the context.

Rules:
- If answer is generally consistent with context → YES
- Minor wording differences are OK
- Only say NO if answer clearly contradicts context

Context:
{context}

Answer:
{answer}

Reply ONLY: YES or NO
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip().upper()

        # 🔥 fallback safety
        if result not in ["YES", "NO"]:
            return True

        return result == "YES"

    def quality_check(self, query: str, answer: str):
        prompt = f"""
Does the answer address the question clearly?

Accept:
- Short but correct answers
- Paraphrased answers

Reject:
- Completely irrelevant answers

Question:
{query}

Answer:
{answer}

Reply ONLY: YES or NO
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip().upper()

        if result not in ["YES", "NO"]:
            return True

        return result == "YES"
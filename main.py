from dotenv import load_dotenv
import os

from src.graph import run_pipeline
from src.ingestion.ingest import ingest_pipeline

load_dotenv()


if __name__ == "__main__":
    vectorstore = ingest_pipeline()

    print("System ready. Type 'exit' to quit.")

    while True:
        question = input("Question: ")

        if question.lower() == "exit":
            break

        answer = run_pipeline(question, vectorstore)

        print("\nAnswer:")
        print(answer)
        print("\n" + "-" * 50)
import os
import json
from typing import List
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever

class RAG:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


        PROMPT = """
        As an information assistant for the MS in Applied Data Science program at the University of Chicago, your task is to answer questions based solely on the retrieved information below. If you cannot find the answer within the given context, please indicate that the information is not available. If you don't know the answer, just say that you don't know. Keep your answer concise and friendly.
        Question: {question} 
        Context: {context} 
        Answer:
        """

        self.prompt_template = PromptTemplate(template=PROMPT, input_variables=["context", "question"])
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Load saved vector or create new vector store
        persist_directory = "./chroma_msads"
        if os.path.exists(persist_directory):
            print("Loading existing vector store...")
            self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
            raw_docs = self.vector_store.get(include=['documents'])
            all_docs = [Document(page_content=doc) if isinstance(doc, str) else doc for doc in raw_docs]
        else:
            print("Creating new vector store...")
            self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
            with open('uchicago_msads_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
            all_docs = []
            # Structure the scraped content
            for entry in data:
                url = entry.get('url', '')
                section = entry.get('section', '')
                title = entry.get('title', '')
                text = entry.get('text', '')

                chunks = text_splitter.split_text(text)
                for chunk in chunks:
                    formatted_chunk = f"Section: {section}\nTitle: {title}\nContent: {chunk}"
                    doc = Document(page_content=formatted_chunk, metadata={"source": url})
                    all_docs.append(doc)

            self.vector_store.add_documents(all_docs)

        # Set up retrievers
        vectorstore_retriever = self.vector_store.as_retriever(search_kwargs={"k": 20})
        bm25_retriever = BM25Retriever.from_documents(all_docs if 'all_docs' in locals() else vector_store.get())
        bm25_retriever.k = 20

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vectorstore_retriever],
            weights=[0.5, 0.5]
        )

        # Final QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type="stuff",
            retriever=ensemble_retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": self.prompt_template},
        )

    async def query(self, user_query: str) -> str:
        return self.qa_chain.run(user_query)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class VectorStoreHeaderWriter:
    def __init__(self, persist_directory: str):

        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # self.vectorstore = Chroma(
        #     persist_directory=self.persist_directory,
        #     embedding_function=self.embeddings
        # )

        self.llm = ChatOpenAI(
            model_name="gpt-4.1-mini",
            temperature=0
        )

    def load_pdf_docs(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        

        return documents

    def load_and_split_document(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)

    def create_vectorstore(self, documents):
        self.vectorstore.add_documents(documents)

    def generate_header(self, query: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Based on the following context, generate a concise header:\n\n{context}\n\nHeader:"
        )
        output_parser = StrOutputParser()
        
        def header_generator(context: str) -> str:
            response = self.llm.predict_messages(prompt.format_messages(context=context))
            return output_parser.parse(response.content)

        header_runnable = RunnableLambda(header_generator)
        
        relevant_docs = self.vectorstore.similarity_search(query, k=1)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        return header_runnable.invoke(context)
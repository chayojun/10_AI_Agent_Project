from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

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

    def load_pdf_docs(self, file_path: str) -> str:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        full_text = ""
        
        for i in range(len(documents)):
            text = documents[i].page_content
            # Clean up excessive newlines and spaces
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'\s{2,}', ' ', text)
            documents[i].page_content = text
            full_text += text + "\n"

        return full_text

    def transfer_full_text_to_metadata(self, full_text: str):
        prompt = """
        당신은 정책 요약 전문가입니다.
        주어진 정책 문서의 전체 내용을 바탕으로 format에 맞게 json 형식으로 메타데이터를 작성하세요.

        <format>
        JSON
        {
            "policy_id": "정책의 이름",
            "summary": "정책의 수혜"
        }
        """

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
        
        return header_runble.invoke(context)
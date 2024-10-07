import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv()

# LangSmith logging setup (optional)
from langchain_teddynote import logging
logging.langsmith("Markdown File With Graph")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Markdown File With Graph"
os.environ["LANGCHAIN_API_KEY"] = "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"

# Step 1: Load Markdown Documents
docs = []
for filename in os.listdir("parsed_pages4"):
    if filename.endswith(".md"):
        try:
            loader = TextLoader(os.path.join("parsed_pages4", filename), encoding='utf-8')
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading file {filename}: {e}")

# Step 2: Split Documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# Step 3: Create Embeddings
embeddings = OpenAIEmbeddings()

# Step 4: Create and Save Vector Database
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# Step 5: Create Retriever
retriever = vectorstore.as_retriever()

# Step 6: Create Prompt
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know.

#Context: 
{context}

#Question:
{question}

#Answer:"""
)

# Step 7: Create Language Model
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Step 8: Create Chain
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Run Chain
question = "which location has the highest cargo export differential to HSFO in the upper range?"
response = chain.invoke(question)
print(response)
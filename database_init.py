from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4

def run():
    # load the env file
    from dotenv import load_dotenv
    load_dotenv()

    DATA_PATH = r"data"
    CHROMA_PATH = r"chroma_db"

    # the model
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

    # init chroma store
    vector_store = Chroma(
        collection_name="website_data",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )

    # load whatever .md docs are in "data"
    loader = DirectoryLoader(DATA_PATH, glob="*.md")

    raw_documents = loader.load()

    # splitting the document
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=120,
        length_function=len,
        is_separator_regex=False
    )

    # create chunks from the data document
    chunks = text_splitter.split_documents(raw_documents)

    # create ids for each of the chunks
    uuids = [str(uuid4()) for i in range(len(chunks))]

    # add all the chunks to the chroma vector store
    vector_store.add_documents(documents=chunks, ids=uuids)

    return True
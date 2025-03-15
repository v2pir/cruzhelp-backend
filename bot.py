from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import gradio as gr

# load the env file
from dotenv import load_dotenv
load_dotenv()

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# load the model
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

# initialize the model
llm = ChatOpenAI(temperature=0.5, model='gpt-4o-mini')

# connect to the vector store
vector_store = Chroma(
    collection_name="website_data",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH, 
)

# make the vector store the retriever
num_results = 5
retriever = vector_store.as_retriever(search_kwargs={'k': num_results})

def stream(message, history):

    # get the correct chunks
    docs = retriever.invoke(message)

    # add all the chunks to "knowledge"
    previous_information = ""

    for doc in docs:
        previous_information += doc.page_content+"\n\n"


    # this is the prompt for the llm, making it remember the previous conversations
    # stole the prompt from some website works pretty well 
    if message is not None:

        partial_message = ""

        prompt = f"""
        You are an assistent which answers questions based on knowledge which is provided to you.
        While answering, you don't use your internal knowledge, 
        but solely the information in the "The knowledge" section.
        You don't mention anything to the user about the povided knowledge.

        The question: {message}

        Conversation history: {history}

        The knowledge: {previous_information}

        """

        # stream the response to the gradio App
        for response in llm.stream(prompt):
            partial_message += response.content
            yield partial_message

# initialize gradio
chatbot = gr.ChatInterface(stream, textbox=gr.Textbox(placeholder="Send to the LLM...",
    container=False,
    autoscroll=True,
    scale=7),
)

# use gradio
chatbot.launch()
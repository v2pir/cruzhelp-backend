from openai import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import webscraper as web
import database_init as init_vector

def create_database(website):
    web.run(website)
    init_vector.run()

def run(msg):

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

    def get_prompt(message):
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

            system_prompt = f"""
            You are an assistent which answers questions based on knowledge which is provided to you.
            While answering, you don't use your internal knowledge, 
            but solely the information in the "The knowledge" section.
            You don't mention anything to the user about the provided knowledge.

            The question: {message}

            The knowledge: {previous_information}

            """

            return system_prompt


    #print(results['documents'])
    #print(results['metadatas'])

    client = OpenAI()

    #print(system_prompt)

    def get_response(message):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = [
                {"role":"user","content":get_prompt(message)}    
            ]
        )

        return response.choices[0].message.content

    return str(get_response(msg))

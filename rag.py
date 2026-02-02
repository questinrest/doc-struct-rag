from scraping.webscrape import scrape_and_clean
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate



load_dotenv()

"""
s1 - scrape
s2 - chunk
s3 - embed
s4 - match


"""


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

clean_text = scrape_and_clean(url)


splitter = CharacterTextSplitter(
    separator="",
    chunk_size = 100,
    chunk_overlap = 10,
    length_function = len
)

chunks = splitter.split_text(clean_text)

# for i in range(len(chunks)):
#     print(f"Chunk {i}: {chunks[i]}")


## creating an index in Pinecone

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key = PINECONE_API_KEY)

index_name = "enterprise-rag"


# create an index 
if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

dense_index = pc.Index(index_name)

# s4, create embeddings and upload chunks to VDB, two steps are there, iterate through each chunk, create embedding for each chunk
# and then upload it to vector database

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2") # dim = 768


# for i, chunk in enumerate(chunks):
#     chunk_embedding = embeddings.embed_query(chunk)
#     dense_index.upsert(vectors=[{"id" : str(i), "values" : chunk_embedding, "metadata" : {'chunk_text' : chunk}}])



## step 5 : chains


llm = init_chat_model(
    model='llama-3.1-8b-instant',
    model_provider='groq',

)


# print(llm.invoke("Hi Are you Up?").content)


## user asks question logic
def chatbot(query):
    while True:
        #query = "Ask your question (or type exit to stop)")
        if query.lower() == "exit":
            break
        
        ## retriving tp 3 chunks from pinecone
        query_embedding = embeddings.embed_query(query)
        result = dense_index.query(vector=query_embedding, top_k=2, include_metadata=True)

        ## combine top results into a single context string
        augment_context = "\n\n".join([match.metadata['chunk_text'] for match in result.matches])


        #create prompt template

        prompt = PromptTemplate(
            input_variables= ['context', 'question'],
            template= "You are a helpful assistant. Use the context provided to answer the question accurately. Only use this context, not your knowledge. If you dont get relavant context say, I don't know.\n\n"
                        "context:{context}"
                        "question:{question}"
        )

        # chain
        chain = prompt |  llm

        # generate response 
        response = chain.invoke({
            'context' : {augment_context},
            'question' : {query}
        })

        return f"Answer : {response.content}"
        




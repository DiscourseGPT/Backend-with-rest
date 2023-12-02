import os
import logging
import openai
logging.getLogger().setLevel(logging.ERROR)
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, PromptHelper, ServiceContext, load_index_from_storage,StorageContext
from langchain.llms.openai import OpenAI
from langchain.base_language import BaseLanguageModel

def construct_index(directory_path):
    # Set maximum input size
    max_input_size = 4096
    # Set number of output tokens
    num_outputs = 20000
    # Set maximum chunk overlap
    max_chunk_overlap = 20
    # Set chunk size limit
    chunk_size_limit = 600
    # Set chunk size ratio
    chunk_size_ratio = 0.1

    # Define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs,chunk_overlap_ratio=chunk_size_ratio, chunk_size_limit=chunk_size_limit)

    # Define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    # index.save_to_disk('index1.json')
    index.storage_context.persist('') 

    return index

def ask_ai(query):
    # index = GPTVectorStoreIndex.load_from_disk('index1.json')
    # index = GPTVectorStoreIndex.from_vector_store(vector_store=)
    storage_context = StorageContext.from_defaults(persist_dir='')
    index = load_index_from_storage(storage_context)
    # index = GPTVectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    while True:
        query = query
        response = query_engine.query(query)
        return response

os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.environ["OPENAI_API_KEY"]
construct_index("context_data/data")

# Imports for processing
from config import INDEX_DIR,DATA_DIR,CHROMA_COLLECTION_NAME,INDEX_DIR as KEYWORD_INDEX_DIR
from data_loader import load_and_chunk_documents
from keyword_store import(
    create_index as create_keyword,
    open_index as open_keyword,
    add_documents as add_keyword
    )
from vector_store import(
    get_chroma_collection as get_vector_collection,
    add_documents as add_vector,
    clear_collection
)
from hybrid_retriever import hybrid_search
from llm_interface import generate

import os
import shutil

# For logging
import logging
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# To create prompt
def create_prompt(query:str,context_chunks:list[dict])->str:
    chunk_texts=[chunk.get('document','') for chunk in context_chunks]
    separator = "\n\n---\n\n"
    context_string=separator.join(chunk_texts)
    prompt = f"""
You are a helpful assistant that answers questions using only the provided context document.

Context Document:
<context>
{context_string}
</context>

The query is {query}

Respond Based on the provided context document, """
    return prompt.strip()


# To hold the vector collection handle
vector_collection_handle=None


# Initilize rag and if checks if there is a need to create a new index for both vector and keyword serach
def initialize_rag(force_reindex:bool=False):
    global vector_collection_handle
    logger.info(f"Initializing RAG(Force Re-Index: {force_reindex})")
    vector_collection=get_vector_collection(CHROMA_COLLECTION_NAME)
    vector_count=vector_collection.count()
    logger.info(f"There are {vector_count} vectors in {CHROMA_COLLECTION_NAME}")

    # To check if keyword store exists
    keyword_index_exists_and_populated = (
        os.path.exists(KEYWORD_INDEX_DIR) and
        len(os.listdir(KEYWORD_INDEX_DIR)) > 0 # Check if directory has files/subdirs
    )
    if keyword_index_exists_and_populated:
        logger.info(f"Keyword store directory found at: {KEYWORD_INDEX_DIR}")
    else:
        logger.info(f"Keyword store directory not found at: {KEYWORD_INDEX_DIR}")

    vector_needs_indexing=False
    keyword_needs_indexing=False
    # For vector store resetting
    if force_reindex :
        logger.warning("Force re-index requested.")
        if vector_count>0:
            logger.info(f"Clearing existing vector store: {CHROMA_COLLECTION_NAME}")
            clear_collection(CHROMA_COLLECTION_NAME)
            vector_count=0
        else:
            logger.info("Vector store already empty or non-existent, no need to clear.")
        vector_needs_indexing=True
        if keyword_index_exists_and_populated:
             logger.info(f"Clearing existing keyword store: {KEYWORD_INDEX_DIR}")
             try:
                 shutil.rmtree(KEYWORD_INDEX_DIR)
                 logger.info(f"Removed keyword index directory: {KEYWORD_INDEX_DIR}")
             except OSError as e:
                 logger.error(f"Error removing keyword index directory {KEYWORD_INDEX_DIR}: {e}. Proceeding with re-index attempt.", exc_info=True)
        else:
             logger.info("Keyword store directory already empty or non-existent, no need to clear.")
        keyword_needs_indexing=True
    else:
        if vector_count == 0:
            logger.info("Vector store is empty. Indexing needed.")
            vector_needs_indexing = True
        # Use the combined check variable here
        if not keyword_index_exists_and_populated:
            logger.info("Keyword store index not found or empty. Indexing needed.")
            keyword_needs_indexing = True
    
    if vector_needs_indexing or keyword_needs_indexing:
        logger.info("Loading and chunking documents from DATA_DIR")
        data=load_and_chunk_documents()
        if data:
            if vector_needs_indexing:
                add_vector(data,vector_collection)
                logger.info("Vectors Added")
            if keyword_needs_indexing:
                if not os.path.exists(KEYWORD_INDEX_DIR):
                    logger.info(f"Creating keyword index directory and schema before adding documents")
                    create_keyword()
                add_keyword(data)
                logger.info("Keywords Added")
        else:
            logger.warning("No Documents found or loaded. Skipping Adding to stores")
    else:
        logger.info("Store is up-to-date")
    
    vector_collection_handle=vector_collection
    logger.info("RAG initialization complete.")


# Main orchestrate to RAG, takes user query as string and provide resutlt using data
def answer_query(query:str)->str:
    if not query:
        logger.warning("Query is Empty. Returning Back to calling function.")
        return "Please provide a query."
    data=hybrid_search(query=query,vector_collection=vector_collection_handle)
    if not data:
        logger.warning("The Hybrid search returned no data. Returning to calling function.")
        return "Sorry, I couldn't find relevant information."
    prompt=create_prompt(query,data)
    response=generate(
        prompt=prompt,
        temperature=0.7,
        top_p=0.7,
        max_tokens=3000
        )
    if response is None:
        logger.error("LLM Generation Failed or returned None")
        return "Sorry, I encountered an error while generating the response."
    logger.info("Recieved Response form LLM")
    return response


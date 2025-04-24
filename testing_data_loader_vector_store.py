# main.py

import logging
import time

# Import functions and config from your modules
from vector_store import initializer, search, get_chroma_collection, clear_collection
from config import CHROMA_COLLECTION_NAME, TOP_K_VECTOR, DEBUG

# --- Basic Logging Setup ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Avoid adding multiple handlers if script is run multiple times in interactive session
if not logger.hasHandlers():
    logger.addHandler(handler)
# --- End Logging Setup ---

def run_query(query: str):
    """
    Initializes the vector store (if needed), runs a query,
    and prints the results.
    """
    start_time = time.time()
    logger.info("--- Starting RAG Test ---")

    # 1. Initialize the Vector Store
    # This loads data from DATA_DIR, chunks it, embeds it,
    # and stores it in ChromaDB.
    # NOTE: The current initializer CLEARS the collection first.
    logger.info(f"Initializing vector store (Collection: {CHROMA_COLLECTION_NAME})...")
    try:
        initializer(CHROMA_COLLECTION_NAME)
        logger.info("Vector store initialization complete.")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}", exc_info=DEBUG)
        return # Stop execution if initialization fails

    # 2. Get the ChromaDB Collection
    # We need the collection object to perform the search
    try:
        collection = get_chroma_collection(CHROMA_COLLECTION_NAME)
    except Exception as e:
        logger.error(f"Failed to get Chroma collection '{CHROMA_COLLECTION_NAME}': {e}", exc_info=DEBUG)
        return

    # 3. Define and Execute the Search Query
    logger.info(f"Executing search query: '{query}'")
    try:
        search_results = search(query=query, top_k=TOP_K_VECTOR, collections=collection)
    except Exception as e:
        logger.error(f"Failed during search execution: {e}", exc_info=DEBUG)
        return

    # 4. Display the Results
    logger.info(f"--- Search Results for query: '{query}' ---")
    if not search_results:
        logger.info("No relevant documents found.")
    else:
        for i, result in enumerate(search_results):
            print(f"\n--- Result {i+1} ---")
            print(f"Score (Distance): {result.get('score', 'N/A'):.4f}") # Lower distance is better
            print(f"Document Chunk: \n{result.get('document', 'N/A')}")
            print(f"Metadata: {result.get('metadata', 'N/A')}")
            print("--------------------")

    end_time = time.time()
    logger.info(f"--- RAG Test Finished ---")
    logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")

    # Optional: Clean up the collection after the test if desired
    # Comment out if you want to keep the index for further queries
    # try:
    #     logger.info(f"Clearing collection: {CHROMA_COLLECTION_NAME}")
    #     clear_collection(CHROMA_COLLECTION_NAME)
    # except Exception as e:
    #     logger.error(f"Error clearing collection: {e}", exc_info=DEBUG)


# --- Main Execution Block ---
if __name__ == "__main__":
    # Ensure the 'data' directory exists and contains your text files
    # Ensure the '.env' file exists if you were relying on it for API keys (though not needed for local embeddings)
    # Ensure all dependencies are installed:
    # pip install chromadb sentence-transformers python-dotenv python-docx PyMuPDF regex

    test_query = "what is machine learning"
    run_query(test_query)
# --- End Main Execution Block ---
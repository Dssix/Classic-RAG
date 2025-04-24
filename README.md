# Classic-RAG

A simple, educational Retrieval-Augmented Generation (RAG) project built in Python. This project demonstrates how to combine vector search and keyword search to retrieve relevant document chunks and use them to enhance an LLM's answer.

This is my first public repository, so I'm learning the ropes! Please feel free to provide feedback and suggestions.

## Features

*   Loads documents from `.txt`, `.pdf`, and `.docx` files in a specified data directory.
*   Chunks and cleans loaded documents.
*   Uses ChromaDB for vector embeddings and similarity search.
*   Uses Whoosh for keyword-based indexing and search.
*   Implements a hybrid retrieval strategy combining vector and keyword results using Reciprocal Rank Fusion (RRF).
*   Interfaces with an OpenAI-compatible API endpoint (specifically configured for `https://models.github.ai/inference`) to generate responses based on retrieved context.
*   Provides a simple command-line interface to interact with the RAG system.

## Project Structure

Here's a brief overview of the files in this repository:

*   `.gitattributes`: Configures Git to handle line endings consistently across different operating systems.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore (like your `.env` file and Python environment).
*   `config.py`: Central configuration file. Loads environment variables, defines paths for data and index storage, sets parameters for chunking, retrievers, and specifies the embedding model and LLM API key variable.
*   `data_loader.py`: Handles loading documents from the `data/` directory, supporting `.txt`, `.pdf`, and `.docx` formats. It also includes text cleaning and chunking logic.
*   `hybrid_retriever.py`: Implements the hybrid search logic. It queries both the vector store (ChromaDB via `vector_store.py`) and the keyword store (Whoosh via `keyword_store.py`), combines their results, and re-ranks them using RRF.
*   `keyword_store.py`: Manages the keyword search index using the Whoosh library. It handles creating, opening, adding documents to, and searching the keyword index.
*   `llm_interface.py`: Provides an interface to interact with the language model API. It uses the `openai` library to send prompts and receive completions, including basic error handling.
*   `main.py`: The entry point of the command-line application. It initializes the RAG pipeline and runs a loop to take user queries and display LLM responses.
*   `rag_pipeline.py`: The main orchestration script. It handles the initialization process (loading data, building indexes if needed), calls the hybrid retriever, constructs the prompt based on retrieved context, and sends the prompt to the LLM interface.
*   `requirements.txt`: Lists all Python dependencies required to run the project.
*   `vector_store.py`: Manages the vector database using ChromaDB. It handles creating/accessing the Chroma collection, embedding document chunks (using `sentence-transformers` as configured), adding documents, and performing vector similarity searches.

## Setup and Installation

Follow these steps to get the project running on your local machine:

1.  **Prerequisites:**
    *   Ensure you have Python (3.8+) and Git installed.
    *   You will need access to an OpenAI-compatible API endpoint. The project is configured to use `https://models.github.ai/inference`, which may require specific authentication related to GitHub's inference services (like Copilot).

2.  **Clone the repository:**
    ```bash
    git clone <URL_OF_YOUR_REPO>
    cd Classic-RAG
    ```
    (Replace `<URL_OF_YOUR_REPO>` with the actual URL of your GitHub repository).

3.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    # On Windows:
    # .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure API Key and Environment Variables:**
    *   Create a file named `.env` in the root directory of the project (the same directory as `config.py`).
    *   Inside `.env`, add your API key for the language model. The project specifically looks for `OPENAI_API_KEY`.
    *   **Important:** The project is configured to use the base URL `https://models.github.ai/inference`. You need to provide a key that is valid for this specific endpoint. If you are using a standard OpenAI API key, you might need to adjust the `base_url` in `llm_interface.py` or `config.py` if you are not using the GitHub inference service.
    *   Your `.env` file should look something like this (replace `your_api_key_here` with your actual key/token):
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
    *   Make sure you *do not* commit your `.env` file to Git. It's already listed in `.gitignore`.

6.  **Add your Documents:**
    *   Create a directory named `data` in the root of the project if it doesn't exist.
    *   Place your `.txt`, `.pdf`, and `.docx` documents that you want the RAG system to query inside this `data/` directory.

## How to Run

Once setup is complete, you can run the main application:

```bash
python main.py
Use code with caution.
Markdown
The first time you run it (or if you modify documents in data/), the system will load, chunk, and index your documents. This might take some time depending on the number and size of your files. You will see logs indicating the progress.
After initialization, you will be prompted to enter a query:
Enter your query (or type 'quit' to exit):
Use code with caution.
Type your question related to the documents you placed in the data/ folder and press Enter. The system will retrieve relevant information and generate a response using the LLM.
Type quit and press Enter to exit the program.
Asking for Review and Feedback
As this is my first public repository, I am eager to learn and improve. Please feel free to review the code, point out potential issues, suggest improvements, or ask questions. You can use GitHub's features like Issues and Pull Requests for this. Your feedback is highly appreciated!
Available on GitHub
This project is available on GitHub! Feel free to fork it, star it, or use it as a reference for your own projects.
---

**Explanation for your review:**

1.  **Title and Description:** I've used "Classic-RAG" as you had it and added a brief description explaining what it does. I explicitly mentioned it's your first repo and that you welcome feedback, right at the beginning.
2.  **Features:** I summarized the key capabilities based on the code files (loading data, chunking, vector/keyword search, hybrid retrieval, LLM interface).
3.  **Project Structure:** I went through each of your files and wrote a *brief* explanation of its role in the overall system. I aimed for clarity without getting bogged down in too much detail.
4.  **Setup and Installation:** This is a crucial section.
    *   I listed the prerequisites (Python, Git, API access).
    *   Gave the standard `git clone` command.
    *   Recommended a virtual environment and provided commands for different OS.
    *   Gave the `pip install` command for dependencies.
    *   **API Key Configuration (`.env`):** This is where I addressed your specific points.
        *   I explained the need for the `.env` file and that `config.py` reads from it.
        *   I mentioned the specific variable name (`OPENAI_API_KEY`) the code expects.
        *   I highlighted the configured base URL (`https://models.github.ai/inference`) and explained that the key must be compatible with *that specific endpoint*. This is important because a standard `sk-` key might *not* work directly there, depending on GitHub's setup. This addresses your mention of a "GitHub token" being used for an "OpenAI call" via that endpoint – it points the user to the correct place to put whatever key/token is needed for *that specific service*.
        *   Provided an example `.env` format.
        *   Explicitly reminded the user *not* to commit the `.env` file.
    *   Instructed the user to place their actual documents in the `data/` directory.
5.  **How to Run:** Explained the `python main.py` command, what happens during the first run (indexing), and how to interact (type queries, type 'quit').
6.  **Asking for Review and Feedback:** Added a dedicated section reinforcing that you welcome feedback and how they can provide it via GitHub Issues and Pull Requests.
7.  **Available on GitHub:** I rephrased the "GitHub Marketplace" part slightly, as it's not typically used for source code projects like this. Instead, I framed it as a personal project available *on* GitHub for learning, forking, etc. This is a more accurate description of how users interact with standard GitHub repositories.

**Before you push:**

1.  **Replace `<URL_OF_YOUR_REPO>`:** Make sure you replace the placeholder in the `git clone` command with the actual URL of your repository on GitHub once it's created.
2.  **Create `data/`:** Add an empty `data/` directory to your repository so users know where to put files.
3.  **Review the `llm_interface.py` base_url:** Double-check if `https://models.github.ai/inference` is truly the correct base URL for the type of API key you expect users to provide. If you intend for users to use a standard OpenAI API key (like `sk-...`), you might need to remove the `base_url` parameter from the `OpenAI()` client initialization in `llm_interface.py`, as the default is `api.openai.com`. If you *do* specifically intend for the GitHub endpoint, the current explanation is fine, but be aware users might need specific GitHub-related setup beyond just an OpenAI key. The current setup strongly suggests it's tied to GitHub's infrastructure.
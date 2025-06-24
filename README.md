# Web Summariser with Ollama and DeepSeek-R1

A simple Python script that fetches content from a given URL and summarises it using a local Large Language Model (LLM) served by Ollama.

## Features

* **Web Scraping:** Fetches content from any accessible webpage using `requests` and `BeautifulSoup`.
* **Local LLM Integration:** Leverages your locally running Ollama server to summarise the extracted text.
* **Lightweight Model:** Optimized to use `deepseek-r1:1.5b` for efficient operation on consumer hardware.
* **User-Friendly:** Prompts the user for the URL to summarise.

## Prerequisites

Before you run this script, ensure you have the following installed and set up:

1.  **Python 3.x:** (e.g., Python 3.9+)
    * [Download Python](https://www.python.org/downloads/)

2.  **Ollama:**
    * [Download Ollama](https://ollama.com/download)
    * After installation, open your terminal and run `ollama serve` to start the local server. Keep this terminal open while using the script.

3.  **DeepSeek-R1:1.5b Model for Ollama:**
    * In your terminal, pull the model:
        ```bash
        ollama pull deepseek-r1:1.5b
        ```

## Setup

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/SOSARS/AI-Summariser
    cd AI-Summariser 
    ```

2.  **Create and activate a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows (PowerShell):
    .venv\Scripts\activate
    # On macOS/Linux/Git Bash:
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Ensure your Ollama server is running (from the Prerequisites section: `ollama serve`).
2.  Run the Python script from your terminal:
    ```bash
    python main.py
    ```
3.  The script will prompt you to `Enter the URL of the webpage to summarise:`. Paste your desired URL and press Enter.
4.  The script will fetch the content, summarise it using DeepSeek-R1, and print the summary to the console.

## Customisation (Optional)

* **Change Ollama Model:** If you want to use a different model installed in Ollama (e.g., `llama3`), update the `OLLAMA_MODEL_NAME` variable in `main.py`.
* **Adjust Summarisation Prompt:** Modify the `llama_prompt` variable in the `summarise_text` function in `main.py` to change how the model summarises (e.g., "Summarise for a child", "Extract key financial points").
* **Refine Web Scraping:** For specific websites that might not scrape well, you might need to adjust the `main_content_elements` selectors in the `extract_text` function in `main.py` by inspecting the website's HTML structure.

## License

This project is open-source and available under the [Choose a license, e.g., MIT License](https://opensource.org/licenses/MIT).

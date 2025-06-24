from bs4 import BeautifulSoup as bs
import requests
import json
import sys
import lxml


# ------ Configurations ---------------
OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL_NAME = "deepseek-r1:1.5b"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}
# -------- End of configurations ------


def fetch_webpage(website_url):
    # --- Fetch the content from the webpage
    print(f"\n--- Step 1: Fetching content from {website_url}")
    raw_html = None
    try:
        response = requests.get(website_url, headers=HEADERS, timeout=30)
        response.raise_for_status() # 4xx (client error) or 5xx (server error)
        raw_html = response.text
        print("Hey! I found your webpage. I'm extracting the content now 😋")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage from {website_url}: {e}")
        print("Please check your internet connection and try again")
        sys.exit(1)  # Exit with an error code

    return raw_html


def extract_text(raw_html):
    # --- Step 2: Parse the HTML and extract the main text
    print(f"\n--- Step 2: Parsing HTML from {website_url}")
    extracted_text = ""

    if raw_html: # only continue if raw html is not 'None'
        try:
            soup = bs(raw_html, "lxml")
            main_content_elements = soup.find("main") or \
                soup.find("article") or \
                soup.find("div", class_="content") or \
                soup.find("div", class_="main-content") or \
                soup.find("div", class_="article-content") or \
                soup.find("div", class_="main-content-text") or \
                soup.find_all("div", class_="entry-content")

            if main_content_elements:
                # separator='\n' ensures that different paragraphs get their own line.
                # strip=True removes leading/trailing whitespace from each line.
                extracted_text = main_content_elements.get_text(separator="\n", strip=True)

            else:
                print("Warning: Specific main content element not found. Attempting to extract content.")
                extracted_text = soup.get_text(separator="\n", strip=True)


            # --- Post-Extraction Cleaning ---
            # Removes excessive blank lines and consolidates whitespace within lines
            # This makes the text cleaner for the LLM
            cleaned_lines = []
            for line in extracted_text.splitlines():
                stripped_line = line.strip()
                if stripped_line:
                    cleaned_lines.append(stripped_line)

            extracted_text = "\n".join(cleaned_lines)

            if extracted_text:
                print(f"I found something... 😄 Here are the first 500 characters:\n{extracted_text[:500]}")

            else:
                print("No text extracted.. something went wrong 🥲")
                exit()

        except Exception as e:
            print(f"Error parsing webpage content: {e}")
            print("This might be due to unexpected HTML structure or a problem with BeautifulSoup.")
            exit()  # Exit if parsing fails

    else:
        print("No raw HTML available to parse. This should not happen if Step 1 succeeded.")

    return extracted_text


def summarise_text(extracted_text, model_name=OLLAMA_MODEL_NAME):
    # --- Step 3: Send the text to local Llama 3.2 for summarising
    print(f"\n--- Step 3: Sending text to model: {OLLAMA_MODEL_NAME} for summarising")
    summ_length = int(input("How many characters long would you like your summary? (sugg: 300 characters)\n"))

    llama_summary = "Failed to create the summary"  # in case of early exit
    llama_prompt = (
        "Please provide a concise summary of the following text."
        "Focus on the main points and key information."
        "The summary should be no more than 200 words and should be easy to understand."
        f"Text:\n{extracted_text}\n\n"
        "Summary: "
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarises text concisely."},
        {"role": "user", "content": llama_prompt}
    ]

    try:
        ollama_payload = {
            "model": OLLAMA_MODEL_NAME,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": summ_length
            }
        }

        api_headers = {"Content-Type": "application/json"}
        ollama_response = requests.post(
            OLLAMA_API_URL,
            headers=api_headers,
            data=json.dumps(ollama_payload),
            timeout=300
        )
        ollama_response.raise_for_status()  # Check for HTTP errors in the response from Ollama
        ollama_response_data = ollama_response.json()  # Parse JSON response from Ollama

        if ollama_response_data and "message" in ollama_response_data and "content" in ollama_response_data["message"]:
            llama_summary = ollama_response_data["message"]["content"].strip()
            print("Summarisation request successful")

        else:
            print(f"Unexpected response structure from Ollama: {ollama_response_data}")
            llama_summary = "Failed to extract summary from Ollama response due to unexpected format."

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Ollama server.")
        print("Please ensure Ollama is running (`ollama serve` in a terminal) and the model is loaded (`ollama pull llama3.2`).")
        llama_summary = "Failed to connect to local Llama server."

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Problem communicating with Ollama API: {e}")
        if e.response:
            print(f"Ollama API raw response content (if available): {e.response.text}")
        llama_summary = "Failed to communicate with Ollama API due to an error."

    except json.JSONDecodeError as e:
        # Catches errors if Ollama's response is invalid JSON
        print(f"ERROR: Failed to parse JSON response from Ollama: {e}")
        llama_summary = "Invalid JSON response from Ollama."

    except Exception as e:
        # General catch-all for any other unforeseen errors
        print(f"An unexpected error occurred during summarisation: {e}")
        llama_summary = "An internal error occurred during summarisation."

    return llama_summary


# ------- Main Execution Block --------
if __name__ == "__main__":

    # Get the url from the user
    website_url = input("Enter the url of your website:\n")
    raw_html = fetch_webpage(website_url)

    if raw_html:
        extracted_text = extract_text(raw_html)
        summary = summarise_text(extracted_text)

    # --- Step 4: Display the summary
        print("\n--- Step 4: Final Summary")
        print("---------------------------")
        print(summary)
        print("---------------------------")

    else:
        print("You did provide a valid URL. Goodbye ☹️")
        sys.exit(1)










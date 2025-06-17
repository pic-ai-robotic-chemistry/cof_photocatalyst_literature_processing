import sys
import os
import csv
from openai import OpenAI
import tiktoken  # Install with `pip install tiktoken`
from datetime import datetime
# Fixed part of the prompt
FIXED_PROMPT = "Please read this piece of text, identify information regarding the synthesis procedure of a stable COF, the linkers that build the stable COF, and the principles behind such stability. Please draft your response exclusively from the information mentioned in the text. The text might accidently contain reference information at the bottom, please ignore these lines if they occur, and only focus on the content in the current article. Below is the text:"

# Token limit
TOKEN_LIMIT = 63000

def read_api_key(filepath):
    """Read the API key from key.txt."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().strip()

def estimate_token_count(text, encoding_name='cl100k_base'):
    """Estimate the number of tokens in a given text."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def process_files(directory, api_key, output_csv, error_log):
    """Process text files in the directory and query the LLM."""
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    data = []
    errors = []

    # Iterate through all .txt files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            print(filename)
            # Read the content of the text file
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            # Combine fixed prompt and content
            full_prompt = f"{FIXED_PROMPT} {content}"

            # Estimate token count
            token_count = estimate_token_count(full_prompt)
            print(token_count)
            if token_count > TOKEN_LIMIT:
                errors.append([os.path.splitext(filename)[0], "Token limit exceeded"])
                continue

            # Query the LLM
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": full_prompt},
                    ],
                    stream=False
                )

                # Extract the response content
                response_text = response.choices[0].message.content
                print(response_text)
                # Store the file name without extension and the response
                data.append([os.path.splitext(filename)[0], response_text])
            except Exception as e:
                errors.append([os.path.splitext(filename)[0], str(e)])

    # Write results to a CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Response"])
        writer.writerows(data)

    # Write errors to a log file
    with open(error_log, 'w', encoding='utf-8', newline='') as errorfile:
        writer = csv.writer(errorfile)
        writer.writerow(["File Name", "Error"])
        writer.writerows(errors)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    api_key = read_api_key("key.txt")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"output_{timestamp}.csv"
    error_log = f"error_log_{timestamp}.csv"
    process_files(directory, api_key, output_csv, error_log)
    print(f"Results saved to {output_csv}")
    print(f"Errors logged in {error_log}")

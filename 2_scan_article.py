import csv
from openai import OpenAI
from tqdm import tqdm
import sys

# Read API key from key.txt
with open("key.txt", "r") as key_file:
    api_key = key_file.read().strip()

# Initialize DeepSeek client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# Fixed prompt text
FIXED_PROMPT = "In this dialogue you will see a piece of text from a research article regarding Covalent Organic Frameworks (COF). For the piece of text you shall determine whether the text is relevant to the topic of the synthesis of a structurally stable COF. If the sentence is incomplete or seems to be a combination of incomplete sentences, please respond 'Nonsense'. For the response, you should only answer between 'Irrelevant', 'Nonsense' and 'Relevant'. Here is the piece of text: "

# Function to query DeepSeek API
def query_llm(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content

# Read markdown file
markdown_file = sys.argv[1] 
with open(markdown_file, "r") as f:
    rows = [line.strip() for line in f if line.strip()]

# Prepare CSV output
output_file = sys.argv[2]  
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Original Text", "Response"])

    # Process each row and query DeepSeek
    for row in tqdm(rows, desc="Processing rows"):
        try:
            prompt = f"{FIXED_PROMPT}{row}"
            response = query_llm(prompt)
            writer.writerow([row, response])
        except Exception as e:
            print(f"Error processing row: {row}\n{e}")

print(f"Responses saved to {output_file}")
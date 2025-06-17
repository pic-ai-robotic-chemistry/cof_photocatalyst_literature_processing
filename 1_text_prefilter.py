import re
import sys
from tqdm import tqdm
import os

def process_text_file(input_file,output_file):
    print(input_file)
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    buffer = ""  # To hold unfinished sentence

    for i in tqdm(range(len(lines)), desc="Processing lines"):
        line = lines[i].strip()

        if not line:
            continue  # Skip empty lines

        # Remove URLs (https://{url} and www.{url})
        line = re.sub(r'\bhttps?://\S+\b', '', line)
        line = re.sub(r'\bwww\.\S+\b', '', line)

        # Remove **** patterns (four asterisks together)
        line = re.sub(r'\*{4}', '', line)

        # Check if line starts with a capital letter and ends abruptly (no ending punctuation or breaks mid-sentence)
        if re.match(r'^[A-Z].*\b(?!.*[.?!]$).*$', line):
            if buffer:
                # Append current buffer to processed lines before overwriting
                processed_lines.append(buffer)
            buffer = line  # Store unfinished sentence in buffer
        elif re.match(r'^[a-z].*[.?!]$', line):
            if buffer:
                # Combine unfinished sentence with the closest sentence finisher below
                processed_lines.append(f"{buffer} {line}")
                buffer = ""  # Clear buffer
            else:
                processed_lines.append(line)  # No unfinished sentence, add normally
        else:
            # For any other line, simply add to processed lines
            if buffer:
                # Search for the closest finisher in subsequent lines
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if re.match(r'^[a-z].*[.?!]$', next_line):
                        processed_lines.append(f"{buffer} {next_line}")
                        buffer = ""  # Clear buffer
                        break
                else:
                    # If no finisher found, just add the buffer as is
                    processed_lines.append(buffer)
                    buffer = ""
            processed_lines.append(line)

    # Add any remaining buffer
    if buffer:
        processed_lines.append(buffer)

    # Write the processed lines to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(processed_lines))

    print(f"Processed file saved to: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_directory>")
        return

    input_dir = sys.argv[1]
    output_dir = f"{input_dir}_cleaned"

    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        input_file = os.path.join(input_dir, file_name)
        if os.path.isfile(input_file):
            base_name = os.path.splitext(file_name)[0]
            output_file = os.path.join(output_dir, f"{base_name}_fixed.txt")
            process_text_file(input_file, output_file)

if __name__ == "__main__":
    main()
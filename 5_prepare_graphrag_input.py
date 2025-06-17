#!/usr/bin/env python3
"""
Script to create a folder and generate text files from CSV data.
Usage: python script.py <folder_name>
"""

import sys
import os
import csv

def main():
    # Check if folder name is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <folder_name>")
        sys.exit(1)
    
    # Get folder name from command line argument
    folder_name = sys.argv[2]
    
    # Create the folder if it doesn't exist
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created/ensured folder exists: {folder_name}")
    except Exception as e:
        print(f"Error creating folder {folder_name}: {e}")
        sys.exit(1)
    
    # CSV file name (adjust this to match your actual file name)
    csv_file = sys.argv[1]
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    # Read CSV and create text files
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            files_created = 0
            for row in csv_reader:
                file_name = row['File Name']
                response_content = row['Response']
                
                # Add .txt extension if not already present
                if not file_name.endswith('.txt'):
                    file_name += '.txt'
                
                # Create full path
                file_path = os.path.join(folder_name, file_name)
                
                # Write content to file
                with open(file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(response_content)
                
                print(f"Created: {file_path}")
                files_created += 1
            
            print(f"\nSuccessfully created {files_created} text files in '{folder_name}' folder")
    
    except FileNotFoundError:
        print(f"Error: Could not find CSV file '{csv_file}'")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing expected column {e} in CSV file")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
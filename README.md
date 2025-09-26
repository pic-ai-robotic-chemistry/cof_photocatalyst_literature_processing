**HOW TO USE**  
Clone the repository, edit the API endpoint and model (default DeepSeek V3) used in LLM-related steps (2_scan_article.py and 4_query_processed.py), then create a key.txt file that contains the API key for your selected endpoint.  
Place your articles in plain text/markdown format in "raw" folder (which can be generated from PDF articles with tools like [Marker](https://github.com/datalab-to/marker) and [Docling](https://github.com/docling-project/docling)).  
When your input files are ready, either run the python scripts sequentially in numerical order, or run workflow.sh as a one-click method. After the process is complete, a folder named "graphrag_in" will be generated, and it contains the input documents for a standard GraphRAG indexing.  
Regarding the articles we've used in our knowledge graph construction, you will find the information in file_names.txt, and we will be uploading a properly formatted article metadata table in a few days.

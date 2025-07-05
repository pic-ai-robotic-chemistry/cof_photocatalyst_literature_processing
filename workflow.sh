python ./1_text_prefilter.py raw
mkdir processed
for file in raw_cleaned/*_fixed.txt; do filename=${file#raw_cleaned/}; python 2_scan_article.py "${file}" processed/"${filename%_fixed.txt}.csv"; done
for file in processed/*.csv; do filename=${file#processed/}; python 3_get_extracted_text.py "${file}" "processed/${filename%.csv}.txt"; done
python 4_query_processed.py processed
python 5_prepare_graphrag_input.py output_20250617_234942.csv graphrag_in
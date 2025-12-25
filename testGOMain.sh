#!/bin/bash

set -e

if [ $# -lt 2]; then
	echo " $0 <input_prefix> <output_dir>
	echo "$0 my_protein output_go"
	echo "input format: input_prefix_annotations, seed_orthologs, hmm_hits"
	exit 1
fi

INPUT_PREFIX =$1
OUTPUT_DIR=$2
ANNOTATION = "${INPUT_PREFIX}.emapper.annotations"
SEED = "${INPUT_PREFIX}.emapper.seed_orthologs"
HMM="${INPUT_PREFIX}.emapper.hmm_hits"

missing_files=()
for file in "$ANNOTATION" "$SEED" "$HMM"; do
	if [ ! -f "$file" ]; then
		missing_files+=("$file")
	fi
done

if [ ${#missing_files[@]} -gt 0]; then
	echo "the files does not exist:"
	for file in "${missing_files[@]}"; do 
		echo "$file"
	done
	exit 1
fi

mkdir -p "$OUTPUT_DIR"

python3 extract_go_annotations.py "$ANNOTATION" "$OUTPUT_DIR"
python3 extract_functional_annotations.py "ANNOTATION" "$OUTPUT_DIR" 

if  [$# -eq 3 ]; then
	BACKGROUND_FILE = $3
	python3 go_enrichment.py "ANNOTATION" "$BACKGROUND_FILE" "$OUTPUT_DIR"
fi

python3 go_statistics.py "$OUTPUT_DIR/go_annotations.tsv" "$OUTPUT_DIR"

python3 create_go_report.py "$OUTPUT_DIR" "$INPUT_PREFIX"


#!/bin/bash

set -e 

if [ $# -ne 2 ]; then
	echo "input: $0 <eggnog annotation> <output prefix>"
	echo "example: $0 emapper.annotations my_results"
	exit 1
fi

INPUT_FILE="$1"
OUTPUT_PREFIX="$2"

if [ ! -f "$INPUT_FILE" ]; then 
	echo "$INPUT_FILE does not exist"
	exit 1
fi

TOTAL_LINES=$(tail -n +4 "$INPUT_FILE"|wc -l)
if [ "$TOTAL_LINES" -eq 0 ]; then
	echo "no data exists"
	exit 1
fi

#1

awk -F'\t' 'NR>4 && $10!="-" && $10!="" {
	split($10, go_terms, ",");
	for (i in go_terms){
		gsub(/^[\t]+|[\t]+$/,"",go_terms[i]);
		if (go_terms[i]!=""&&go_terms[i]!="-"){
			print $1 "\t" go_terms[i]
		}
	}
}' "$INPUT_FILE" >"${OUTPUT_PREFIX}_go_terms.tsv"

if [ -s "${OUTPUT_PREFIX}_go_terms.tsv" ]; then
	cat "${OUTPUT_PREFIX}_go_terms.tsv" |cut -f2 | sort | uniq -c|sort -rn|awk '{print $2 "\t" $1}' > "${OUTPUT_PREFIX}_go_counts.tsv"
	cat "${OUTPUT_PREFIX}_go_terms.tsv" |cut -f2|grep -E "^GO:[0-9]+"|sort|uniq|wc -l >"${OUT_PREFIX}_unique_go_counts.tsv"	
fi

if [ -f"${OUTPUT_PREFIX}_go_terms.tsv" ]; then
	GO_ENTRIES=$(wc -l<"${OUTPUT_PREFIX}_go_terms.tsv")
	UNIQUE_GO=$(cut -f2 "${OUTPUT_PREFIX}_go_terms.tsv"|sort -u|wc -l)
	echo "$GO_ENTRIES"
	echo "$UNIQUE_GO"
else
	echo "GO annotated: 0"
fi

ls -la "${OUTPUT_PREFIX}"_*

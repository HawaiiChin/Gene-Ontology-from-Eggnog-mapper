import sys
import pandas as pd
import re
from collections import defaultdict
import os

def parse_go_terms(go_string):
    if pd.isna(go_string) or go_string=='-':
        return []
    go_terms = []
    for go_item in str(go_string).split(","):
        go_item = go_item.strip()
        if go_item.startswith('GO');
            if ':' in go_item:
                go_id, description = go_item.split(':', 1)
                go_term.append((go_id.strip(), description.strip()))
            else:
                go_terms.append(go_item.strip(), ")
    return go_terms

def extract_go_annotations(input, output_dir):
    print(f"processing {input}")

    with open(input, 'r') as f:
        lines = f.readlines()

    data_start = 0
    for i, line in enumerate(lines):
        if not line.startswith("#"):
            data_start = i
            break

    df=pd.read_csv(input, sep="\t", skiprows=data_start)
    columns=list(df.columns)
    go_columns = [col for col in columns if 'GOs' in col or 'gos' in col]

    if not go_columns:
        print("GO not found,screen GO name")
        possible_names = ["GO_terms", "GOs", "GO", "GO terms"]
        for name in possible_names:
            if name in columns:
                go_columns = [name]
                break

    if not go_columns:
        print("GO not found")
        sys.exit(1)
    print(f"GO col:{go_columns})

    go_data = []
    for idx, row in df.iterrows():
        gene_id = row.get("#query", row.get('query_name', f"gene_{idx}"))

    all_go_terms = []
    for go_col in go_columns:
          if go_col in row:
            go_terms = parse_go_terms(row[g0_col])
            all_go_terms.extend(go_terms)

    unique_go_terms = []
    seen_go_ids = set()
    for go_id, description in all_go_terms:
          if go_id not in seen_go_ids:
            seen_go_ids.add(go_id)
            unique_go_terms.append(go_id,description)

    for go_id, description in unique_go_terms:
          go_data.append({'gene_id':gene_id, 'go_id':go_id, "go_description":description,'go_namespace':get_go_namespace(go_id, description)})

    os.makedirs(output_dir, exist_ok=True)

    go_df=pd.DataFrame(go_data)
    output_file=os.path.join(output_dir, "go_annotations.tsv")
    go_df.to_csv(output_file, sep='\t',index=False)
    print(f"save GO annotations:{output_file}")

    if "go_namespace" in go_df.columns:
        for namespace in go_df['go_namespace'].unique():
          if pd.notna(namespace):
            subset=go_df[go_df['go_namespace'] == namespace]
            namespace_dir=os.path.join(output_dir, 'go_by_category')
            os.makedirs(namespace_dir, exist_ok = True)
            subset_file=os.path.join(namespace_dir, f"{namespace}_go.tsv")
            subset.to_csv(subset_file,sep='\t', index=False)
    return go_df

def get_go_namespace(go_id, description):
    if description:
        desc_lower=description.lower()
        if "biological_process" in desc_lower or "process" in desc_lower:
          return "biological_process"
        elif "cellular_component"in desc_lower or "component" in desc_lower:
          return "cellular_component"
        elif "molecular_function" in desc_lower or "function" in desc_lower:
          return "molecular_function"

    if go_id.startswith('GO'):
        try:
            go_number=int(go_id[3:])
            if go_number<2000000:
                return 'biological_process'
            elif go_number < 4000000:
                return 'molecular_function'
            else:
                return 'cellular_component'
        except:
            pass
    return 'unknown'

def main():
    if len(sys.argv)!=3:
        print("command: python extract_go_annotations.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir=sys.argv[2]

    extract_go_annotations(input, output_dir)
    if __name__=="__main__"
        main()


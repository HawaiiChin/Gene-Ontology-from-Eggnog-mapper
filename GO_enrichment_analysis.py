import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import argparse
import os
import requests
import json
import gzip
from collections import defaultdict, Counter
import networkx as nx
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

class GOEnricher:
    def __init__(self, go_obo_path="https://geneontology.org/docs/download-ontology/"):
        self.go_terms={} 
        self.load_go_ontology(go_obo_path)

    def load_go_ontology(self, obo_path=None):
        if obo_path and os.path.exists(obo_path):
            print(f"import Gene Ontology:{obo_path}")
            self._parse_obo_file(obo_path)
        else:
            print("use online GO API")

    def _parse_obo_file(self, obo_path):
        with open(obo_path, 'r', encoding= 'utf-8') as f:
            current_term = None

            for line in f:
                line = line.strip()

                if line.startswith('[Term]'):
                    if current_term:
                        self._save_current_term(current_term)
                    current_term={'id': None, 'name':None, 'namespace':None, 'parents':[]}

                elif line.startswith('id:') and current_term:
                    current_term['id'] = line.split(':')[1].strip()
                
                elif line.startswith('name:') and current_term:
                    current_term['name'] = line.split(":",1)[1].strip()

                elif line.startswith('namespace"') and current_term:
                    current_term['namespace']=line.split(':').strip()

                elif line.startswith('is_a:') and current_term:
                    parent=line.split('')[1]
                    current_term['parents'].append(parent)

                elif line.startswith('relationship:part_of') and current_term:
                    parts = line.split('')
                    if len(parts) >= 3:
                        current_term['parents'].append(parts[2])

            if current_term and current_term['id']:
                self._save_current_term(current_term)

        print(f"saving {len(self.go_terms)} GO terms")

    def _save_current_term(self, term):
        go_id = term['id']
        if go_id.startswith('GO:'):
            self.go_terms[go_id]={
                'name':term.get('name','Unknown'),
                'namespace': term.get('namespace', 'Biological_process'),
                'parents': term.get('parents',[])
            }


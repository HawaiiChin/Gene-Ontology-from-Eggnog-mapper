
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class SimpleKEGGPlotter:
    def __init__(self):
        self.pathway_colors={
                'Metabolism':'#FF6B6B',
                'Genetic Information Processing':'#4ECDC4',
                'Environmental Information Processing':'#45B7D1',
                'Cellular Processes':'#96CEB4',
                'Organismal Systems':'#FFEAA7',
                'Human Diseases':'#DDA0DD'
        }

    def create_pathway_diagram(self, pathway_data, gene_abundance,output_file='pathway_diagram.png'):
        fig,ax = plt.subplots(figsize=(14, 10))
        G=nx.DiGraph()
        for i, (gene, data) in enumerate(pathway_data.items()):
            G.add_node(gene, pos=(np.random.uniform(0.1, 0.9),
                                  np.random.uniform(0.1, 0.9)),
                       abundance=gene_abundance.get(gene,0),
                       description=data.get('description', gene))

        pos=nx.get_node_attributes(G, 'pos')
        abundances = [G.nodes[n]['abundance'] for n in G.nodes()]

        if abundances:
            max_abundance=max(abundances)
            min_abundance=min(abundances)
            if max_abundance>min_abundace:
                norm_abundances=[(a-min_abundance)/max_abundance-min_abundance) for a in abundances]
            else:
                norm_abundances = [0.5]*len(abundances)
        else:
            norm_abundances=[0.5]*len(G.nodes())

        nodes=nx.draw_networkx_nodes(G, pos, node_size=800, 
                                     node_color=norm_abundances,
                                     cmap=plt.cm.YIOrRd,
                                     edgecolors='black'
                                     ax=ax)

        nx.draw_networkx_labels(G, pos,
                            labels={n:G.nodes[n]['description'][:15]
                                    for n in G.nodes()},
                            font_size=8, ax=ax)

        if G.edges():
            nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, ax=ax)

        sm=plt.cm.ScalarMappable(cmap=plt.cm.YIOrRD,
                            norm=plt.Normalize(vmin=min(abundances),
                                               vmax=max(abundances)))
        sm.set_array([])
        cbar=plt.colorbar(sm, ax=ax, shrink=0.8)
        cbar.set_label('Gene Abundance', fontsize=12)

        ax.set_title('KEGG Pathway Visualization with Gene Abundance', fontsize = 14, fontweight = 'bold')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_pathway_bar_chart(pathway_stats, output_file='pathway_enrichment.png'):
        pathways=list(pathway_stats.keys())
        counts=[pathway_stats[p]['gene_count'] for p in pathways]

        fig,(ax1, ax2)=plt.subplots(2, 1, figsize=(12, 10))
        bars1 = ax1.barh(pathways, counts, color='skyblue')
        ax1.set_xlabel('Number of Genes')
        ax1.invert_yaxix()
        ax1.set_title('Gene Count per Pathway')

        for bar in bars1:
            width = bar.get_width()
            ax1.text(width+max(counts)*0.01, bar.get_y()+bar.get_height()/2,
                     f'{int(width)}', ha='left', va='center')

        bars2=ax2.barh(pathways,mean_abundance,color='lightcoral')
        ax2.set_xlabel('Mean Gene Abundance')
        ax2.set_title('Mean Abundance per Pathway')
        ax2.invert_yaxis()

        for bar in bars2:
            width=bar.get_width()
            ax2.text(width + max(mean_abundance)*0.01, bar.get_y()+bar.get_height()/2,
                     f'{width:.2f}', ha='left',va='center')

        plt.tight_layout()
        plt.savefig(output_file, dpi=600, bbox_inches='tight')
        plt.show()
        




import streamlit as st
import pandas as pd
import sys, json
sys.path.append("app_dev/codeBase")
import SepsisStudyCode as sSC

st.markdown("""
## Automated Candidate Gene Prioritization Workflow for Sepsis Monitoring Using GPT-4 (Azure-OpenAI)
We utilized GPT-4 to analyze genes associated with various aspects of sepsis, including:

(a) Pathogenesis
(b) Host immune response
(c) Organ dysfunction related to sepsis
(d) Circulating immune biology
(e) Clinical biomarkers for sepsis
(f) Potential as a blood transcriptional biomarker
(g) Known drug targets
Each statement was contextually enriched to ensure more accurate responses. For details on the parameters used, refer to the dropdown section below.

To demonstrate the system's scalability, we processed data from the bloodGen3 dataset, which initially contained 11,465 genes. After excluding hypothetical and redundant genes, 10,824 were analyzed for their response. To identify genes specifically relevant to sepsis, we filtered for those with a score of at least 5 on any of the statements, resulting in 1,070 genes, approximately 9.8% of the total analyzed.

The analysis cost about $200 USD and utilized 156 CPU hours.

""")
with st.expander("see parameter file used for capturing gene specific response to Sepsis"):
    st.json(json.load(open('app_dev/data_repo/paramFiles/sepsis_param.json',"r")))

st.header("Overview of result")
# load bloodGen3 repo data
geneBase = pd.read_csv("app_dev/data_repo/geneList/ModuleTranscript_geneList.csv.gzip",compression="gzip").set_index("geneSymbol")
geneBase = geneBase.drop("Unnamed: 0",axis=1)
# load response curated data
atL1_evd_annpt = pd.read_csv("app_dev/data_repo/CaseStudy/Sepsis/GenelevelData_annnotated.csv").set_index("geneName")
color_key = atL1_evd_annpt[['ClusterName','c_color']].sort_values(by="ClusterName").set_index("ClusterName").to_dict()['c_color']

# plot 1
sepsis_plot1 = sSC.getPlot1(atL1_evd_annpt,geneBase)
st.altair_chart(sepsis_plot1)
st.markdown("""
The top panel depicts the percentage of genes, within each Module Function, that meet the filtering criteria (gene response score ≥5 in at least one 
category). Numbers above each bar represent the total count of genes fulfilling these criteria per Module Function.
The bottom panel presents the distribution of gene response scores, grouped by Module Function. 
Each boxplot shows the range and variability of total scores (sum of all response in filtered gene set) within the genes belonging to a module function,
    illustrating typical and outlier gene responses. Hover-over the plot to know more statistics.         
""")
st.markdown("""
### Comprehensive Analysis of Gene Clustering in Sepsis-Related Research
Our analysis involves clustering a filtered set of genes to identify sub-groups with similar responses to sepsis-related queries, 
effectively categorizing them from the most to least promising candidates based on their response profiles. 
The results highlight:
1. Clustering Response Profiles: Hierarchical clustering reveals distinct sub-clusters of genes. 
These sub-clusters are formed based on their similarity in response to various sepsis-related statements, 
enabling us to identify genes with potentially critical roles in sepsis pathology and treatment.
2. Identification of Promising Candidates: The clustering approach helps segregate the genes into groups from those showing the 
most promising responses (high scores across different statements) to those deemed least promising, providing a 
focused set of candidates for further investigation.
3.Assessment of Variability in Responses: By examining the variability in response profiles within each cluster for 
different sepsis-related statements, we strengthen our confidence in the reliability of our clustering. 
Clusters 1 and 2, in particular, show consistent high scores with minimal variability across all statements,
underscoring their potential significance in sepsis research.
""")
score_cols = [ 'a_pathogenic_assoc', 'b_host_immune_Respo',
    'c_organ_dysfunction', 'd_circu_leu_imm_biol', 'e_biomarker_clinical',
    'f_pot_bolldtransc_biomarker', 'g_drug_target', 'h_theraputically_rel',]

sepsis_plot2 = sSC.getPlot2(atL1_evd_annpt,score_cols, color_key)
st.altair_chart(sepsis_plot2)
st.markdown("""
1. *Hierarchical Clustering of Sepsis-Related Genes Based on Response Scores* :This figure presents a hierarchical clustering analysis of 1,070 genes filtered based on their relevance to sepsis-related queries. 
The dendrogram illustrates the patterns of gene response to sepsis related questions, grouped by similarity in their response scores. 
Each branch represents a cluster of genes that exhibit similar response behaviors, aiding in the identification of potential genetic markers or 
targets for sepsis therapy. The color intensity within each cluster corresponds to the relative confidence levels of the genes, ranging from 0 (low confidence) to 10 (very high confidence), 
providing deeper insights into the reliability of the gene data within the context of sepsis.

2. *Heatmap of Response Score Variability for Sepsis-Related Gene Clusters* : 
This heatmap visualizes the variability and central tendency of response scores across different clusters of sepsis-related genes, categorized by various aspects of sepsis pathology and treatment. 
The rows represent different queries relevant to sepsis and The columns correspond to gene clusters numbered 1 through 5, previously identified in hierarchical clustering analyses. The color gradient from light blue to deep red indicates the median response score for genes within each cluster for the corresponding query, with red denoting a higher median response and blue a lower. The size of each circle indicates the standard deviation of the response scores within each cluster, providing insight into the consistency of gene responses; larger circles signify greater variability.
This heatmap allows for a comparative analysis of gene behavior across clusters, highlighting differences in gene response that may be critical for understanding sepsis mechanisms or developing targeted therapies.

3. *Distribution of Gene Populations Across Clusters* : This bar plot visualizes the distribution of gene counts across five distinct clusters identified in 
the previous hierarchical clustering analysis of sepsis-related genes. Each bar represents a cluster, with the height indicating the number of genes grouped within that cluster. 
The color coding is consistent with the hierarchical plot, providing a visual correlation. Cluster 1 (Red): 203 genes, Cluster 2 (Purple): 201 genes, 
Cluster 3 (Orange): 95 genes, Cluster 4 (Blue): 342 genes, Cluster 5 (Green): 229 genes. These distributions help in assessing the relative size and significance of each cluster, 
potentially correlating with different gene functions or response types associated with sepsis.
            
This structured approach not only refines our understanding of gene behavior in sepsis but also enhances the selection 
process for potential therapeutic targets based on robust statistical evidence. In following section, we have shown the analysis in differernt
resolution, staring from module , Module Function Title and Module Aggregate. With each increimental resolution we aim to opt more coarse-grain over-view of the range of gene
gets effected in the context of Sepsis. These aggregates are well defined in the [BloodGen3](https://pubmed.ncbi.nlm.nih.gov/33624743/).
""")
# plot4

st.header("Module Response Profile to Sepsis")
moduleFracPlot = sSC.moduleRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key)
st.altair_chart(moduleFracPlot,use_container_width=True)
st.markdown("""
*Distribution of Gene Membership Across Clusters in Different Modules* : stacked bar plot visualizes the distribution of 
gene membership across different modules related to sepsis, with each module represented along the x-axis (total modules = 297).
The y-axis displays the fraction of member genes within each cluster, represented by stacked color bars corresponding to each cluster. 
The calculation for the representation of cluster members in each module is performed by dividing the number of genes in a cluster 
for a specific ModuleID by the total number of genes in that respective ModuleID. The top panel of the figure provides additional 
context by showing the total number and percentage of geapp_devnes in each respective module, 
helping to understand the scale and relevance of each module's gene population.
                """)

st.header("Module Title Profile to Sepsis")
moduleTitleFracPlot = sSC.moduleTitleRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key)
st.altair_chart(moduleTitleFracPlot,use_container_width=True)
st.markdown("""
*Cluster Representation in Functional Modules Related to Sepsis* : This figure illustrates the proportion of
gene representation within each of five clusters across various functional modules pertinent to sepsis,
such as cytokine activation, monocyte responses, and platelet/PSGL-1 interaction. 
Each color in the stacked bar chart represents one of the five clusters, demonstrating how genes 
are distributed across these modules. The y-axis represents the fraction of genes in each cluster 
relative to the total number of genes within the respective module title, providing insights into the 
predominant gene activities and their potential roles in sepsis response mechanisms. 
The specific proportions are calculated by dividing the number of genes in a cluster for 
each module by the total number of genes in that module.""")


st.header("Module Aggregate Profile to Sepsis")
aggregateFracPlot,stacked_aggPlot = sSC.aggregateRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key)
st.altair_chart(aggregateFracPlot,use_container_width=True)
st.markdown("""
*Cluster Membership Distribution Across Module Aggregates* :This figure represents the distribution of gene memberships across 
different Module Aggregates, with each Module Aggregate shown along the x-axis (total Module Aggregates = 35). 
The stacked bars depict the proportion of genes and percentage of gene belonging to each cluster within the aggregates. 
These proportions are calculated by dividing the number of genes in each cluster for a given Module Aggregate by the total 
number of genes in that Module Aggregate. This visualization helps in understanding the clustering pattern and the relative 
contribution of each cluster to the various Module Aggregates, facilitating insights into gene distribution and potential 
functional impacts in sepsis-related gene studies.
""")

st.subheader("Aggregate stacked")
st.altair_chart(stacked_aggPlot,use_container_width=True)

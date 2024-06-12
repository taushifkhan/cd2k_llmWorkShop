import streamlit as st
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import scipy.stats as sp
import sys, json
sys.path.append("app_dev/codeBase")



st.set_page_config(page_title="Example", page_icon=":eyeglasses:")

st.markdown("""
### Benchmarking and Prioritization of Interferon-Related Genes for Translational Research

We conducted a detailed benchmarking and prioritization process for genes within interferon (IFN)-related modules, 
focusing on their potential application in translational research. Our analysis covered six modules containing a total of 114 genes. 
The goal was to identify top candidate genes suitable for further study and application in translational research contexts.

Translational research was defined through a set of eight questions that explored both direct associations with IFN and broader 
applicability as clinical and blood transcriptional biomarkers. These questions were designed to probe both related and orthogonal 
statements to comprehensively define each gene's relevance to current medical research.
            
""")

with st.expander("see parameter file used for capturing gene specific response to Interferon"):
    st.json(json.load(open('app_dev/data_repo/paramFiles/ifn_workshop.json',"r")))

case1, case2 = st.tabs(["IFN-Benchmarking", "IFN-Gene Selection"])

with case1:
    st.markdown("""
    ### A. Benchmarking
    We conducted a benchmarking exercise to assess the robustness of automated API calls compared to manually generated responses. 
    This was performed for one module (M10.1) within the "Interferon" aggregate of the BloodGen3 dataset, which includes 21 genes. 
    For each statement, we generated responses through the standard procedure of three replicates and an extended set of five replicates using automatic API mode. 
    Additionally, extensive manual response generation was conducted in three countries—USA, Thailand, and Qatar—with three replicates for each statement.

    The following responses were compared and analyzed:

    1. Automated API response with three replicates (API_3x)
    2. Automated API response with five replicates (API_5x)
    3. Manual response using Chat-GPT in the USA, three replicates (Manual_USA)
    4. Manual response using Chat-GPT in Thailand, three replicates (Manual_Thailand)
    5. Manual response using Chat-GPT in Qatar, three replicates (Manual_Qatar)
    6. Manual response using Claude-3 in the USA, three replicates (Claude-3)
    #### A.1 Comparing Overall Agreement:
    The aggregate (mean) response for each statement (n=8) across the 21 genes was evaluated for all six response modes. 
    Pearson correlation was utilized to compare the agreement in the overall mean responses generated across the aforementioned modes.
                """)
    bm_inter = pd.read_csv("app_dev/data_repo/CaseStudy/Interferone/Benchmarking_M10.1.csv.gz",compression="gzip")
    corr_overall = bm_inter[['API_3x', 'API_5x', 'Manual_US',
       'Manual_Thailand', 'Manual_Qatar', 'Claude-3']].corr()
    corr_interX = corr_overall.unstack().reset_index().rename({'level_0':'callMode1','level_1':'callMode2',0:'pearsonCorr'},axis=1)

    corr_plot = alt.Chart(corr_interX,width=500, height=400).mark_rect().encode(
        x=alt.X("callMode1"),
        y=alt.Y("callMode2"),
        color=alt.Color('pearsonCorr',scale=alt.Scale(scheme="tealblues")),
        tooltip=['pearsonCorr']
    )
    st.altair_chart(corr_plot)

    st.markdown("""
    *Pearson Correlation Plot of Different Response Generation Modes* : The Pearson correlation plot displays various modes of response generation 
    with a color gradient from teal to blue, indicating increasing agreement. As expected, the highest correlations were observed between the 3x and 5x API-driven 
    responses compared to the manual responses, with a Pearson correlation coefficient greater than 0.96. This high level of agreement may be attributed to the fixed 
    setting (temperature and random seed) used in the API request parameters. Interestingly, higher correlations were also noted for manual responses generated in the
    USA and Thailand, with Pearson correlations exceeding 0.91. However, there was a marginally lower correlation between API responses and manual responses,
    particularly for the USA (p_corr = 0.81) and Thailand (p_corr = 0.79). Conversely, for Qatar, the agreement increased, showing a Pearson correlation of 0.92.

    #### A.2 Agreement Over Each Statement
    For benchmarking, we analyzed eight statements across six modes of response generation in a pairwise manner (n=15), generating a Pearson correlation 
    (r-square) for each pair across the statements. As illustrated in the heatmap, 
    """)

    mode_pair = list(itertools.combinations(['API_3x', 'API_5x', 'Manual_US',
       'Manual_Thailand', 'Manual_Qatar', 'Claude-3'],2))
    
    statement_rel = pd.DataFrame(index=bm_inter.Statements.unique())
    for kname, kgrp in bm_inter.groupby("Statements"):
        for kpair in mode_pair:
            kapr_name = ":".join(kpair)
            col1 = kgrp[kpair[0]].values
            col2 = kgrp[kpair[1]].values
            r, p = sp.pearsonr(col1,col2)
            statement_rel.loc[kname,kapr_name+"_r"] = round(r,2)
    
    statement_relPT = statement_rel.unstack().reset_index().rename({'level_0':'modePair','level_1':'statements',0:'pearson_r'},axis=1)

    statementPlot = alt.Chart(statement_relPT,width=350, height=400).mark_rect().encode(
            x=alt.X("modePair",axis=alt.Axis(labelFontSize=12,labelLimit=300,title='')),
            y=alt.Y("statements",axis=alt.Axis(labelFontSize=12,labelLimit=200,title='')),
            color=alt.Color('pearson_r',scale=alt.Scale(scheme='blueorange',clamp=True)),
            tooltip=['modePair','statements','pearson_r']
        )
    
    st.altair_chart(statementPlot,use_container_width=True)

    st.markdown("""
    The color code on the heatmap represents the Pearson correlation for each pair of response generation methods (columns) across 
    different statements (rows). While the overall correlation remains positive (minimum = 0.6), some deviations are observed depending on 
    the statements analyzed. The most significant deviations were noted in statements regarding (e) use as a biomarker in clinical settings and (g) known drug targets.
    #### A.3. Agreement Over Each Pairwise Mode of Response
    
    """)
    sel_modepair = st.selectbox("Select Modes to compare",mode_pair)
    mode_relation_plot = alt.Chart(bm_inter).mark_point(filled=True).encode(
            x=alt.X(sel_modepair[0]),
            y=alt.Y(sel_modepair[1]),
            color=alt.Color("Statements"),
            tooltip=['GeneSymbol','Statements',sel_modepair[0],sel_modepair[1]]
        )
    st.altair_chart(mode_relation_plot,use_container_width=True)

    st.markdown("""
    ### Summary of Benchmarking Findings

    The benchmarking exercise evaluated the robustness of automated API calls compared to manual response generation, focusing on responses related to interferon modules 
    within the BloodGen3 dataset. Various modes of response generation were analyzed, including automated responses with three and five replicates, and manual responses 
    generated in three different countries using two different AI models.

    Key Findings:

    1. **High Agreement in Automated Responses**: Automated responses generated by the API, particularly with three and five replicates, showed the highest agreement, with Pearson correlation coefficients exceeding 0.96. This suggests a strong consistency in automated response generation, likely influenced by fixed parameter settings in the API requests.
    2. **Manual Response Variability**: Manual responses varied by location, with the USA and Thailand showing higher correlations (greater than 0.91), indicating good reliability in these responses. However, the correlation was slightly lower when comparing API responses with manual responses from the USA and Thailand, but increased with responses from Qatar.
    3. **Statement-Specific Deviations**: Deviations in correlation were particularly noted in responses related to the use of genes as biomarkers in clinical settings and as known drug targets, indicating that these areas might have less consistency across different response generation modes.
    4. **Overall Positive Correlation**: Across all modes and statements, the correlation remained positive, though with some deviations, underscoring the general reliability of the response generation methods used in the study.
        """)


def get_barPlot_scores(df, moduleName):
    dfX =  df[df.moduleID==moduleName]
    score_aggregatePT_mean =dfX.pivot_table(index="geneSymbol",columns="questions",values="score")
    genesorted_Score = list(score_aggregatePT_mean.sum(axis=1).sort_values().index)

    barplot_Scores = alt.Chart(dfX).mark_bar().encode(
        y=alt.Y('geneSymbol',sort=genesorted_Score),
        x='sum(score)',
        color=alt.Color('questions',legend=alt.Legend(labelLimit=200)),
        tooltip=['questions','geneSymbol']
    ).properties(title="{} scores".format(moduleName))

    return barplot_Scores

def do_polarplot(df, moduleName):
    """
    df = Dataframe with top quantile genes
    moduleID = module for which plot has to be generated
    """
    df = df.reset_index()
    data = df[df.moduleID == moduleName]
    # Convert the column labels (except for the first column which is gene_name) into angles
    labels = data.columns[2:]  # Exclude the gene_name column for the labels
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The radar chart plots a circle, so we need to "complete the loop" and append the start value to the end.
    angles += angles[:1]

    # Plotting
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    # Function to create the plot for each gene
    def add_to_plot(ax, values, label):
        values = np.concatenate((values,[values[0]]))
        ax.plot(angles, values, linewidth=1, linestyle='--', label=label,marker="o")
    #    ax.fill(angles, values, alpha=0.25)

    # Loop through each row and add the plot
    for index, row in data.iterrows():
        add_to_plot(ax, row[2:].values, row[0])

    # Labels for each category
    ax.set_theta_offset(np.pi / 2)  # Start the top
    ax.set_theta_direction(-1)  # Move clockwise

    # Draw one axe per variable and add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Draw ytick labels to show scale
    ax.set_rlabel_position(0)
    plt.yticks([2,4,6,8], ["2","4","6","8"], color="grey", size=7)
    plt.suptitle('Module : {}'.format(moduleName), fontsize=16)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.4, 0.75), ncols=1)
    return fig


with case2:
    st.markdown("""
    ### B. Gene Prioritization
    Our gene prioritization workflow is a collaborative process that combines and assesses statement scores from both manual and automated 
                response generations. This approach, pivotal to our pipeline, focuses on a score-driven methodology.

    #### B.1 Total Score as an Indicator of Gene Relevance
    We calculate the mean score for each gene across all questions to determine its overall standing in a specific context.
    The stacked bar plot illustrates these aggregated responses for each gene within a chosen module, with different questions 
    represented by unique colors. Total scores are summed to rank genes within their modules, displayed on the y-axis in ascending 
    order of their total score from top to bottom.
    
                """)
    api_scores = pd.read_csv("app_dev/data_repo/CaseStudy/Interferone/ApiScore_replicates.csv.gz",compression="gzip")
    module_select = st.selectbox("load a module to see overall score", api_scores.moduleID.unique())
    stackedPLot = get_barPlot_scores(api_scores, module_select)
    st.altair_chart(stackedPLot,use_container_width=True)

    st.markdown("""
    #### B.2 Selection of Top Scoring Genes
    We independently analyze the total score distribution for each module to identify high-performing genes, 
    typically selecting those above the 75th quantile. This threshold is adjustable, allowing customization based on specific
    research goals or expert insights. A visual slider facilitates quantile selection, with top genes highlighted in red on the plot and listed in a table below.
                """)

    q_val=st.slider("Quantile cut-off for top gene", 0.25,1.0, 0.75)

    def getTopGenes(api_scores,q_val=0.75):
        totalScore = api_scores.groupby(['moduleID','geneSymbol'])['score'].sum().reset_index()
        for kname,kgrp in totalScore.groupby('moduleID'):
            totalScore.loc[kgrp.index,'normScore'] = kgrp['score']/kgrp['score'].max()
            q_cutoff = kgrp['score'].quantile(q_val)
            top_genes = kgrp[kgrp['score']>=q_cutoff].index
            totalScore.loc[top_genes,'topGene']=1
        totalScore['gene_module'] = totalScore['geneSymbol']+"_"+totalScore['moduleID']
        return totalScore
    
    totalScore = getTopGenes(api_scores, q_val=q_val)
    api_scores_filter  = api_scores[api_scores.gene_module.isin(totalScore[totalScore.topGene==1].gene_module.values)]
    api_scores_filterPT = api_scores_filter.pivot_table(index=["geneSymbol","moduleID"],columns="questions",values="score")

    splot = plt.figure(figsize=(3,3))
    sns.boxplot(x='normScore',y='moduleID',data=totalScore)
    sns.stripplot(x='normScore',y='moduleID',data=totalScore[totalScore.topGene.isna()],color="gray")
    sns.stripplot(x='normScore',y='moduleID',data=totalScore[totalScore.topGene==1],color="r")

    st.pyplot(splot,use_container_width=True)
    st.info("Top genes [red dots from plot above]")
    st.write(totalScore[totalScore.topGene==1].groupby('moduleID')['geneSymbol'].agg(['nunique',list]))

    lableNames = {'a. Association with type I interferon responses':'a.Assoc_IFN-I',
    'b. Association with type II interferon responses':'b.Assoc_IFN-II',
    'c. Association with type III interferon responses':'c.Assoc_IFN-III',
    'd. Relevant to circulating leukocytes immune biology':'d.Rel_Circu_Leukocyte',
    'e. Used as a biomarker in clinical settings':'e.BioMarker_Clinical',
    'f. Potential value as a blood transcriptional biomarker':'f.BioMarker_BloodTranscip.',
    'g. Known drug target':'g.Drug_Target_Known',
    'h. Therapeutically relevant for immune system diseases':'h.Theraputic_Rel_ImmSysDise',
    }

    st.markdown("""
    #### B.3 Performance Evaluation of Selected Genes
    The effectiveness of the selected genes is then compared across different questions. 
    This comparison is visualized using a polar plot, where each gene is color-coded, and the distance from the center indicates
    the aggregate score for each question.
    """)

    api_scores_filterPTX= api_scores_filterPT.rename(lableNames,axis=1)
    show_top_module = st.selectbox("Select modules:", api_scores.moduleID.unique())
    st.pyplot(do_polarplot(api_scores_filterPTX, show_top_module))
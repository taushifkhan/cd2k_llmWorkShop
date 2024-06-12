import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import fcluster
import altair as alt
import pandas as pd

def getPlot1(atL1_evd_annpt, geneBase):
    txb = geneBase[geneBase.ModuleTitle.isin(atL1_evd_annpt.ModuleTitle.unique())]

    scoreOrder = atL1_evd_annpt.groupby('ModuleTitle')['totalScore'].agg("median").sort_values().index
    titlBoxplot = alt.Chart(atL1_evd_annpt,height=200).mark_boxplot().encode(
        x=alt.X('ModuleTitle',sort=list(scoreOrder),
                axis=alt.Axis(title="Module Function Title",
                              titleFontSize=10,
                              labelFontSize=14,
                              labelLimit=500)),
        y='totalScore'
    )

    # module pct presence
    # vx_mod = atL1_evd_annpt.groupby('ModuleTitle')['ModuleID'].nunique()
    # tx_module = txb.groupby('ModuleTitle')['ModuleID'].nunique()
    # pct = (vx_mod/tx_module)*100

    # pct_modules = pd.DataFrame([vx_mod,pct],index=['moduleCount','pct_of_BG3']).T
    
    # module_bar = alt.Chart(pct_modules.reset_index(),height=150).mark_bar().encode(
    #     x=alt.X('ModuleTitle',sort=list(scoreOrder),axis=alt.Axis(labels=False,title='')),
    #     y=alt.Y('pct_of_BG3',axis=alt.Axis(title="pct Module Count"))
    # )
    # module_text = module_bar.mark_text(
    #         align="center",
    #         baseline="middle",
    #         dy=-5,
    #         size=14
    #     ).encode(text="moduleCount")
    # module_bar_plot = module_bar+module_text

    # plot gene percentage
    vx_gene = atL1_evd_annpt.groupby('ModuleTitle').size()
    tx_gene = txb.groupby('ModuleTitle').size()
    pct_gene = (vx_gene/tx_gene)*100

    pct_genes = pd.DataFrame([vx_gene,pct_gene],index=['geneCount','pct_of_BG3']).T

    gene_bar = alt.Chart(pct_genes.reset_index(),height=150).mark_bar().encode(
    x=alt.X('ModuleTitle',sort=list(scoreOrder),axis=alt.Axis(labels=False,title='')),
    y=alt.Y('pct_of_BG3',axis=alt.Axis(title="pct Gene Count"))
    )
    gene_text = gene_bar.mark_text(
        align="center",
        fontStyle="italic",
        baseline="middle",
        color="#756bb1",
        dy=-5,
        size=14
    ).encode(text="geneCount")
    gene_bar_plot  = gene_bar+gene_text

    # final_figure = alt.vconcat(gene_bar_plot,module_bar_plot, titlBoxplot).resolve_scale(
    #     x='shared')
    final_figure = alt.vconcat(gene_bar_plot,titlBoxplot).resolve_scale(x='shared')
    return final_figure


def getPlot2(atL1_evd_annpt,score_cols,color_key):
    cbarLeft = atL1_evd_annpt[['c_color','ClusterName']].reset_index()
    
    # side bar heatmap for cluster numbers
    cluserD = alt.Chart(cbarLeft,width=25,height=500).mark_rect().encode(
        y=alt.Y('geneName',axis=None,sort=None),
        color=alt.Color('ClusterName:O',
                        scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values())),
                        legend=alt.Legend(orient='bottom',
                                        direction="vertical",
                                        legendY=40,
                                        title='Cluster')
                        ),
        tooltip=['geneName','ClusterName']
    )

    # heatmap for scores
    dmat   = atL1_evd_annpt[score_cols]
    dmat_melt = dmat.reset_index().melt(id_vars='geneName',value_vars=dmat.columns,value_name='score',var_name='questions')

    hmalt = alt.Chart(dmat_melt,width=200,height=500).mark_rect().encode(
        y= alt.Y('geneName',sort=None,axis=None),
        x=alt.X('questions',sort=None,axis=alt.Axis(labelLimit=500)),
        color=alt.Color('score',scale=alt.Scale(scheme="lightgreyteal")),
        tooltip=['geneName','score','questions']
    )

    sepsis_plot3_lift= alt.hconcat(cluserD,hmalt, spacing=0).resolve_axis(y='shared').resolve_legend(shape='shared')
    # aggscores
    question_clusterAgg = atL1_evd_annpt.groupby('ClusterName')[score_cols].agg(['median','std']).\
    unstack().reset_index().pivot(index=['level_0','ClusterName'],columns='level_1',values=0)

    question_clusterAgg = question_clusterAgg.reset_index().rename({'level_0':'questions'},axis=1)

    question_clusterAgg = atL1_evd_annpt.groupby('ClusterName')[score_cols].agg(['median','std']).\
        unstack().reset_index().pivot(index=['level_0','ClusterName'],columns='level_1',values=0)

    question_clusterAgg = question_clusterAgg.reset_index().rename({'level_0':'questions'},axis=1)

    sepsis_plot3_1 =alt.Chart(question_clusterAgg,height=150,width=200).mark_square(filled=True).encode(
        y=alt.Y('questions',axis=alt.Axis(labelFontSize=14,labelLimit=500)),
        x=alt.X('ClusterName:O'),
        color=alt.Color("median",scale=alt.Scale(scheme="redblue",reverse=True,
                                                domainMin=0.5,domainMax=8,domainMid=4
                                                ,clamp=True),
                                legend=alt.Legend(
                                                direction="vertical",
                                                )
                                                ),
        size=alt.Size('std',scale=alt.Scale(reverse=True,nice=True),
                    legend=alt.Legend(direction="vertical",columns=2)),
        tooltip=["median","std"]
        )

    funct_bar = alt.Chart(atL1_evd_annpt.reset_index(),height=150,width=200).mark_bar().encode(
    x=alt.X('ClusterName:N',sort=sorted(list(color_key.keys())), axis=alt.Axis(title="Cluster",labelFontSize=14)),
    y=alt.Y('count(geneName)',axis=alt.Axis(title="Gene Count")),
    color=alt.Color('ClusterName:O',scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values())))
    )
    func_text = funct_bar.mark_text(
        align="center",
        baseline="middle",
        dy=-5,
        size=14
    ).encode(text="count(geneName)")
    sepsis_plot3_2  = funct_bar+func_text

    sepsis_plot3_right = alt.vconcat(sepsis_plot3_1,sepsis_plot3_2).resolve_scale("independent")

    return alt.hconcat(sepsis_plot3_lift, sepsis_plot3_right)


def moduleRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key):
    moduleID_agg = []
    for kname, kgrp in atL1_evd_annpt.groupby('ModuleID'):
        totalcount = kgrp.shape[0]
        total_geneinModule_base = geneBase[geneBase.ModuleID==kname].shape[0]
        tmp = {}
        for cname, cgrp in kgrp.groupby("ClusterName"):
            tmp={}
            tmp['ModuleID'] = kname
            tmp['c_id'] = cname
            tmp['ModuleTitle']=cgrp.ModuleTitle.unique()[0]
            tmp['AggregateNumber'] = cgrp.AggregateNumber.unique()[0]
            tmp['geneCount'] = cgrp.shape[0]
            tmp['geneFraction'] = cgrp.shape[0]/totalcount
            tmp['geneList'] = ",".join(list(cgrp.index))
            tmp['pct_geneModule'] = (cgrp.shape[0]/total_geneinModule_base)*100
            for k in score_cols:
                tmp[k] = cgrp[k].mean()

            moduleID_agg.append(tmp)

    module_agg_DF = pd.DataFrame(moduleID_agg)
    module_agg_DF = module_agg_DF.sort_values(by=['c_id','geneFraction'],ascending=[True,False]).reset_index().drop('index',axis=1)

    #plot 
    stackedBar = alt.Chart(module_agg_DF,height=300,width=900).mark_bar(filled=True,).encode(
    x=alt.X("ModuleID",sort=list(module_agg_DF.ModuleID.values),axis=alt.Axis(title="ModuleID",labels=False)),
    y=alt.Y("geneFraction"),
    color=alt.Color('c_id:O',scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values()))),
    tooltip=list(module_agg_DF.columns)
    )
    tCount = alt.Chart(module_agg_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("ModuleID",sort=list(module_agg_DF.ModuleID.unique()),axis=alt.Axis(title="ModuleID",labels=False)),
        y=alt.Y("sum(geneCount)"),
        tooltip=["ModuleID","sum(geneCount)"]
    )

    tCount_pct = alt.Chart(module_agg_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("ModuleID",sort=list(module_agg_DF.ModuleID.unique()),axis=alt.Axis(title="ModuleID",labels=False)),
        y=alt.Y("sum(pct_geneModule)"),
        tooltip=["ModuleID","sum(pct_geneModule)"]
    )

    moduleFracPlot = alt.vconcat(tCount_pct, tCount, stackedBar)
    return (moduleFracPlot)


def moduleTitleRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key):
    title_grp = []
    for kname, kgrp in atL1_evd_annpt.groupby('ModuleTitle'):
        totalcount = kgrp.shape[0]
        totalGene_moduleT = geneBase[geneBase.ModuleTitle==kname].shape[0]
        tmp = {}
        for cname, cgrp in kgrp.groupby("ClusterName"):
            tmp={}
            tmp['Title'] = kname
            tmp['ModuleAggregates'] = ",".join(cgrp.AggregateNumber.unique())
            tmp['ModuleIds'] = ",".join(cgrp.ModuleID.unique())
            tmp['c_id'] = cname
            tmp['geneCount'] = cgrp.shape[0]
            tmp['geneFraction'] = cgrp.shape[0]/totalcount
            tmp['geneList'] = ",".join(list(cgrp.index))
            tmp['pct_geneModuleTitle'] = (cgrp.shape[0]/totalGene_moduleT)*100
            for k in score_cols:
                tmp[k] = cgrp[k].mean()

            title_grp.append(tmp)

    title_grp_DF = pd.DataFrame(title_grp)
    title_grp_DF = title_grp_DF.sort_values(by=['c_id','geneFraction'],ascending=[True,False]).reset_index().drop('index',axis=1)


    titleList = list(title_grp_DF.Title.values)
    stackedBar = alt.Chart(title_grp_DF,height=300,width=900).mark_bar(filled=True,).encode(
        x=alt.X("Title",sort=titleList,axis=alt.Axis(title="Module Title",labels=True,labelFontSize=14,labelLimit=500)),
        y=alt.Y("geneFraction"),
        color=alt.Color('c_id:O',scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values()))),
        tooltip=list(title_grp_DF.columns)
    )

    tCount = alt.Chart(title_grp_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("Title",sort=titleList,axis=alt.Axis(title="",labels=False)),
        y=alt.Y("sum(geneCount)"),
        tooltip=["Title","sum(geneCount)","ModuleAggregates","ModuleIds"]
    )

    tCount_pct = alt.Chart(title_grp_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("Title",sort=titleList,axis=alt.Axis(title="",labels=False)),
        y=alt.Y("sum(pct_geneModuleTitle)"),
        tooltip=["Title","sum(pct_geneModuleTitle)","ModuleAggregates","ModuleIds"]
    )

    TitleFracPlot = alt.vconcat(tCount_pct, tCount, stackedBar)
    return (TitleFracPlot)


def aggregateRespPlots(atL1_evd_annpt,score_cols,geneBase,color_key):
    modaggregate_grp = []
    for kname, kgrp in atL1_evd_annpt.groupby('AggregateNumber'):
        totalcount = kgrp.shape[0]
        totalGene_aggregate = geneBase[geneBase.AggregateNumber==kname].shape[0]
        tmp = {}
        for cname, cgrp in kgrp.groupby("ClusterName"):
            tmp={}
            tmp['ModuleAggregate'] = kname
            tmp['ModuleTitle'] = ",".join(cgrp.ModuleTitle.unique())
            tmp['ModuleIds'] = ",".join(cgrp.ModuleID.unique())
            tmp['c_id'] = cname
            tmp['geneCount'] = cgrp.shape[0]
            tmp['geneFraction'] = cgrp.shape[0]/totalcount
            tmp['geneList'] = ",".join(list(cgrp.index))
            tmp['pct_geneAggregate'] = (cgrp.shape[0]/totalGene_aggregate)*100
            for k in score_cols:
                tmp[k] = cgrp[k].mean()

            modaggregate_grp.append(tmp)

    modaggregate_grp_DF = pd.DataFrame(modaggregate_grp)
    modaggregate_grp_DF = modaggregate_grp_DF.sort_values(by=['c_id','geneFraction'],ascending=[True,False]).reset_index().drop('index',axis=1)

    aggregateList = list(modaggregate_grp_DF.ModuleAggregate.values)
    stackedBar = alt.Chart(modaggregate_grp_DF,height=300,width=900).mark_bar(filled=True,).encode(
        x=alt.X("ModuleAggregate",sort=aggregateList,axis=alt.Axis(title="Aggregate",labels=False)),
        y=alt.Y("geneFraction"),
        color=alt.Color('c_id:O',scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values()))),
        tooltip=list(modaggregate_grp_DF.columns)
    )

    tCount = alt.Chart(modaggregate_grp_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("ModuleAggregate",sort=aggregateList,axis=alt.Axis(title="",labels=True)),
        y=alt.Y("sum(geneCount)"),
        tooltip=["ModuleAggregate","sum(geneCount)"]
    )

    tCount_pct = alt.Chart(modaggregate_grp_DF,height=100,width=900).mark_bar(filled=True,color="gray").encode(
        x=alt.X("ModuleAggregate",sort=aggregateList,axis=alt.Axis(title="",labels=True)),
        y=alt.Y("sum(pct_geneAggregate)"),
        tooltip=["ModuleAggregate","sum(pct_geneAggregate)"]
    )


    AggFracPlot = alt.vconcat(tCount_pct, tCount, stackedBar)
    # return AggFracPlot

    dx = modaggregate_grp_DF.groupby("ModuleAggregate")['pct_geneAggregate'].agg('sum').sort_values().to_frame()
    for kname, kgrp in modaggregate_grp_DF.groupby("c_id"):
        dx["Cluster_{}".format(kname)] =kgrp[['ModuleAggregate','pct_geneAggregate']].set_index('ModuleAggregate')

    dx = dx.reset_index().fillna(0)

    base = alt.Chart(dx,width=900, height=300).encode(alt.X('ModuleAggregate',sort=list(dx['ModuleAggregate'].values)))
    area = base.mark_area(opacity=0.3, color='#57A44C').encode(
        alt.Y('pct_geneAggregate')
        )

    stackedBarX = alt.Chart(modaggregate_grp_DF,width=900, height=300).mark_bar(filled=True,width=10).encode(
        x=alt.X("ModuleAggregate",sort=list(dx['ModuleAggregate'].values),axis=alt.Axis(title="Aggregate")),
        y=alt.Y("pct_geneAggregate",axis=alt.Axis(title="pct_gene in each cluster")),
        color=alt.Color('c_id:O',scale=alt.Scale(domain=list(color_key.keys()),range=list(color_key.values()))),
        tooltip=list(modaggregate_grp_DF.columns)
    )


    aggregate_stckedplot = alt.layer(stackedBarX,area).resolve_scale(
        y='independent'
    )
    return (AggFracPlot, aggregate_stckedplot)
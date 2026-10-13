"""Reproduce controles numéricos de estadística; no reemplaza la interpretación."""
from pathlib import Path
import json, statistics
import numpy as np,pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]

def calcular():
    valores=[120,80,450,60,230,90,1100,75,320,180,90,95,210,85,90]
    d=pd.read_csv(ROOT/'04_DATASETS/distribuidora/drop_por_pedido.csv').drop_bs
    q=d.quantile([.25,.5,.75,.9,.95]);iqr=q.loc[.75]-q.loc[.25]
    pilot=pd.read_csv(ROOT/'04_DATASETS/experimento_piloto.csv')
    a=pilot.loc[pilot.grupo=='A','ticket_bs'];b=pilot.loc[pilot.grupo=='B','ticket_bs']
    t=stats.ttest_ind(a,b,equal_var=False);ci=stats.t.interval(.95,len(a)-1,loc=a.mean(),scale=stats.sem(a))
    encuesta=pd.read_csv(ROOT/'04_DATASETS/encuesta_canales.csv')
    tabla=pd.crosstab(encuesta.grupo,encuesta.compra)[[1,0]].to_numpy()
    chi,p,df,expected=stats.chi2_contingency(tabla,correction=False)
    return {'ST01':{'media':statistics.mean(valores),'mediana':statistics.median(valores),'moda':statistics.mode(valores),'desv_muestral':statistics.stdev(valores)},'ST02':{'n':len(d),'media':d.mean(),'mediana':d.median(),'desv_muestral':d.std(),'percentiles':{str(k):float(v) for k,v in q.items()}},'ST03':{'IQR':iqr,'atipicos':int(((d<q.loc[.25]-1.5*iqr)|(d>q.loc[.75]+1.5*iqr)).sum()),'z_mayor_3':int((np.abs(stats.zscore(d))>3).sum()),'asimetria':d.skew()},'ST05':{'n_A':len(a),'n_B':len(b),'media_A':a.mean(),'media_B':b.mean(),'diferencia':a.mean()-b.mean(),'t_welch':t.statistic,'p':t.pvalue,'IC95_A':list(ci)},'ST06':{'tabla':tabla.tolist(),'chi2':chi,'p':p,'gl':int(df),'esperados':expected.tolist(),'V_Cramer':float(np.sqrt(chi/len(encuesta)))}}

if __name__=='__main__':print(json.dumps(calcular(),indent=2,ensure_ascii=False))

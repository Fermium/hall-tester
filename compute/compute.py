#importing package for r
import numpy
import readline
import csv
import os
import statsmodels.api as sm
import seaborn as sns


def compute(assets_path,data,x,y):
    Y=numpy.array([data[dd][y] for dd in data if data[dd] is not None])
    X=numpy.array([data[dd][x] for dd in data if data[dd] is not None])
    X_m=sm.add_constant(X)
    results = sm.OLS(Y, X_m).fit()
    intercept=results.params[0]
    slope=results.params[1]
    results.summary()
    sns.set()
    plot = sns.regplot(X,Y,scatter_kws={'color':'red','s':20})
    fig = plot.get_figure()
    fig.savefig(os.path.join(assets_path,  "plot.png"))
    test=dict()
    if(results.f_pvalue<=0.005):
        test['raw_data']={y:Y.tolist(),x:X.tolist()}
        test['coeff']={'intercept':intercept,'slope':slope}
        test['status']=True
        return test
    else:
        test['status']=False
        return test

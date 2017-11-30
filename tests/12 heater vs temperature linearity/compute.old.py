#importing package for r
import numpy
import readline
import rpy2.robjects as robj
import csv
import os

def compute(assets_path):
    r = robj.r
    #aliasing r funcions for faster usage
    summary = r['summary']
    coef = r['coef']
    attach = r['attach']
    read_csv = r['read.csv']
    deviance = r['deviance']
    dfres = r['df.residual']

    #importing ggplot2 for plots, if doesn't exist donwload it and then import it
    try:
        import rpy2.robjects.lib.ggplot2 as ggplot2
    except ImportError:
        utils = robj.packages.importr('utils')
        utils.install_packages('ggplot2')
        import rpy2.robjects.lib.ggplot2 as ggplot2
        
    #grdevices to plot to file
    grdevices = robj.packages.importr('grDevices')

    #loading and attaching 'output.csv' to model on that
    robj.globalenv['data'] = read_csv(os.path.join(assets_path , "output.csv"))
    data = robj.globalenv['data']
    attach(data)

    #first model, ch2=a+b*i
    model1 = r.lm('ch2~i')

    ch2vsi = coef(model1)
    ch2vsi[0] #intercept
    ch2vsi[1] #slope
    
    # Print graphs
    grdevices.png(file=os.path.join(assets_path,  "temp_vs_time.png"),width=512,height=512)
    gp = ggplot2.ggplot(data)
    pp = gp + \
        ggplot2.aes_string(x='i',y='ch2')+\
        ggplot2.geom_abline(intercept=ch2vsi[0],slope=ch2vsi[1],color='red')+\
        ggplot2.geom_line()+\
        ggplot2.ggtitle('ch2 over time')
    pp.plot()
    grdevices.dev_off()
    
    # If the model ( a line ) is a good model (meaning the data is very linear) pass the test
    if(r['pf'](summary(model1)[9][0],summary(model1)[9][1],summary(model1)[9][2],lower_tail=False)[0]<=0.005):
        return True
    else:
        return False

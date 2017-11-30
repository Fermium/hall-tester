#importing package for r
import numpy
import readline
import rpy2.robjects as robj
import csv
import os
import pickle


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

    #first model, ch3=a+b*raw_current_code
    model1 = r.lm('ch3~raw_current_code')

    ch3vsraw = coef(model1)
    ch3vsraw[0] #intercept
    ch3vsraw[1] #slope
    
    configuration = { "current_compensation_intercept": ch3vsraw[0], "current_compensation_slope" : ch3vsraw[1]}
    pickle.dump ( configuration, open(os.path.join(assets_path , "configuration.json"),"wb"))
    
    

    grdevices.png(file=os.path.join(assets_path,  "ch3vsraw.png"),width=512,height=512)
    gp = ggplot2.ggplot(data)
    pp = gp + \
        ggplot2.aes_string(x='raw_current_code',y='ch3')+\
        ggplot2.geom_abline(intercept=ch3vsraw[0],slope=ch3vsraw[1],color='red')+\
        ggplot2.geom_line()+\
        ggplot2.ggtitle('Ch3 vs Raw Current')
    pp.plot()
    grdevices.dev_off()
    
    if(r['pf'](summary(model1)[9][0],summary(model1)[9][1],summary(model1)[9][2],lower_tail=False)[0]<=0.005):
        return True
    else:
        return False
    #plot for visual check, red line is the fitting line and black is the data
    """
    #second model, raw_current_code=a'+b' * ch3
    model2 = r.lm('raw_current_code~ch3') # like the other model data here is in a straight line
    check2 = False
    if(r['pf'](summary(model2)[9][0],summary(model2)[9][1],summary(model2)[9][2],lower_tail=False)[0]<=0.005):
        check2=True

    rawvsch3 = coef(model2)
    rawvsch3[0]#intercept
    rawvsch3[1]#slope

    grdevices.png(file=os.path.join(assets_path,  "rawvsch3.png"),width=512,height=512)
    gp = ggplot2.ggplot(data)
    pp = gp + \
        ggplot2.aes_string(y='raw_current_code',x='ch3')+\
        ggplot2.geom_abline(intercept=rawvsch3[0],slope=rawvsch3[1],color='red')+\
        ggplot2.geom_line()+\
        ggplot2.ggtitle('Raw Current vs Ch3')
    pp.plot()
    grdevices.dev_off()"""
    #plot for visual check, red line is the fitting line and black is the data

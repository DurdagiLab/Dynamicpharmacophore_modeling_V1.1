#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:36:03 2023

@author: Ehsan.Sayyah
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import seaborn as sns
import os
import glob
import weasyprint
import numpy as np
from pypdf import PdfMerger


pathrmsd = input('Please write the path of your trjrmsd.dat file: \n')
pathrmsd = pathrmsd+'/trajrmsd.dat'

rmsd_data = pd.read_table(pathrmsd, sep="\s+")
rmsd_data = rmsd_data.iloc[:5001]
rmsd_data.sort_values(by=['mol0'], inplace=True)

path = input('Please write the path of your pharmacophore csv files: \n')
path = path+'/'
pathsave= input('Give a path to save your figures and pdf files: \n')
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
import re
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval
def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]
result.sort(key=natural_keys)
print(result)
ic=[]
features7=[]
features6=[]
features5=[]
features4=[]
features3=[]
f3=[]
f4=[]
f5=[]
f6=[]
f7=[]
ADDRR_index=[]
dups=0
for e in range(len(result)):
    path+=result[e]
    csv= pd.read_csv(path, sep=',', usecols=['Feature_label']).tail(10)
    if len(csv) == 2:
        print('low feature')
    if len(csv) == 3:
        features3.append(re.sub(r'[^A-Z]', '',(''.join(sorted(csv['Feature_label'][:3])))))
        f3.append(e)
    if len(csv) == 4:
        features4.append(re.sub(r'[^A-Z]', '',(' '.join(sorted(csv['Feature_label'][:4])))))
        f4.append(e)
    if len(csv) == 5:
        features5.append(re.sub(r'[^A-Z]', '',(' '.join(sorted(csv['Feature_label'][:5])))))
        # if re.sub(r'[^A-Z]', '',(' '.join(sorted(csv['Feature_label'][:5])))) == 'ADDRR' :
        #     ADDRR_index.append(e)
        f5.append(e)
    if len(csv) == 6:
        features6.append(re.sub(r'[^A-Z]', '',(' '.join(sorted(csv['Feature_label'][:6])))))
        f6.append(e)
    if len(csv) == 7:
        features7.append(re.sub(r'[^A-Z]', '',(' '.join(sorted(csv['Feature_label'][:7])))))
        f7.append(e)
    ic.append(csv)
    path = path.replace(result[e],'')
    
rmsd_data['Features']=pd.Series(dtype='int')
for z in rmsd_data['frame'] :
    if rmsd_data['frame'][z] != 0:
        path+= 'Hypothesis_{}_features_table.csv'.format(z)
        csv= pd.read_csv(path, sep=',', usecols=['Feature_label']).tail(10)
        ftr = list(csv['Feature_label'])
        rmsd_data.loc[z,'Features']=re.sub(r'[^A-Z]', '',(' '.join(sorted(ftr))))
        path = path.replace('Hypothesis_{}_features_table.csv'.format(z),'')

unique3=[]
unique4=[]
unique5=[]
unique6=[]
unique7=[]
uniques=[]
features = [features3,features4,features5,features6,features7]
def unique(features):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in features:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print (x)
        uniques.append(x)
    return uniques

unique3 = unique(features[0])
uniques=[]
unique4 = unique(features[1])
uniques=[]
unique5 = unique(features[2])
uniques=[]
unique6 = unique(features[3])
uniques=[]
unique7 = unique(features[4])

unq=[unique3,unique4,unique5,unique6,unique7]
ft=[]
cnt=[]

def featureinfo(unq,features):
    if len(unq):
        for b in unq:
            ft.append(b)
            cnt.append(features.count(b))
            info = pd.DataFrame({'Features': ft
                                 ,'counter': cnt})
    else:
        info= pd.DataFrame({'Features': '-'
                                 ,'counter': 0},index=['No Data'])
    return info

info3 = featureinfo(unq[0],features[0])
ft=[]
cnt=[]
info4 = featureinfo(unq[1],features[1])
ft=[]
cnt=[]
info5 = featureinfo(unq[2],features[2])
ft=[]
cnt=[]
info6 = featureinfo(unq[3],features[3])
ft=[]
cnt=[]
info7 = featureinfo(unq[4],features[4]) 

infoall = pd.concat([info3,info4,info5,info6,info7])
infoall = infoall.reset_index(drop=True)
inf=[info3,info4,info5,info6,info7]

def lowrmsd(inf):
    if inf['counter'][0] != 0 :
        count= inf.nlargest(2,['counter']).reset_index(drop=True)
        feat = count['Features']
        if len(feat) == 2:
            feat = count['Features'].reset_index(drop=True)
            findrmsd = rmsd_data.loc[rmsd_data['Features'] == feat[0]]
            minim=findrmsd.loc[findrmsd['mol0'].idxmin()]
            rmsdframe=minim['frame']
            findrmsd1 = rmsd_data.loc[rmsd_data['Features'] == feat[1]] 
            minim1=findrmsd1.loc[findrmsd1['mol0'].idxmin()]
            rmsdframe1=minim1['frame']
            rmsd = pd.concat([minim,minim1], axis=1)
            rmsd = rmsd.T
            rmsd['counter']=[count['counter'][0], count['counter'][1]]
            rmsd=rmsd.reset_index(drop=True)
        elif len(feat) == 1:
            findrmsd = rmsd_data.loc[rmsd_data['Features'] == feat[0]]
            minim=findrmsd.loc[findrmsd['mol0'].idxmin()]
            rmsdframe=minim['frame']
            rmsd = pd.concat([minim], axis=1)
            rmsd = rmsd.T
            rmsd['counter']=[count['counter'][0]]
            rmsd=rmsd.reset_index(drop=True)
    else:
        rmsd = pd.DataFrame({'Features': '-'
                            ,'counter': 0},index=['No Data'])
    return rmsd

bestframe3= lowrmsd(inf[0])
bestframe4= lowrmsd(inf[1])
bestframe5= lowrmsd(inf[2])
bestframe6= lowrmsd(inf[3])
bestframe7= lowrmsd(inf[4])
bestframe=[bestframe3,bestframe4,bestframe5,bestframe6,bestframe7]

pdfinfo=[]
v=3
for t in bestframe:
    if t.shape[1] == 4:
        data = 'lowest RMSD of the MD simulation for the best Features with {} Hypothesis is {} in {} frame which have {} Features and Total {} trajectory contain these Features'.format(v,t.iloc[0,1], t.iloc[0,0], t.iloc[0,2], t.iloc[0,3])
        v = v+1
        pdfinfo.append(data)
        pdfinfo.append('\n')
    elif t.shape[1] == 2:
        data = 'There is no {} Hypothesis in these trajectories'.format(v)
        v=v+1
        pdfinfo.append(data)
        pdfinfo.append('\n')
datafile = pd.DataFrame({'3.features': pdfinfo[0], '4.features': pdfinfo[2], '5.features': pdfinfo[4], '6.features': pdfinfo[6], '7.features': pdfinfo[8] }, index=['INFORMATION'])
datafile=datafile.T


def barplot(bestframe):
    if bestframe.shape[1] == 4:
        bar = plt.figure(dpi=200)
        sns.set_style('darkgrid')
        sns.barplot(x='frame', y='counter', hue='Features', data=bestframe, palette='viridis')
    else:
        bar = plt.figure(dpi=200)
        sns.set_style('darkgrid')
        sns.barplot(x='counter', y='counter', hue='Features', data=bestframe, palette='viridis') 
    return bar


plot3= barplot(bestframe[0])
plot4= barplot(bestframe[1])
plot5= barplot(bestframe[2])
plot6= barplot(bestframe[3])
plot7= barplot(bestframe[4])

infpie=[info3,info4,info5,info6,info7,infoall]
def pieplot(infpie):
    if infpie['counter'][0] != 0:
        data = infpie.nlargest(5, ['counter'])
        x= data['counter']
        y= data['Features']
        pie = plt.figure(dpi=200)
        palette_color = sns.color_palette('viridis')
        plt.pie(x, labels=y, colors=palette_color, autopct='%.0f%%')
        plt.savefig(pathsave+"/plots.pdf", format="pdf", bbox_inches="tight")
    elif infpie['counter'][0] == 0:
        x = []
        y = []
        pie = plt.figure(dpi=200)
        palette_color = sns.color_palette('viridis')
        plt.pie(x, labels= y, colors=palette_color)
        plt.savefig(pathsave+"/plots.pdf", format="pdf", bbox_inches="tight")  
    return pie

pie3= pieplot(infpie[0])
pie4= pieplot(infpie[1])
pie5= pieplot(infpie[2])
pie6= pieplot(infpie[3])
pie7= pieplot(infpie[4])
pieall= pieplot(infpie[5])

pp = PdfPages(pathsave+'/plots.pdf')
pp.savefig(plot3)
pp.savefig(plot4)
pp.savefig(plot5)
pp.savefig(plot6)
pp.savefig(plot7)
pp.savefig(pie3)
pp.savefig(pie4)
pp.savefig(pie5)
pp.savefig(pie6)
pp.savefig(pie7)
pp.savefig(pieall)
pp.close()

rmsd_data = rmsd_data.reset_index(drop=True)
intermediate_html = pathsave+'/intermediate.html'
intermediate1_html = pathsave+'/intermediate1.html'
intermediate2_html = pathsave+'/intermediate2.html'
infoall.to_html(intermediate_html)
datafile.to_html(intermediate1_html)
rmsd_data.to_html(intermediate2_html)

out_pdf= pathsave+'/data.pdf'
out_pdf1= pathsave+'/data1.pdf'
out_pdf2= pathsave+'/data2.pdf'
weasyprint.HTML(intermediate_html).write_pdf(out_pdf)
weasyprint.HTML(intermediate1_html).write_pdf(out_pdf1)
weasyprint.HTML(intermediate2_html).write_pdf(out_pdf2)

pdfs = [pathsave+'/data.pdf',pathsave+'/data1.pdf', pathsave+'/plots.pdf',pathsave+'/data2.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(pathsave+"/FeatureResult.pdf")
merger.close()

# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:53:28 2020

@author: azelle
"""

import numpy as np
from utils import distance_nuplet,region,getnext,buf,listpos,compute_zones


def compute_mean_dist_color(image):
    #A color constraint measure based on the mean distance to expected color
    value =0
    a=np.asarray(image)
    for elem in a: 
        for ele in elem:
            value +=min (distance_nuplet(ele,(255,0,0)),distance_nuplet(ele,(255,255,255)))
    return value/(len(a)*len(a[0]))


def compute_ratio_color(image):
    #A color constraint measure based on the ratio of not expected color
    value=0
    a=np.asarray(image)
    for elem in a: 
        for ele in elem:
            if not ((ele[0]==255 and ele[1]==0 and ele[2]==0) or (ele[0]==255 and ele[1]==255 and ele[2]==255)):
                value +=1
    return value/(len(a)*len(a[0]))

def compute_color(image):
    #A color constraint measure based on the ratio of pixel too far of the expected color 
    n=0
    a=np.asarray(image)
    for elem in a: 
        for ele in elem:
            if distance_nuplet(ele,(255,0,0))>9 and distance_nuplet(ele,(255,255,255))>9:
                n +=1
    return n/(len(a)*len(a[0]))


def  compute_position(ref, pred):
    #The measure of position accuracy
    ref=np.array(ref)
    pred=np.array(pred)
    cinter=0
    cunion=0
    for i in range  (len(ref)):
        for j in range(len(ref[i])):
            if ref[i][j]==1 and pred[i][j]==1: 
                cinter+=1
            if ref[i][j]==1 or pred[i][j]==1:
                cunion+=1
    return cinter/cunion

def compute_structure(rec, real):
    #measure the connectivity preservation
    (ar,ab)=region(real)
    (br,bb)=region(rec)
    return((abs(ar-br)+abs(ab-bb))/((ar+ab)))


def compute_noise(image,threshold):
    #measures the noise in an image
    im=np.asarray(image) 
    a=im.copy()
    blanc=0
    flag=np.zeros(image.size)
            
    for i in range(len(im)):
        for j in range(len(im[i])): 
            pix=a[i][j]
            if flag[i][j]==1 or pix==0:
                continue
            (flag,l)=getnext((i,j),pix,a,flag)
            if len(l)<threshold:
                blanc+=1
            if(len(flag[flag==0])==0):
                return blanc
    return blanc         

def compute_coalescense(image,v,img=False): 
    #measures the quantity of coalescence in an image
    a=buf(v,1,image) 
    b=buf(v+6,0,a) 
    c=buf(6,1,b)
    d=np.asarray(c)
    l=listpos(d,1)
    w=2+v
    nb=len(l)
    for elem in l:
        (i,j)=elem
        im=image.crop((i-w,j-w,i+w,j+w))
        (blanc,noir)=compute_zones(im,0)
        if blanc>1:
            nb=nb-1 
    if img:
        
        return (nb,c)
    else: 
        return nb

def compute_smoothness(image,img=False):
    #measures the quantity of irregulare pixels in an image
    tt=len(listpos(np.asarray(image),1))
    a=buf(3,1,image)
    b=buf(3,0,a)
    c=np.asarray(b)
    value =len(listpos(c,1))-tt
    if img:
        
        return (value,b)
    else: 
        return value

# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:53:28 2020

@author: azelle
"""

import os 
from PIL import Image
import numpy as np

from skimage.measure import label
from skimage import filters
from skimage.color import rgb2gray



def distance_nuplet(a,b):
    #compute the distance between to nuplet
    s=0
    for i in range (len(b)):
        s+=(a[i]-b[i])**2
    s=(s**0.5)/len(a)
    return s



def listpos(npim,sign):
    #list the position of element of value sign in npim
    l=[]
    for i in range (len(npim)): 
        for j in range (len(npim[i])):
            if npim[i][j]==sign:
                l+=[(i,j)]
    return l


def lista_porte(pix,size,npix): 
    #calculate the list of pixel at a distance smaller than npix from pix.
    (i,j)=pix
    npix+=1
    li=[]
    for k in range(npix):
        for l in range (npix-k):
            if i-k>=0 and j-l>=0:
                li+=[(i-k,j-l)]
            if j+l<size and i+k<size:
                li+=[(i+k,j+l)]
            if i-k>=0 and j+l<size:
                li+=[(i-k,j+l)]
            if i+k<size and j-l>=0 :
                li+=[(i+k,j-l)]
    return  list(set(li))  


def buf(nPix,sign,image):
    #calculate the image of the buffer of size nPix around pixel of value sign in image. 
    im=np.asarray(image)
    lInit=listpos(im,sign)
    for elem in lInit:
        lporte=lista_porte(elem,len(im),nPix)
        for pix in lporte: 
            (i,j)=pix
            image.putpixel((j,i),sign)
    return image



def region(A):
    #calculate the background and road sets. 
    img=np.asarray(A)
    grayscale = rgb2gray(img)

    try:
        thresh = filters.threshold_otsu(grayscale)
    except: 
        return(0,1)
    bw = grayscale> thresh
    (a,background)=label(bw, connectivity=2,return_num=True,background=0)
    (a,road)=label(bw, connectivity=2,return_num=True,background=1)
    return(road,background)



 

def compute_zones(image,threshold):
    #compute pixel sets consider only those above threshold.
    im=np.asarray(image) 
    a=im.copy()
    listdenoir=[]
    listdeblanc=[]
    blanc=0
    noir=0
    flag=np.zeros(image.size)

    for i in range(len(im)):
        for j in range(len(im[i])): 
            pix=a[i][j]
            if flag[i][j]==1:
                continue
            (flag,l)=getnext((i,j),pix,a,flag)
            if pix==1:
                if len(l)>threshold:
                    blanc+=1
                listdeblanc.append(l)
            else:
                if len(l)>threshold:
                    noir+=1
                listdenoir.append(l)
            
            if(len(flag[flag==0])==0):
                return(blanc,noir)


def getnext(init,color,im,flag):
    
    (i,j)=init
    flag[i][j]=1
    l=[init]
    v=list_near(init,color,im,flag)
    l+=v
    for elem in v: 
        (i,j)=elem
        flag[i][j]=1    
    while v!=[]:
        vcopy=list(set(v))
        v=[]
        for elem in vcopy: 
            v+=list(set(list_near(elem,color,im,flag)))
        for elem in v: 
            (i,j)=elem
            flag[i][j]=1
        l+=list(set(v))
        vcopy=[]
    return (flag,l) 




def list_near(pixpos,color,im,flag):   
    (i,j)=pixpos
    size=len(im)
    l=[]
    if i<size-1:
        if im[i+1][j]==color:
            l.append((i+1,j))
    if j<size-1:
        if im[i][j+1]==color:
            l.append((i,j+1)) 
    if i>0 and im[i-1][j]==color:
        if flag[i-1][j]==0:
            l.append((i-1,j))
    if j>0 and im[i][j-1]==color:
        if flag[i][j-1]==0:
            l.append((i,j-1))
    return l             



def apply_by_windows(example_folder): 
    #permits to compute coalescence on each windows instead of images. 
    for im in os.listdir(example_folder):
        print(im)
        image=(Image.open(example_folder+'\\'+im))
        l=slidding_windows(40,20,image)
        summ =0
        for elem in l:
            (value,image)=compute_coalescense(elem)
            summ+=value
        print(summ)


def slidding_windows(taille,pas,image):
    #splits an image according a slidding windows
    listimg=[]
    n=image.size[0]
    for i in range (int((n-taille)/pas)):
        for j in range (int((n-taille)/pas)):
            a=image.crop((i*pas,j*pas,i*pas +taille,j*pas+taille))
            listimg.append(a)
    return listimg


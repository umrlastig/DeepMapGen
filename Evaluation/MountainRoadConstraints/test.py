# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:34:02 2020

@author: ACourtial
"""
import constraints as cst
import os 
from PIL import Image

import csv



folder_img='.//data//real//'
file_eval='.//eval.csv'
folder_seg='.//data//seg//'

def savebinary(init_folder,dest): 
    #this function permit to save image created using  make_binary.
    for im in os.listdir(init_folder):
        a= make_binary(Image.open(init_folder+'\\'+im))
        a.save(dest+im)                      
                      
def distance_nuplet(a,b):
    s=0
    for i in range (len(b)):
        s+=(a[i]-b[i])**2
    s=(s**0.5)/len(a)
    return s

def make_binary(image):
    #this function permits to transform a colored image into a mask of road position. 
    imageb=Image.new('1', image.size, (0))
    for i in range(image.width): 
        for j in range(image.height):
            ele=image.getpixel((i,j))
            if ele[0] == 255 and ele[1]==255 and ele[2]==255: 
                imageb.putpixel((i,j),0)
            elif ele[0] == 255 and ele[1]==0 and ele[2]==0 :
                imageb.putpixel((i,j),1)
            else :
                dist_red=distance_nuplet(ele,(255,0,0))
                dist_white=distance_nuplet(ele,(255,255,255))
                if dist_red<dist_white:
                    imageb.putpixel((i,j),1)
                else:
                    imageb.putpixel((i,j),0)
    return imageb

if __name__ == '__main__':
    savebinary(folder_img,folder_seg)

    with open(file_eval, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Image','Color','Noise','Continuity','Position','Coalescence','Smoothness'])

    for nom in os.listdir(folder_img): 

        rep=[nom[:len(nom)-10]]
        pred_image=Image.open(folder_img+nom)
        pred_seg=Image.open(folder_seg+nom)
        ref_seg=Image.open(folder_seg+'r'+nom[1:len(nom)])
        rep+=[cst.compute_color(pred_image)]
        rep+=[cst.compute_noise(pred_seg,6)]
        rep+=[cst.compute_structure(ref_seg,pred_seg)]
        rep+=[cst.compute_position(ref_seg,pred_seg)]
        rep+=[cst.compute_coalescense(pred_seg,5)]
        rep+=[cst.compute_smoothness(pred_seg)]
        with open(file_eval, 'a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(rep)
        
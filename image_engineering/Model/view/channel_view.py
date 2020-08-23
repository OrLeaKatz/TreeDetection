from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import math



def channel_view (img , save_path, max_col = 5 ):
    obj = Image.open(img) 
    obj = np.array(obj)
    #obj = np.random.rand(300,300, 16)
    channe_num = obj.shape[-1]
    
    fig_H = obj.shape[0]*(max_col)*1.3/100
    fig_W = obj.shape[1]*(math.ceil(channe_num/max_col))*1.3/100
    
    
    #fig = plt.figure(figsize = (max_col*4,channe_num))
    fig = plt.figure(figsize = (fig_H,fig_W))
    plt.axis('off')
    ax = []
    hight = math.ceil(channe_num/float(max_col))
    for i in range(channe_num):
        print (i)
        ax.append(fig.add_subplot(hight , max_col, i + 1))
        ax[-1].set_title("channel#" + str(i+1))
        ax[-1].axis('off')
        ax[-1].imshow(obj[:,:,i])


    try:
        plt.savefig(save_path+ 'out3.png' , bbox_inches='tight')
    except:
        print ("err saving image")

channel_view( r"C:\Users\abed\Desktop\project\func\imgs\face.png", max_col = 6)
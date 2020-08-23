import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


  
def display_img (**kargs ):
    """
    function recieves numpyarray and imag path and displays thoes as images in plot

    Parameters
    ----------
    **kargs : NumPy array , img path
        DESCRIPTION.

    Returns
    -------
    None.

    """
    l = len(kargs.items())
    # prepering the image to be desplayed
    img_list = []
    a= tuple(range(3))
    for i, (name, obj) in enumerate(kargs.items()):
        
        #checks if path is a file
        if(isinstance(obj, str)) and (os.path.isfile(obj)) :
            
            obj = Image.open(obj) 
            obj = np.array(obj)
                 

        # check if obj is np array
        # we try to display numpy array where the channels are always the in th last index
        if (type(obj).__module__ == np.__name__):
            pass
    
            if (len(obj.shape)==2): # W,S
                pass 
            
            elif(len(obj.shape)==3): 
                pass
            
                if obj.shape[2]==3:                 #CASE W,H,3
                    pass
                
                elif obj.shape[0]==3:               #CASE 3,W,H
                    obj = np.transpose(a, (2,0,1))  #CASE W,H,3
                    
                elif obj.shape[-1] == 4:            #CASE W,H,4
                    obj = obj[:,:,0:3]              #CASE W,H,3
                    
                elif  obj.shape[0] == 4:            #CASE 4,W,H
                    obj = np.transpose(a, (2,0,1))  #CASE W,H,4
                    obj = obj[0:3,:,:]              #CASE W,H,3
                    
        img_list.append(obj)
                

    fig = plt.figure(figsize = (20,3*l))
    ax= []
    
    for i, img in enumerate(img_list):
        ax.append(fig.add_subplot( 1 , l, i + 1))
        ax[-1].set_title("img" + str(i+1))
        ax[-1].imshow(img)
        
    plt.show()
        
        
        
def channel_view (img , save_path, max_col = 5 ):
    """
    channel displays  image with each channel as seperate image  on plt

    Parameters
    ----------
    img : String
        image path
    save_path : String
        directory to save image
    max_col : int, optional
        how many columns the plt should have. The default is 5.

    Returns
    -------
    None.

    """
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
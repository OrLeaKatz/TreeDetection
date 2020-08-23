from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt



def display_img (**kargs ):
    plt_size = 100,100
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
                
    #fig, ax = plt.subplots(nrows=1, ncols=l)  #for i, axi in enumerate(ax.flat):
    fig = plt.figure(figsize = (20,3*l))
    ax= []
    
    # for i, axi in enumerate(plt.gcf().get_axes()):
    #     axi.set_title("img" + str(i+1))        
    #     axi.imshow(obj)
        
    for i, img in enumerate(img_list):
        ax.append(fig.add_subplot( 1 , l, i + 1))
        ax[-1].set_title("img" + str(i+1))
        ax[-1].imshow(img)
        
       
       
    plt.show()
        
    
        
        
    #for axi, obj in  lz:
        #axi.imshow(obj)
        
    
                

def force_np(**kwarg):
    '''
    # INPUT  -> array or image-as-array or path-to-img 
    # OUTPUT -> array (W,H) or (3,W,H)
    '''
    pass


display_img(arg = r"C:\Users\abed\Desktop\project\test\AND.png" ,
            arg1 =r"C:\Users\abed\Desktop\project\test\OR.png",
            arg2 =r"C:\Users\abed\Desktop\project\test\replace.png")

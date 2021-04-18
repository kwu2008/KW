
from ipywidgets import *
import ipywidgets as widgets

def f(x):
    return x

def Interact_Demo():
    
    interact(f, x=10)
    interact(f, x=True)
    interact(f, x=['abc', 'xyz']) 



if __name__ == '__main__':
        Interact_Demo()
        


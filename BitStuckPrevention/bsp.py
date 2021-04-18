import sys
import os

def BSP_LoadData():
    print('BSP_LoadData')

    cwd = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(cwd, 'S-503000-523000.csv')

    print('Opening file ' + filePath + '...')

    fileSrc = open(filePath, 'r')

    print(fileSrc.read())



def BSP_ProcessData():
    print('BSP_ProcessData')


def BSP_DisplayData():
    print('BSP_DisplayData')


def BSP_Main():
    print('BSP_Main')
    BSP_LoadData()
    BSP_ProcessData()
    BSP_DisplayData()
 

if __name__ == '__main__':
        BSP_Main()



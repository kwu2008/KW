import matplotlib.pyplot as plt
import numpy as np


def Scatter_Demo():
    N = 100

    X = np.random.rand(N)
    Y = np.random.rand(N)

    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2

    plt.figure( figsize=(15,8) )
    plt.scatter(X, Y, s=area, c=colors, alpha=0.5)
    plt.show()


def Chart_Demo():

    Scatter_Demo()


if __name__ == '__main__':
        Chart_Demo()


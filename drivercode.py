import threading
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from GAcode import *

# POINTS = {
#     'A':(33,7),
#     'B':(9.8,1),
#     'C':(29,5),
#     'D':(14,15.4),
#     'E':(27,17),
#     'F':(42,23),
#     'G':(43,2),
#     'H':(17,21),
#     'I':(22,1),
#     'J':(23,7),
# }


# points = list(POINTS.values())
# labels= POINTS.keys()

NO_OF_POINTS = 30
points = [(random.uniform(0,100),random.uniform(0,100)) for _ in range(NO_OF_POINTS)]
labels = [i for i in range(1,NO_OF_POINTS+1)]

bestcurrentorder = [i for i in range(len(points))]
X_values = [p[0] for p in points]
Y_values = [p[1] for p in points]

terminate_flag = threading.Event()

def myGeneticAlgo(path,points,populationSize,noOfCities):
    genetic=Genetic(path,points,populationSize,noOfCities)
    genetic.createInitialPopulation()
    while not terminate_flag.is_set():
        genetic.createNewGeneration()
        global bestcurrentorder
        bestcurrentorder= genetic.record_path
        #print(genetic.record_path," and ",genetic.record_distance," and ",bestcurrentorder)


def updatePlot():
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('close_event', on_close)
    while not terminate_flag.is_set():
        #print(bestcurrentorder)
        printedorder = bestcurrentorder[:]
        ax.clear()
        ax.scatter(X_values,Y_values)
        for i, txt in enumerate(labels):
            ax.annotate(txt, (X_values[i], Y_values[i]), textcoords="offset points", xytext=(0,10), ha='center')
        
        for i in range(len(printedorder) - 1):
            ax.plot([X_values[printedorder[i]], X_values[printedorder[i+1]]], [Y_values[printedorder[i]], Y_values[printedorder[i+1]]], 'r-')
        
        # Connect the last point to the first point to form a closed path (if needed)
        ax.plot([X_values[printedorder[-1]], X_values[printedorder[0]]], [Y_values[printedorder[-1]], Y_values[printedorder[0]]], 'r-')
    
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.pause(0.5)
    plt.close()

def on_close(event):
    global terminate_flag
    terminate_flag.set()
    genetic_thread.join()

# Create a thread for running the algorithm
genetic_thread = threading.Thread(target=myGeneticAlgo, args=(bestcurrentorder,points,100,len(points)))
genetic_thread.start()

updatePlot()
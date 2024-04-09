import random
import math
import heapq
import bisect

class Genetic:
    def __init__(self,record_path=[],points=[],populationSize=0,no_of_cities=0):
        self.points=points
        self.population=[]
        self.population_size=populationSize
        self.record_path=record_path
        self.record_distance=float('inf')

        self.fitness=[0 for i in range(self.population_size)]
        
        self.MUTILATIONRATE=0.2
        self.NO_OF_CITIES=no_of_cities
        self.NO_OF_ELITES = 20
        
        

    def createInitialPopulation(self):
        for i in range(self.population_size):
            shuffledorder = self.record_path[:]
            random.shuffle(shuffledorder)
            self.population.append(shuffledorder)

    def calcFitness(self):
        sum=0
        for i in range(self.population_size):
            distance=self.calcDistance(self.population[i])
            # print(self.population[i])
            # print(distance," distance    |    record distance ",self.record_distance)
            if (distance<self.record_distance):
                self.record_distance=distance
                self.record_path=self.population[i]

            self.fitness[i]= 1/(distance+1) #the plus one is just to avoid divide by zero error
            sum+=self.fitness[i]

        #now, to normalize the fitness
        for i in range(self.population_size):
            self.fitness[i]=self.fitness[i]/sum


    def crossover(self, newGeneration, idx):
        orderA=newGeneration[idx]
        orderB=newGeneration[idx+1]
        child1=[None]*len(orderA)
        child2=[None]*len(orderB)
        selected_size = math.floor(self.NO_OF_CITIES/3)
        start_idx = random.randint(0,self.NO_OF_CITIES-selected_size)

        child1[start_idx:start_idx+selected_size]=orderA[start_idx:start_idx+selected_size]
        child2[start_idx:start_idx+selected_size]=orderB[start_idx:start_idx+selected_size]
        index=0
        #kinda ugly change later
        for i in range(len(orderB)):
            if orderB[i] in child1:
                continue
            
            while child1[index]!=None:
                index+=1
            
            if index>=len(orderB):
                break
                
            child1[index]=orderB[i]
        
        index=0
        for i in range(len(orderA)):
            if orderA[i] in child2:
                continue
            
            while child2[index]!=None:
                index+=1
            
            if index>=len(orderA):
                break
                
            child2[index]=orderA[i]
        newGeneration[idx]=child1
        newGeneration[idx+1]=child2


    def mutatue(self, newGeneration):
        for i in range(self.population_size):
            randomprob = random.random()
            if randomprob<self.MUTILATIONRATE:
                # randomno is the no of times we want to swap to mutate.
                randomno= random.randint(math.floor(self.NO_OF_CITIES/10),math.floor(self.NO_OF_CITIES/5)) # 1 to 2 mutations possible
                for i in range(randomno):
                    indxA = random.randint(0,self.NO_OF_CITIES-1)
                    indxB = random.randint(0,self.NO_OF_CITIES-1)
                    #now we swap whatever is in the two indices
                    temp = newGeneration[i][indxA]
                    newGeneration[i][indxA]=newGeneration[i][indxB]
                    newGeneration[i][indxB]=temp

    def createNewGeneration(self):
        self.calcFitness()
        newGeneration=[]
        topelites=TopKHeap(self.NO_OF_ELITES)
        for i in range(self.population_size):
            topelites.push(self.fitness[i],self.population[i])
        
        elites = [x[1] for x in topelites.get_top_k()]
        #just storing the elites
        
        # finding the cumulative fitness so that we can sample the rest
        for i in range(1,self.population_size):
            self.fitness[i]+=self.fitness[i-1]
        
        for i in range(self.population_size-self.NO_OF_ELITES):#cuz we also have our elites that we have to store
            random_no=random.random()
            idx = bisect.bisect_right(self.fitness,random_no)
            newGeneration.append(self.population[idx])
        
        #now we have to crossover
        for i in range(0,len(newGeneration)-1,2):
            self.crossover(newGeneration,i)

        #now we add the elites then mutate.
        newGeneration.extend(elites)
        self.mutatue(newGeneration)
        
        self.population = newGeneration

    def calcDistance(self,order) -> float:
        d=0
        for i in range(len(order)-1,-1,-1): # the end is -1 as we have to include 0
            d+= math.sqrt(math.pow(self.points[order[i]][0]-self.points[order[i-1]][0],2)+math.pow(self.points[order[i]][1]-self.points[order[i-1]][1],2))
        
        return d

class TopKHeap:
    def __init__(self, k):
        self.heap = []
        self.k = k

    def push(self, fitness, orderidx):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (fitness,orderidx))
        else:
            # If the heap is full, push the number if it's greater than the smallest number in the heap
            min_fitness,_ = self.heap[0]
            if fitness > min_fitness:
                heapq.heappop(self.heap)
                heapq.heappush(self.heap, (fitness,orderidx))

    def get_top_k(self):
        return sorted(self.heap, reverse=True)


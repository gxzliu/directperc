# *******************************************************
# vertperc
# george liu
# date: 4.10
# functions that create, manipulate, and plot the dynamics
# within site vacancy matrices and flow matrices
# *******************************************************

import numpy as np
import matplotlib.pyplot as plt

def read_file(infile):
    """
    Create a site vacancy matrix represented as a numpy array 
    from a text file with the name infile_name.
    """

    invalue = open(infile, 'r')
    #read the first line, which contains # of col/rows
    dimension = int(invalue.readline())
    listvalue = []
    
    #reads the content, cleans, and appends to listvalue
    content = invalue.read().rstrip('\n').split()
    listvalue.append(content)  
    
    #strips each values of the quotations surrounding them
    cleanvalue = [[int(i) for i in l] for l in listvalue]
    
    #adds cleavalue to array and shapes array
    a = np.array(cleanvalue)
    a.shape = (dimension, dimension)
        
    return a


def write_file(outfile,sites):
    """
    Write a site vacancy matrix from the numpy array sites 
    to a file of name outfile. 
    """

    outval = open(outfile, 'w')
    #prints out # of col/rows first
    print(sites.shape[0], file = outval)

    #go thru each row in matrix
    for row in range(sites.shape[0]):
        content = ""
        #go thru each value in each row and add to string
        content = ' '.join([str(int(i)) for i in sites[row]]) + ' '
        print(content, file = outval)
    outval.close()


def dir_flow(sites):
    """
    Function takes in a numpy array representing a site vacancy matrix
    and returns a corresponding flow matrix of vacant/full sites 
    (1=full, 0=vacant), generated through directed percolation.
    """
    #sets flow matrix size equal to site matrix size
    flowm = np.zeros(sites.shape)
    
    #goes along perc possibilities stemming from top row
    for s in range(len(sites)):
        flow_from(sites, flowm, 0, s)
        
    return flowm
    

def flow_from(sites,full,i,j):
    """
    Adjusts the full array for flow from a single site
    """
    
    #make sure points are within boundaries
    if (i < sites.shape[0]) and (j < sites.shape[0]):
        if (i >= 0 and j >= 0):
            #make sure vacant, not blocked, and empty, not full
            if sites[i,j] == 1 and full[i,j] != 1:
                full[i,j] = 1
                #checks everywhere but up since directed flow
                flow_from(sites, full, i + 1, j)
                flow_from(sites, full, i, j + 1)
                flow_from(sites, full, i, j - 1)



def percolates(flow_matrix):
    """
    Returns a boolean if the flow_matrix numpy array exhibits percolation
    """
    
    dimension = len(flow_matrix)
    #checks for fluid in last row of flow matrix
    sol = bool(sum(flow_matrix[dimension-1])>0)
    return(sol)
    
    
def make_matrix(n,p):
    """
    Returns an numpy array representing an nxn site vacancy 
    matrix w/ site vacancy prob p
    """
    
    #creates a random array with n*n dimensions
    matrix = np.random.rand(n*n)
    matrix.shape = (n,n)
    matrix = matrix < p
    #makes sure matrix is 0/1 not T/F
    matrix = matrix.astype(int)
    
    return matrix


def perc_visual(sites):
    """
    Visualizes undirected flow on the matrix sites
    """
    
    #sites to determine vacant/blocked, directed_flow to determine fullness
    plt.matshow(sites + dir_flow(sites))
    #blue = 0 = blocked, green = 1 = vacant, red = 2 = full
    plt.title('Matrix: B=Blocked, G=Vacant, R=Full')
    plt.show()
    

def make_graph(n,trials):
    """
    Generates a graph of percolation p vs. vacancy p. Estimates 
    percolation probability for directed percolation 
    thru a Monte Carlo simulation
    """
    
    #creates array for percolation probability
    percprob = np.zeros(25)
    
    #creates array for vacancy probability
    vacprob = np.linspace(0, 1, 25)
    
    #counter to move through percprob array
    y = 0
    
    for v in vacprob:
        #counter for successful percolations
        perc = 0
        
        for t in range(trials): 
            #generates site vacancy matrix
            vacmat = make_matrix(n,v)
            write_file('sites.txt',vacmat)
            #returns corresponding flow matrix
            percmat = dir_flow(read_file('sites.txt'))
            if percolates(percmat):
                perc += 1
        #point at y has x-value of # of percs so far / # of trials
        percprob[y] = (perc/trials)
        y += 1
    
    
    #outputs plot
    plt.plot(vacprob, percprob)
    plt.xlabel('Vacancy Probability')
    plt.ylabel('Percolation Probability')
    plt.title('Percolation Probability and Vacancy Probability')
    plt.show()
    
    
    
    
    
    
    
    
    
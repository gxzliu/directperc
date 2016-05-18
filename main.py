#*******************************************************
# vertperc
# george liu
# date: 4.10
# main method
#*******************************************************


import directperc as perc

def main():
    a=perc.make_matrix(30,0.55)
    perc.write_file('sites.txt',a)
    b=perc.read_file('sites.txt')
    c=perc.dir_flow(b)
    if perc.percolates(c):
        print('percolates')
    else:
        print('does not percolate')
    
    #visualize flow
    perc.perc_visual(b)
    
    #generate percolation probability graph
    perc.make_graph(10,500)

main()

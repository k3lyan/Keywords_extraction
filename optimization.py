def density(output_density):
    D_n=[]
    for V_E in output_density:
        if(V_E[1]>1):
            D_n.append([V_E[0], V_E[2]/(V_E[1]*(V_E[1]-1))])
        else:
            D_n.append([V_E[0],0])
    print('D_n: ', D_n)
    return(D_n)

def elbow_function(D_n):
    if(len(D_n) > 2):
        a_equation = (D_n[0][1]-D_n[-1][1])/(D_n[0][0]-D_n[-1][0])
        b_equation = (D_n[0][1]-D_n[0][0]*a_equation)
        distance = {}
        s = 0
        for (x,y) in D_n:
            distance[s] = (abs((a_equation*x+b_equation-y)/(((a_equation**2)+(1)))**(1/2)))
            s += 1
        distance = sorted(distance, key = distance.get, reverse=True)
        if(distance[0] != distance[1]):
            return(distance[0])
        else:
            return(0)
    else:
        if(len(D_n) > 2 == 1):
            return(D_n[0][0])
        else:
            return(max(D_n[0][0],D_n[1][0]))

def get_optimized_nb_keywords(output_density, density_applied):
    if(density_applied):
        D_n = density(output_density) 
        print('elbow_function(D_n): ', elbow_function(D_n))
        return(output_density[elbow_function(D_n)])
    else:
        CD = []
        n = 1
        for i in range(len(output_density)-1):
            CD.append(output_density[i+1][1]-output_density[i][1])
        for i in range(2,len(CD)-1):
            if(CD[i+1]<0 and CD[i]>0):
                n = i
        return(output_density[n][1])


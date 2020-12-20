import numpy as np
import random as rnd
import main as pso_main
#import mainTestPso as pso_main

# classe particella, entità che si muoveranno nello spazio 7-dimensionale
class Particle:
    # _ndim => indica il numero di dimensioni dello spazio => nel nostro caso 7
    # nhood_size => numero di particelle che rientrano nell'insime dei "vicini"
    def __init__(self, _ndim, nhood_size):
        self.fit = 0        # valore di fitness per la singola particella
        self.fitnbest = 0   # miglior valore di fitness tra i vicini 
        self.fitbest = 0    # miglior valore di fitness tra tutte le particelle
        
        # inizializzo la velocità
        self.v = np.zeros(_ndim, dtype=np.float)
        # inizializzo il valore della posizione
        self.x = np.zeros(_ndim, dtype=np.float)
        # migliore posizione pbest
        self.xbest = np.zeros(_ndim, dtype=np.float)
        # migliori posizioni dei vicini
        self.nxbest = np.zeros(_ndim, dtype=np.float)
        # array contenente gli indici delle particelle vicine => 
        #  l'indice si riferisce alla posizione della particella vicina nell'array pop
        self.nset = np.zeros(nhood_size, dtype=np.int)
   
# classe Particle Swarm Optiomization        
class ParSwarmOpt :
    '''
        - x indica la posizione nello spazio; per noi sono le 7 percentuali, hanno dei massimi e minimi
        - _xmin => valore minimo per la posizione; nel nostro caso sarà 0.05
        - _xmax => valore massimo per la posizione; nel nostro caso sarà 0.70
    '''
    def __init__(self, _xmin, _xmax, _processor, _portfolioKeys):
        # sono valori condivisi da tutte le particelle
        self.c0 = 0.25 # coefficiente della velocità
        self.c1 = 1.5  # coefficiente relativo alla posizione xbest
        self.c2 = 2.0  # coefficiente relativo alla posizione nxbest
        self.fitbest = -np.inf # migliore fitness
        self.xmin = _xmin # mi porto dietro il valore minimo che può assumere per fare dei controlli
        self.xmax = _xmax # mi porto dietro il valore massimo che può assumere per fare dei controlli
        self.sum_c = 1.0 # somma delle componenti del vettore posizione
        self.processor = _processor #elemento ForecastsProcessor da passare alla funzione compute_fitness
        self.portfolioKeys = _portfolioKeys # array contenente nomi di indici da passare a compute_fitness
        self.gbestDictionary = {} # mi porto dietro l'evoluzione del gbest, per debug
        self.lastFitnessComputationRes = {} # quando calcolo la fitness mi faccio restituire un dizionario che contiene anche valore di stdev e mediamobile questa è una variabile d'appoggio
        self.gbestFitnessComputationRes = {} # FitnessComputationRes relativo al gbest
        '''
            lastFitnessComputationRes e gbestFitnessComputationRes contengono le seguenti info:
                "fitness" : valore di fitness
                "media_mobile" : media_mobile,
                "risk" : stdev
        '''
     
    # genera un attay contenente numvar componenti di intervallo [0.05,0.7] 
    # che possono costituire la posizione iniziale per una particella
    def generateStartPoint(self, numvar):
        res = [0.05]*numvar
        toAssign = round(1-(0.05*numvar),2)
    
        for i in range(numvar-1):
            # percentuale da assegnare
            pToAssign = rnd.randrange(0,(100-(numvar*7)))/100 #percentuale di toAssign che verrà attribuita al prossimo elemento
            valueToAssign = round((pToAssign*toAssign),2) # calcolo l'ammontare da assegnare corrispondete alla percentuale individuata
            toAssign -= valueToAssign # sottraggo la quota da assegnare all'ammontare di partenza
            res[i] += valueToAssign # asegno la quota
            
        res[numvar-1] += toAssign # all'ultimo elemento di res va tutta la quota restante
    
        return res
    
    
    # prende l'array arr e trasforma il valore dei suoi elementi in modo tale che la loro somma faccia 1 
    def fixSum1(self, arr):
        temp = []
        for elem in arr:
            temp.append(elem/sum(arr)) 
        return temp
    
    # arr è una posizione feasible se, i suoi elementi sommano ad 1 e apprtengono a [xmin,xmax] 
    def isPositionFeasible(self, arr):
        for e in arr:
            if e<self.xmin or e>self.xmax: return False
        if sum(arr) > 1.0000000000000002 or sum(arr)<0.9999999999999999: return False
        return True
    
    # modifico le componenti del vettore posizione arr in modo tale che rispettino i vincoli
    def setMinMax(self, arr):
        temp = []
        for e in arr: # per ogni componente e del vettore posizione arr
            if e<self.xmin :
                temp.append(self.xmin) # se e è più piccolo del minimo lo setto al minimo consentito (0.05)
            elif e>self.xmax:
                temp.append(self.xmax) # se e è maggiore del massimo lo setto al massimo consentito (0.7)
            else: temp.append(e)
        return temp
    
    # coordina un processo ricorsivo che permette di spostare particelle finite fuori dominio all'interno del dominio di ricerca
    def fixPosition(self, arr, numvar):
        cont = 0
        while (not self.isPositionFeasible(arr)) and cont<100: #conteggio a 100 serve questa funzione ha una convergenza lenta, in questo modo evitiamo problemi
            arr = self.fixSum1(arr)
            arr = self.setMinMax(arr)
            cont += 1
            if cont > 100: print("errore!! ", cont)
        if not self.isPositionFeasible(arr): # in caso non si sia raggiunta una convergenza in 100 iterazioni, generiamo una nuova posizione per la particella
            return self.generateStartPoint(numvar)
        return arr 
    
    # controlla se la posizione della particella è feasible, se non lo è modifica i vettori posizione(x) e velocità(v)
    def fixParticleXV(self, particle, numvar):
        if not self.isPositionFeasible(particle.x): 
            for i in range(numvar): # aggiorno componenti del vettore velocità 
                if particle.x[i]<self.xmin or particle.x[i]>self.xmax: particle.v[i] = -particle.v[i]
            particle.x = self.fixPosition(particle.x, numvar) #aggiorno vettore posizione
    
              
    '''
        Algoritmo pso:
        - popsize = numero di particelle
        - numvar = sono le dimesioni (nel nostro caso saranno 7)
        - niter = numero di iterazioni da compiere per ottimizzazione
        - nhood_size = numero di particelle considerate far parte del neighborhood
    '''
    def pso_solve(self, popsize, numvar, niter, nhood_size):
        rnd.seed(550)
        self.xsolbest = np.zeros(numvar, dtype=np.float)
        
        #------------------------------INIZIALIZZAZIONE----------------------------------------
        
        ''' inizializzo le particelle che costituiscono la mia popolazione '''
        pop = [] # array contenente le particelle 
        for i in range(popsize): # istanzio n particelle (con n==popsize)
            pop.append(Particle(numvar, nhood_size))
            
        ''' per ogni particella istanziata provvedo a inizializzare i valori di posizione e velocità '''
        for i in range(popsize):
            # posizioni e velocità sono array di n elementi (dove n == numsize) => necessario ciclare
            pop[i].x = self.generateStartPoint(numvar)# inizializzo i valori della posizione
            for j in range(numvar): 
                #pop[i].x[j] = self.generateStartPoint(numvar) # inizializzo i valori della posizione 
                pop[i].v[j] = (rnd.random()-rnd.random())*0.5*(self.xmax-self.xmin)-self.xmin # inizializzo i valori della velocità 
                pop[i].xbest[j] = pop[i].x[j] # inizializzo la posizione migliore, dandogli il valore di quella corrente
                pop[i].nxbest[j] = pop[i].x[j] # inizializzo la posizione migliore nel neighborhood, dandogli il valore di quella corrente della particella
            
            # inizializzo valori di fitness
            self.lastFitnessComputationRes = pso_main.compute_fitness(pop[i].x, self.processor, self.portfolioKeys)
            pop[i].fit = self.lastFitnessComputationRes["fitness"] # chiamando fit su una particella chiamerò compute_fitness(posizione_particella)
            pop[i].fitbest = pop[i].fit # inizializzo la fitness migliore di quella particella con il primo valore
            
            '''
                le particelle sono contenute nell'array pop quindi sono identificate dal loro indice 
                che è [0,(popsize-1)] == range(popsize); 
                
                non conoscendo i vicini di ogni particella, inizialmente inseriamo all'interno dell'array dei
                vicini nset degli indici random di particelle tra quelli compresi in range(popsize)
                
                while else permette di evitare che l'estrazione randomica porti a inserire due volte la 
                stessa particella nell'array
            '''
            for j in range(nhood_size):
                id = rnd.randrange(popsize)
                while (id in pop[i].nset): 
                    id = rnd.randrange(popsize)
                else :
                    pop[i].nset[j] = id
                
        #------------------------------Runniamo Codice ----------------------------------------
        for iter in range(niter):
            print("---------------iterazione{0}----fitbest{1}---------------------".format(iter, self.fitbest))
            # aggiorna tutte le particelle [popsize == n°particelle]
            for i in range(popsize):
                # per ogni dimensione [numvar == n° dimensioni (7)]
                for d in range(numvar):
                    # aggiorno i coefficienti stocastici come da slide 9
                    rho1 = self.c1 * rnd.random()
                    rho2 = self.c2 * rnd.random()
                    
                    # aggiorno la velocità: nuova_velocità = f'(velocità_attuale) + f''(pbest) + f'''(lbest) => vedi slide 9
                    pop[i].v[d] = self.c0 * pop[i].v[d] +  rho1 * (pop[i].xbest[d] - pop[i].x[d]) + rho2 * (pop[i].nxbest[d] - pop[i].x[d]) 
                    
                    # aggiorno la posizione
                    pop[i].x[d] += pop[i].v[d] 
                    
                # controlla feasibility della posizione della particella, eventualmente modifica vettori posizione e velocità
                self.fixParticleXV(pop[i], numvar) 

                # aggiorno il valore di fitness associato alla particella
                self.lastFitnessComputationRes = pso_main.compute_fitness(pop[i].x, self.processor, self.portfolioKeys)
                pop[i].fit = self.lastFitnessComputationRes["fitness"]

                
                ''' aggiorno i valori di fitness: particle.fitbest, particle.fitnbest, ParSwarmOpt.fitbest'''

                # aggiorno il valore di miglior posizione assunta (qualora sia il caso)
                if(pop[i].fit > pop[i].fitbest):
                    pop[i].fitbest = pop[i].fit # aggiorno il miglior valore di fitness mettendolo uguale a quello attuale
                    for j in range(numvar):
                        pop[i].xbest[j] = pop[i].x[j] # aggiorno la pbest mettendola uguale a quella attuale
                        
                # aggiorno neighborhood best (lbest)
                pop[i].fitnbest = -np.inf
                for j in range(nhood_size): # per ogni neighbor => pop[pop[i].nset[j]] è il vicino j-esimo
                    if(pop[pop[i].nset[j]].fit > pop[i].fitnbest):
                        pop[i].fitnbest = pop[pop[i].nset[j]].fit # aggiorno il miglior valore di nfitness mettendolo uguale a quello attuale del vicino j-esimo
                        for k in range (numvar): # aggiorno il valore della posizione corrispondente al valore fitnbest
                            pop[i].nxbest[k] = pop[pop[i].nset[j]].x[k]
                            
                # aggiorno gbest
                if(pop[i].fit > self.fitbest):
                    # aggiorna best fitness
                    self.fitbest = pop[i].fit
                    # copia la posizione della particella nel vettore gbest
                    for j in range(numvar):
                        self.xsolbest[j] = pop[i].x[j]
                    self.gbestDictionary["{0}".format(self.fitbest)] = [iter, self.xsolbest]
                    self.gbestFitnessComputationRes = self.lastFitnessComputationRes

        #------------------------------Restituiamo il risultato ----------------------------------------     
        return {
            "fitbest" : self.fitbest, 
            "xsolbest" : self.xsolbest, 
            "history":self.gbestDictionary,
            "media_mobile" : self.gbestFitnessComputationRes["media_mobile"],
            "stdev" : self.gbestFitnessComputationRes["risk"]
        }       
                    
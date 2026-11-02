from model.model import Model
modello_prova = Model()

print(f"La lista che contiene tutti i nodi (non filtrati) è lunga: {len(modello_prova.lista_nodi_totale)}")
#creo il grafo:
modello_prova.crea_grafo("USA")
print(f"Il grafo ha {modello_prova.num_nodi()} nodi, e {modello_prova.num_archi()} archi")


lista_nodi = list(modello_prova._grafo.nodes())
nodo0 = lista_nodi[0]
nodo1 = lista_nodi[1]
nodo2 = lista_nodi[2]

print(nodo0.numero_copie)





#CONTROLLA CHE LA RICORSIONE DIA TUTTI I VINCOLI SIANO GIUSTI E RESTITUISCONO TRUE
soluzione = modello_prova.crea_albero(nodo0, 2)
print(soluzione)

#print("Parte dalla sorgente:", soluzione[0] == nodo1)

#print("Nodi non ripetuti:", len(soluzione) == len(set(soluzione)))

#for i in range(len(soluzione)-1):
    #u = soluzione[i]
    #v = soluzione[i+1]

    #print("Arco valido:", modello_prova._grafo.has_edge(u, v))

    #print("Fatturati validi:",
          #modello_prova.fatturato_nodo(u) >=
          #modello_prova.fatturato_nodo(v))
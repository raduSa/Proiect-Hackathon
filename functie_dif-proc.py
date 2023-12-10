def lista_store(prod_x):
    for store in prod_x.keys():
        luna = 1
        while store[luna] == None:
            luna += 1
        else:
            vinit = store[luna]
        for x in store.keys():
            if store[x] != None:
                store[x] = (store[x] - vinit)*100/vinit

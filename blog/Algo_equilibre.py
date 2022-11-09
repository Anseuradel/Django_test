import threading
import sys
import time
import random
import pandas as pd
import numpy as np

GlobalVar = [
    {
        "name" : "T1",
        "vehicules" : 5,
        "vehicule_dispo": 5,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    }, 
    {
        "name" : "T2",
        "vehicules" : 3,
        "vehicule_dispo": 3,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    },
    {
        "name" : "T3",
        "vehicules" : 4,
        "vehicule_dispo": 4,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    },
    {
        
        "name" : "T4",
        "vehicules" : 2,
        "vehicule_dispo": 5,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    }, 
    {
        "name" : "T5",
        "vehicules" : 6,
        "vehicule_dispo": 3,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    },
    {
        "name" : "T6",
        "vehicules" : 4,
        "vehicule_dispo": 4,
        "nbre_transport": 0,
        "nbre_demande_exclusif": 0,
        "ratio" : 0
    }]


def liste_dispatch(x,marge):
    DFT_sorted = x.sort_values(by =["ratio"],ascending = False)
    toBeInvoked = []
    index1 = 0
    while (index1  < len(DFT_sorted)) :
        index2 = index1 + 1
        origin_index1 = DFT_sorted.index[index1]
        exclude = False
        while (index2  < len(DFT_sorted)): 
            origin_index2 = DFT_sorted.index[index2]
            c = (DFT_sorted["ratio"][origin_index1] - DFT_sorted["ratio"][origin_index2])
            if(c >= marge):
                exclude = True
                break;
            index2 = index2 + 1    
        if(exclude == False):
            toBeInvoked.append(origin_index1) 
        index1 = index1 + 1
    return(toBeInvoked)

#a = formule2(GlobalVar, marge_param)
#display(GlobalVar("T2")("name").index)

'''def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()'''

def course_en_cour(index, lock):
    global GlobalVar
    #print("thread: {} started".format(threading.current_thread().name))
    time.sleep(random.randint(10, 30))
    lock.acquire()
    if (GlobalVar[index]["vehicule_dispo"] < GlobalVar[index]["vehicules"]):
        GlobalVar[index]["vehicule_dispo"] = GlobalVar[index]["vehicule_dispo"] + 1
        displayInfo('ride terminated', GlobalVar[index])
    lock.release()
    
    
    #print("thread: {} finished".format(threading.current_thread().name))
    return

def propose_course(index, lock):
    marge_param = 0.5
    nbr_course_a_proposer = 10
    global GlobalVar
    for i in range(nbr_course_a_proposer):
        #print("nbre_total_course = "+str(i)) 
    #while(ind < nbr_de_transport):
        df = pd.DataFrame(GlobalVar)
        a = liste_dispatch(df,marge_param)
        if(len(a) == 0):
            course_dispatched = False
            while(course_dispatched != True):
                index = np.random.randint(0,len(GlobalVar))
                #GlobalVar[index]["nbre_vehicule_dispo"] = GlobalVar[index]["nbre_vehicule_dispo"] + 1
                lock.acquire()
                if(GlobalVar[index]["vehicule_dispo"] != 0):
                    GlobalVar[index]["vehicule_dispo"] = GlobalVar[index]["vehicule_dispo"] - 1
                    GlobalVar[index]["nbre_transport"] = GlobalVar[index]["nbre_transport"] + 1
                    GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
                else:
                    GlobalVar[index]["nbre_demande_exclusif"] = GlobalVar[index]["nbre_demande_exclusif"] + 1 
                    GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
            print(df)
            lock.release()
            threading.Thread(target=course_en_cour, args=(index, lock)).start()
            time.sleep(random.randint(1, 10))
        elif(len(a) > 1):
            i = np.random.randint(0,len(a))
            index = a[i]
            lock.acquire()
            if(GlobalVar[index]["vehicule_dispo"] != 0):
                GlobalVar[index]["vehicule_dispo"] = GlobalVar[index]["vehicule_dispo"] - 1
                GlobalVar[index]["nbre_transport"] = GlobalVar[index]["nbre_transport"] + 1
                GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
            else:
                GlobalVar[index]["nbre_demande_exclusif"] = GlobalVar[index]["nbre_demande_exclusif"] + 1 
                GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
            print(df)
            #displayInfo('start ride type 2', GlobalVar[index])
            lock.release()
            threading.Thread(target=course_en_cour, args=(index, lock)).start()
            time.sleep(random.randint(1, 10))
        else:
            index = a[0]
            d = GlobalVar[index]["vehicules"] - GlobalVar[index]["vehicule_dispo"]
            if(d != GlobalVar[index]["vehicules"]):
                lock.acquire()
                if(GlobalVar[index]["vehicule_dispo"] != 0):
                    GlobalVar[index]["vehicule_dispo"] = GlobalVar[index]["vehicule_dispo"] - 1
                    GlobalVar[index]["nbre_transport"] = GlobalVar[index]["nbre_transport"] + 1
                    GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
                else:
                    GlobalVar[index]["nbre_demande_exclusif"] = GlobalVar[index]["nbre_demande_exclusif"] + 1 
                    GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]
                print(df)
                #displayInfo('start ride type 3', GlobalVar[index])
                lock.release()
                threading.Thread(target=course_en_cour, args=(index, lock)).start()
                time.sleep(random.randint(1, 10))
            else:               
                GlobalVar[index]["nbre_demande_exclusif"] = GlobalVar[index]["nbre_demande_exclusif"] + 1
            GlobalVar[index]["ratio"] = (GlobalVar[index]["nbre_transport"] + GlobalVar[index]["nbre_demande_exclusif"])/GlobalVar[index]["vehicules"]  

def displayInfo(text, entreprise):
    print("{} ===> Entreprise: {}, Nbr Vehicle: {}, Vehicle Disponible: {}".format(text, entreprise["name"], entreprise["vehicules"], entreprise["vehicule_dispo"]))
    
if __name__ == '__main__':
    lock = threading.Lock()
    i=0
    for idx, x in enumerate(GlobalVar):
        threading.Thread(target=propose_course, args=(idx, lock)).start()
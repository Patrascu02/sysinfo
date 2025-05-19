import subprocess
import re

'''
Functie gaseste_rute:

OS suportat: Linux
Verificat pe Ubuntu 20.04

Se executa comanda route -n si se preia rezultatul.
Din text-ul rezultat se creaza o lista de dictionare. 
Numarul de elemente din lista va fi egal cu numarul de rute.
Pentru fiecare ruta, avem un dictionar cu chei date de parametrii rutei:
    - Destination
    - Gateway
    - Genmask
    - Flags
    - Metric
    - Ref
    - Use
    - Iface 

parametrii: -

return: lista de dictionare
        pentru fiecare ruta se creeaza un dictionar cu cheile de mai sus    
'''
def gaseste_rutele():
    ret = []

    out_bin = subprocess.run(['route', '-n'], capture_output=True).stdout
    out_asc = out_bin.decode('ascii')
    
    #procesare text returnat de comanda 'route -n'
    out_lst = out_asc.split("\n")
    
    lst_chei = out_lst[1].split()
    #print("DBG:", lst_chei)

    for i in range(2, len(out_lst)):
        #print("DBG:", out_lst[i])
        d = {}
        lst_rand = out_lst[i].split()
        if len(lst_rand) < len(lst_chei):
            print("WARNING: gaseste_rute - rand gol:", i, lst_rand)
            continue
        else:
            pass
            #print("DBG:", lst_rand)
        for j in range(0, len(lst_chei)):
            #print(lst_chei[j], lst_rand[j])
            d[lst_chei[j]] =  lst_rand[j]
        
        ret.append(d)

    #print("DBG:", ret)
    return ret
    
'''
Functie: gaseste_linkuri:

OS suportat: Linux
Verificat pe Ubuntu 20.04

Se executa comanda 'ip link' si se preia rezultatul.
Din text-ul rezultat se creaza o lista de dictionare. 
Numarul de elemente din lista va fi egal cu numarul de interfete.
Pentru fiecare interfata, vom avea in lista un dictionar cu parametrii si 
valorile pentru fiecare parametru.

parametrii: -

return: lista de dictionare
        pentru fiecare link se creeaza un dictionar cu chei - numele 
        parametrilor link-ului din ip link si valori - valorile acestor 
        parametrii.  
'''    
def gaseste_linkuri():
    ret = []

    try:
        out_bnr = subprocess.run(['ip', '-j', 'link'], capture_output=True).stdout
        out_str = out_bnr.decode('ascii').strip()
    
        out_lst = eval(out_str)
    except Exception as e:
        print(e)
        out_lst = "EROARE executie comanda: 'ip -j link'"
 
    #print(out_lst)
    return out_lst

'''
Functie gaseste_adrese:

OS suportat: Linux
Verificat pe Ubuntu 20.04

Se executa comanda 'ip -j address' si se preia rezultatul.
Din text-ul rezultat se creaza o lista de dictionare. 
Numarul de elemente din lista va fi egal cu numarul de interfete.
Pentru fiecare interfata, vom avea in lista un dictionar cu parametrii si 
valorile pentru fiecare parametru.

parametrii: -

return: lista de dictionare
        pentru fiecare adresa se creeaza un dictionar cu chei
        numele parametrilor din comanda ip address si cu valori, valorile
        acestora.    
'''  
def gaseste_adrese():
    ret = []

    true = True

    try:
        out_bnr = subprocess.run(['ip', '-j', 'address'], capture_output=True).stdout
        out_str = out_bnr.decode('ascii').strip()
    
        out_lst = eval(out_str)
    except Exception as e:
        print("Eroare executie comanda 'ip -j address'", e)
        out_lst = ["Eroare executie comanda 'ip -j address'"]
        try:
            out_bnr = subprocess.run(['ip', 'address'], capture_output=True).stdout
            out_str = out_bnr.decode('ascii').strip()
            #de procesat, acum intoarcem un sir:
            out_lst = out_str
        except Exception as e:
            print("Eroare executie comanda: 'ip address': ", e)
            out_lst = "Eroare executie comanda: 'ip address'"
 
    #print("DBG:", out_lst)
    return out_lst



def gaseste_spatiu_liber():
    retr = []

    out_bin = subprocess.run(['df', '-h'], capture_output=True).stdout
    out_asc = out_bin.decode('utf-8')

    out_lst = out_asc.strip().split("\n")

    if len(out_lst) < 2:
        return ["Nu s-au putut extrage date"]

    for i in range(1, len(out_lst)):
        lst_rand = out_lst[i].split()
        if len(lst_rand) >= 6:
            retr.append({
                "Filesystem": lst_rand[0],
                "Size": lst_rand[1],
                "Used": lst_rand[2],
                "Avail": lst_rand[3],
                "Use%": lst_rand[4],
                "Mounted_on": lst_rand[5]
            })
        else:
            print("WARNING: rand incomplet:", i, lst_rand)

    if not retr:
        return ["Nu s-au gasit date despre spatiul liber."]
    
    return retr




'''
Functie genereaza_tabela_ruteL

Formateaza dictionarul de rute returnat de functia 'gaseste_rute'
si-l prezinta sub o forma mai simplificata, pentru a putea fi afisat mai 
usor.
'''
def genereaza_tabela_rute(rute, *param):
    lret = []
    # Functia care returneaza rutele are mai multi parametrii pentru fiecare ruta
    # 
    chei = rute[0].keys()
    
    l_param = []
    
    if param == ():
        l_param = ["Destination", "Gateway", "Genmask", "Iface"]
    elif param == ("all"):
        l_param = list(chei)
        
    lret.append(l_param)
            
    for r in rute:
        r_lst = []
        for c in l_param:
            r_lst.append(r[c])

        #print("DBG:", r_lst)
        lret.append(r_lst)

    ret = "<pre>\n"
    for el in lret:
        ret += str(el) + "\n"
    ret += "</pre>"
        
    #print("DBG:", ret)
    return ret

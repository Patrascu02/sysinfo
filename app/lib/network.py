import subprocess
import re

def gaseste_rute():
    '''
    Functie gaseste_rutele:

    OS suportat: Linux
    Verificat pe Ubuntu 20.04

    Se executa comanda route -n si se preia rezultatul.

    parametrii: -

    return: lista de dictionare
            pentru fiecare ruta se creeaza un dictionar cu cheile de mai sus    
    '''
    ret = []

    out_bin = subprocess.run(['route', '-n'], capture_output=True).stdout
    out_asc = out_bin.decode('ascii')
    
    return out_asc
    
    
def gaseste_linkuri():
    '''
    Functie: gaseste_linkuri:

    OS suportat: Linux
    Verificat pe Ubuntu 20.04

    Se executa comanda 'ip link' si se preia rezultatul.

    parametrii: -

    return: lista de dictionare
            pentru fiecare link se creeaza un dictionar cu chei - numele 
            parametrilor link-ului din ip link si valori - valorile acestor 
            parametrii.  
    '''
    ret = []

    try:
        out_bnr = subprocess.run(['ip', 'link'], capture_output=True).stdout
        out_str = out_bnr.decode('ascii').strip()
    
    except Exception as e:
        out_str = "EROARE executie comanda: 'ip link': " + str(e)
 
    return out_str


def gaseste_adrese():
    '''
    Functie gaseste_adrese:

    OS suportat: Linux
    Verificat pe Ubuntu 20.04

    Se executa comanda 'ip address' si se preia rezultatul.

    parametrii: -

    return: lista de dictionare
            pentru fiecare adresa se creeaza un dictionar cu chei
            numele parametrilor din comanda ip address si cu valori, valorile
            acestora.    
    '''  
    ret = []

    true = True

    try:
        out_bnr = subprocess.run(['ip', 'address'], capture_output=True).stdout
        out_str = out_bnr.decode('ascii').strip()
        
    except Exception as e:
        #print("Eroare executie comanda: 'ip address': ", e)
        out_str = "Eroare executie comanda: 'ip address': " + str(e)
 
    #print("DBG:", out_lst)
    return out_str


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


import subprocess

def timp_pornire_sys():
    rezultat = subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip()
    try:
       
        parts = rezultat.split(" up ")
        ora_curenta = parts[0].strip()

        rest = parts[1]
        uptime_part, rest = rest.split(",", 1)
        
        rest_parts = rest.strip().split(",")
        nr_utilizatori = rest_parts[0].strip()
        
        load_avg_str = rest.split("load average:")[-1].strip()
        load_1, load_5, load_15 = [x.strip() for x in load_avg_str.split(",")]

        return (
            f"Ora curenta: {ora_curenta}\n"
            f"Timp de functionare: {uptime_part.strip()}\n"
            f"Numar utilizatori conectati: {nr_utilizatori}\n"
            f"Incarcare medie (1 min): {load_1}\n"
            f"Incarcare medie (5 min): {load_5}\n"
            f"Incarcare medie (15 min): {load_15}"
        )

    except Exception as e:
        return f"Eroare la parsare uptime: {str(e)}\nRezultat brut:\n{rezultat}"




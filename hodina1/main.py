pravBreh = {"farmar": False, "koza": False, "vlk": False, "zeli": False}

# Podminky
def podminky(stav):
    if pravBreh["koza"] == pravBreh["vlk"] and pravBreh["koza"] != pravBreh["farmar"]:
        return False
    elif pravBreh["koza"] == pravBreh["zeli"] and pravBreh["koza"] != pravBreh["farmar"]:
        return False
    else: 
        return True
    
def presunKozy():
    pravBreh["farmar"] =not(pravBreh["farmar"])
    pravBreh["koza"] = not(pravBreh["koza"]) 

def presunVlk():
    pravBreh["farmar"] =not(pravBreh["farmar"])
    pravBreh["vlk"] = not(pravBreh["vlk"])

def presunZeli():
    pravBreh["farmar"] =not(pravBreh["farmar"])
    pravBreh["zeli"] = not(pravBreh["zeli"])




while (True):

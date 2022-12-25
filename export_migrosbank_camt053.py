# -*- coding: utf-8 -*-
# AMTQ - 25.12.2022
"""
Skript für die Verarbeitung von CAMT053-Dateien der Migrosbank in eine vernünftige Form als DataFrame
und anschliessender Export als Excel.
Getestet mit Export Migrosbank Stand 25.12.2022, AMTQ.
"""



from iso_camt053_to_df import camt2df
from pathlib import Path
from tqdm import tqdm


# Wo liegen die zu verarbeitenden Dateien
sourcepath = Path(Path.cwd().parents[0], Path(r'00 Daten\0 zu verarbeiten'))

# Wohin sollen die verarbeiteten Dateien wegsortiert werden
wegsortierpath = Path(Path.cwd().parents[0], Path(r'00 Daten\5 bereits verarbeitet'))
wegsortieren = False

# Wo sollen die exportierten Dateien gespeichert werden
zielpfad = Path(Path.cwd().parents[0], Path(r'50 Export'))

# Was für Dateien sollen berücksichtigt werden
source_pattern = 'CAMT053*.xml' # CAMT053*.xml ist NICHT rekursiv! Rekursiv wäre: '**/CAMT053*.xml'. 










def pfad_umwandeln(p_orig, zielpfad='', zielname='', zielendung='', modus='einfach'):
    if zielpfad == '': zielpfad = p_orig.parent
    if zielname == '': zielname = p_orig.stem
    if zielendung == '': zielendung = p_orig.suffix
        
    if modus == 'einfach':
        p_ziel =  str(zielname) + zielendung
    elif modus == 'VersionierungTag':
        zeitstring = time.strftime("%Y-%m-%d")
        p_ziel = str(zielname) + '_' + zeitstring + zielendung
    elif modus == 'Versionierung':
        zeitstring = time.strftime("%Y-%m-%d_%H-%M-%S")
        p_ziel = str(zielname) + '_' + zeitstring + zielendung
    elif modus == 'VersionierungPlus':
        zeitstring = time.strftime("%Y-%m-%d_%H-%M-%S")
        p_ziel = zeitstring + "_" + p_orig.stem + "_" + str(zielname) + zielendung
    else:
        errstr = 'modus ' + modus + ' wurde nicht definiert.'
        raise ValueError(errstr)# https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
    # print(zielpfad, p_ziel)
    p = zielpfad / p_ziel
    return p



filepaths = sorted(sourcepath.glob(source_pattern)) # sorted ist wichtig, da der Generator sonst weg ist nach dem ersten Aufruf
alle_df = []
if len(filepaths) == 0: 
    print(f'Keine Dateien zum Bearbeiten gefunden in\n{sourcepath}\n### Skript wird abgebrochen. ###')
else:
    for p_orig in tqdm(filepaths):
        print('p_orig:', p_orig)
        df = []
        df = camt2df(p_orig)
        alle_df.append(df)
        p_ziel = pfad_umwandeln(p_orig, zielpfad, zielendung='.xlsx')
        
        # print(p_orig, '\n-->', p_ziel,'\n')
        df = df.sort_values(['Datum', 'IBAN', 'Betreff', 'Stichwort'], ascending=False)
        df.drop_duplicates(inplace=True)
        
        df.to_excel(p_ziel, index=False)
            
        if wegsortieren:
            p_wegsortier = wegsortierpath.joinpath(p_orig.name)
            p_wegsortier = pfad_umwandeln(p_orig, wegsortierpath, modus='einfach')
            p_orig.replace(p_wegsortier) # Originaldateien wegverschieben
    
    if len(filepaths) > 1:
        df_alles = pd.concat(alle_df).sort_values(['Datum', 'IBAN', 'Betreff', 'Stichwort'], ascending=False)
        df_alles.drop_duplicates(inplace=True)
        p_ziel_alles = pfad_umwandeln(p_ziel, zielname='CAMT053', modus='einfach')
        df_alles.to_excel(p_ziel_alles, index=False)

    

#%%
# DEBUG

    # dd['entry_details'][4][0]['batch']['number_of_transactions'] # ergibt die Anzahl Transaktionen pro Batch
    # dd['entry_details'][4][0]['transactions'][i] # ergibt Transaktion i aus einem Batch 


# # Iterieren durch ein dict https://www.tutorialspoint.com/How-to-recursively-iterate-a-nested-Python-dictionary
# def iterdict(d):
#     for k,v in d.items():        
#        if isinstance(v, dict):
#            iterdict(v)
#        elif isinstance(v, list):
#            print('Achtung, ist eine Liste:', v)
#            for el in v:
#                if isinstance(el, dict):
#                    iterdict(el)
#                else:
#                    print(el)
    
#        else:            
#            print (k,":",v)
    
#     return

# # iterdict(x)

# -*- coding: utf-8 -*-
"""
# iso_camt053_to_csv

**WARNING! This library does not guarantee completenes and may contain bugs. Use at your own risk.**

 Export data from standardized ISO CAMT053 to something human-readable.
 
 Convert export-files from e-banking of Migrosbank in the format ISO CAMT053
 to pandas DataFrame.
 Why choose this xml-format in the first place? Because all other proposed 
 export formats from Migrosbank (pdf, csv) do contain less information
 information than the xml-files. However, even here some information visible 
 in e-banking is not contained in the files, for whatever reason.
 
 This library has been specifically created for files of Migrosbank. It *may*
 work with other files in the same guise, but nothing has been tested.
 
 AMTQ - 25.12.2022
"""

from pathlib import Path
import pandas as pd


from sepa import parser
import re
import time


pd.set_option('mode.chained_assignment','raise')


#%% Funktionsdefinitionen     
# Utility function to remove additional namespaces from the XML
def strip_namespace(xml):
    return re.sub(' xmlns="[^"]+"', '', xml, count=1)


# Extract remittance information from transactions
def extract_rem_inf2(dd_flattened):
    cleaned_list = []
    for j in range(len(dd_flattened)):
        try:
            info = dd_flattened['remittance_information'][j]['unstructed'][0]
            # print(j, info)
        except:
            info = ''
            # print(j, 'did not work')
        
        cleaned_list.append(info)
        # print(j, info)
    return cleaned_list
        
# Extract Stichwörter from transactions
def extract_Stichwort2(dd_flattened):
    cleaned_list = []
    for j in range(len(dd_flattened)):
        try:
            info = dd_flattened['refs'][j]['instruction_id']
            
        except:
            info = ''
        
        cleaned_list.append(info)
        # print(j, info)
    return cleaned_list




def camt2df(source):
    """
    Convert export-files from e-banking of Migrosbank in the format ISO CAMT053
    to pandas DataFrame.
    Why choose this xml-format in the first place? Because all other proposed 
    export formats from Migrosbank (pdf, csv) do contain less information
    information than the xml-files. However, even here some information visible 
    in e-banking is not contained in the files, for whatever reason.
    
    This library has been specifically created for files of Migrosbank. It *may*
    work with other files in the same guise, but nothing has been tested.
                                

    Parameters
    ----------
    source : Path-Object to xml-File or a filepath as string
        The file content must match:
            - XML Version 1.0, Encoding UTF-8
            - xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.04"
        File must be from the type "Bank to Customer Statement" <BkToCstmrStmt>
        
        Whether it works with exports from other Banks is unknown, it has only
        been tested with xml-Files of Migros Bank Schweiz.

    Returns
    -------
    df_entries : Pandas DataFrame including all transactions
        A dataframe is generated including all transactions from the input-file.
        The columns contain information about each transaction (if available in original file)
            IBAN of the concerned bank account
            Währung (currency) of the transaction
            Datum (date) of the transaction
            Betreff (subject) of the transaction
            Betrag (amount) in + (credit) or - (debit) of the transaction
            Stichwort (keyword) of the transaction
            Mitteilung an Empfänger (remittance information) of the transaction

    """
    

    # source = p_orig
    with open(source, 'r', encoding='utf8') as f:
        input_data = f.read()
        f.close()
    
    # Parse the bank statement XML to dictionary
    camt_dict = parser.parse_string(parser.bank_to_customer_statement, bytes(strip_namespace(input_data), encoding='utf-8'))
    statements = pd.DataFrame.from_dict(camt_dict['statements'])
    all_entries = []
    df = pd.DataFrame()
    
    # Unfortunately this format is so ugly, I was not able to extraxt all the information
    # using sensible coding but had to resort to treat the file line by line,
    # batch by batch, entry by entry and transaction by transaction. :(
    for i,_ in statements.iterrows():
        # print(i)
        if 'entries' in camt_dict['statements'][i]:
            # print('new_entry')
            df = pd.DataFrame()
            dd = pd.DataFrame.from_records(camt_dict['statements'][i]['entries'])
            
            dd_flattened = []
            
            
            nb_entries = len(dd['entry_details'])
            # dd['entry_details'][0][0]['batch']['number_of_transactions'] zeigt die Anz. Transaktionen
            # nb_tx_structure = [int( entry[0]['batch']['number_of_transactions'] ) for entry in dd['entry_details']]
            # nb_tx = np.sum(nb_tx_structure)
            for j in range(nb_entries):
                # print(i, j)
                
                txs = dd['entry_details'][j][0]
                betreff = dd['additional_information'][j][0] # Ein Hack, weil die Betreff nur auf Stufe Batch vorhanden sind
                datum = pd.to_datetime(dd['value_date'].str['date'], format='%Y-%m-%d')[j].date()
                
                # Falls man alle Infos zu einem Eintrag anschauen will: dd.iloc[j, :]
                if betreff == '':
                    print(f'Kein Betreff! Schräger Fall, bitte untersuchen!\n   i={i}, j={j}, k={k}\n   source={source}\n   txs={txs}')
                
                
                try:
                    k_range = range(len(txs['transactions']))
                except KeyError: # Für den Fehler KeyError: 'transactions'
                    if dd['additional_information'][j][0] == 'Gehaltszahlung':
                        k_range = range(1) # Bei Gehaltszahlungen gibt es keine Transaktionen, deshalb muss man diesen Umweg gehen
                        # print('Gehaltszahlung, mögliches Problem')
                        # Gehaltszahlungen werden völlig quer erfasst in diesem ISO-Format
                        # Siehe dd.iloc[17,:] bei ../CAMT053_181222.xml
                        
                        # tx = dd.iloc[j,:] # Ein sehr hässlicher Hack, aber funktioniert. Man weist einfach den ganzen Eintrag zu statt die Transaktion
                        betreff = 'Gehaltszahlung'
                    else:
                        print(f'schräger Fall, bitte untersuchen!\n   i={i}, j={j}, k={k}\n   source={source}\n   txs={txs}')
                    
                for k in k_range:
                    # print(i, j, k)
                    try: 
                        tx = txs['transactions'][k]
                    except KeyError: # Spezialfall von Gehaltszahlungen... unglaublich nervig aber geht. 
                        tx = dd.iloc[j,:] # Ein sehr hässlicher Hack, aber funktioniert. Man weist einfach den ganzen Eintrag zu statt die Transaktion
                    
                    # TODO
                    """
                    # Name vom Debitor: 
                    tx['related_parties']['debtor']['name']
                    # IBAN vom Debitor: (gibt es irgendwie nicht immer)
                    tx['related_parties']['debtor_account']['id']['iban']
                    
                    # Name vom Kreditor: 
                    tx['related_parties']['creditor']['name']
                    # IBAN vom Kreditor: 
                    tx['related_parties']['creditor_account']['id']['iban']
                
                    """
                
                    tx['Betreff'] = betreff
                    tx['Datum'] = datum
                    
                    dd_flattened.append(tx)
                    
                dd_flattened.append(tx)
           
                
                    
            dd_flattened = pd.DataFrame.from_records(dd_flattened)     
                    
                    
            # Das Mistformat muss man noch umwandeln je nach Kredit oder Debit
            credit_debit = dd_flattened['credit_debit_indicator'].replace({'CRDT':1, 'DBIT':-1})
            df['Betrag'] = dd_flattened['amount'].str['_value'].apply(pd.to_numeric) * credit_debit
            iban = camt_dict['statements'][i]['account']['id']['iban'] 
            df['IBAN'] = iban
            df['Währung'] = dd_flattened['amount'].str['currency']
            
            df['Betreff'] = dd_flattened['Betreff']
            df['Datum'] = dd_flattened['Datum']
            
            df['Stichwort'] = extract_Stichwort2(dd_flattened)
            df['Mitteilung an Empfänger'] = extract_rem_inf2(dd_flattened)
            
            all_entries.append(df)
    
    df_entries = pd.concat(all_entries)
    df_entries['Betrag'] = df_entries['Betrag'].apply(pd.to_numeric)
    # print(df_entries)
    # Ghüder rausfiltern
    df_entries = df_entries.replace(['00000000', 'NOTPROVIDED'], '')
    
    # definierte Reihenfolge herstellen für den Export
    cols = ['IBAN','Währung','Datum','Betreff', 'Betrag', 'Stichwort', 'Mitteilung an Empfänger']
    df_entries = df_entries[cols + [c for c in df.columns if c not in cols]]
    
    df_entries.drop_duplicates(inplace=True) # BUG wieso ist das nötig???
    
    return df_entries



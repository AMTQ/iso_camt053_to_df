# -*- coding: utf-8 -*-
"""
Beispielskript für die Verarbeitung von CAMT053-Dateien und Export als Excel/CSV

"""



from iso_camt053_to_df import camt2df


source_xml = 'CAMT053_071222_sample.xml'
target_xlsx = 'CAMT053_071222_sample.xlsx'


df = camt2df(source_xml)

df = df.sort_values(['Datum', 'IBAN', 'Betreff', 'Stichwort'], ascending=False).reset_index(drop=True)
print(df)

df.to_excel(target_xlsx, index=False)




# iso_camt053_to_df
## Motivation und Zusammenfassung
English version see [Motivation and summary](#motivation-and-summary).
**ACTHUNG! Diese Bibliothek erhebt keinen Anspruch auf Vollständigkeit der
exportierten Daten. Verwendung auf eigenes Risiko.**

Datenexport vom standardisierten ISO CAMT053-Format in etwas Menschenlesbares.

Dieses Projekt erlaubt die Export-Dateien des E-Bankings der Migrosbank im Format 
ISO CAMT053 in ein pandas DataFrame zu konvertieren.

Warum schlägt man sich überhaupt mit diesem xml-Format herum? Weil alle anderen
zur Zeit verfügbaren Exportformate (pdf, csv) viel weniger Informationen enthalten,
insbesondere Stichworte und Mitteilungen an den Empfänger werden nicht exportiert.

Allerdings werden auch in diesem CAMT053-Format **nicht** sämtliche Informationen,
die im E-Banking sichtbar sind, exportiert, wieso auch immer. Ebenso werden nicht
alle in den xml-Dateien enthaltenen Informationen exportiert, sondern nur das
von mir als Relevant eingeschätzte.

Diese Bibliothek wurde spezifisch für die Dateien des Migrosbank E-Banking Export 
geschrieben. Da es sich - scheinbar - um ein standardisiertes FOrmat handelt,
*könnte* es möglicherweise auch für solche Dateien von anderen Banken funktionieren.
Wäre aber Zufall und ist ungetestet.


## Motivation and summary
**WARNING! This library does not guarantee completenes and may contain bugs. Use 
at your own risk.**

 Export data from standardized ISO CAMT053 to something human-readable.
 
 Convert export-files from e-banking of Migrosbank in the format ISO CAMT053
 to pandas DataFrame.
 Why choose this xml-format in the first place? Because all other proposed 
 export formats from Migrosbank (pdf, csv) do contain less information
 information than the xml-files. However, even here some information visible 
 in e-banking is not contained in the files, for whatever reason. What is more, 
 not all information contained in the xml-files is exported, only what I decided
 to be useful and pertinent.
 
 This library has been specifically created for files of Migrosbank. It *may*
 work with other files in the same guise, but nothing has been tested.

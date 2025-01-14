Per testare è necessario usare Linux perché i software sono predisposti per tale OS,
anche la WSL va bene; inoltre consiglio di verificare se Probe e Validate abbiano i permessi
di esecuzione poichè senza essi non è possibile eseguirli.

Per farlo è sufficiente andare nella cartella dove sono presenti Probe e Validate e usare il comando:
''' chmod +x probe '''
e
''' chmod +x Validate '''

N.B.: è necessario avere installato le seguenti librerie:
numpy
tqdm
pickle
pynput
shutil
pddl
re
tabulate
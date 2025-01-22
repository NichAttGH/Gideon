Per testare è necessario usare Linux perché i software sono predisposti per tale OS,
anche la WSL va bene; inoltre consiglio di verificare se Probe e Validate abbiano i permessi
di esecuzione poichè senza essi non è possibile eseguirli.

Per farlo è sufficiente andare nella cartella dove è presente Probe e usare il comando:
''' chmod +x probe '''
mentre per Validate il percorso è il seguente:
"/your/path/Project/planner/VAL/build/linux64/Release/bin/Validate"
e il comando è: ''' chmod +x Validate '''

N.B.: è necessario avere installato le seguenti librerie:
numpy
tqdm
pickle
shutil
pddl
re
tabulate
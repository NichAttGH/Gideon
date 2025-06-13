import os
from pathlib import Path
from typing import List, Dict, Tuple, Union


def check_empty_files(folder_path: Union[str, Path], 
                     recursive: bool = False, 
                     return_details: bool = False) -> Union[bool, List[str], Dict[str, any]]:
    """
    Verifica se in una cartella sono presenti file vuoti (dimensione 0 byte).
    
    Args:
        folder_path (str|Path): Percorso della cartella da verificare
        recursive (bool): Se True, cerca ricorsivamente nelle sottocartelle
        return_details (bool): Se True, restituisce dettagli completi sui file vuoti
        
    Returns:
        bool: Se return_details=False, restituisce True se ci sono file vuoti
        List[str]: Se return_details=False ma vengono trovati file vuoti, lista dei percorsi
        Dict: Se return_details=True, dizionario con statistiche dettagliate
        
    Raises:
        FileNotFoundError: Se la cartella non esiste
        PermissionError: Se non si hanno i permessi per accedere alla cartella
    """
    
    # Converti in Path object per facilità d'uso
    folder = Path(folder_path)
    
    # Verifica che la cartella esista
    if not folder.exists():
        raise FileNotFoundError(f"La cartella '{folder_path}' non esiste")
    
    if not folder.is_dir():
        raise ValueError(f"'{folder_path}' non è una cartella")
    
    empty_files = []
    total_files = 0
    errors = []
    
    try:
        # Scegli il metodo di scansione basato su recursive
        if recursive:
            # Scansione ricorsiva con rglob
            file_pattern = "**/*"
            files_to_check = folder.rglob("*")
        else:
            # Solo file nella cartella principale
            files_to_check = folder.iterdir()
        
        for item in files_to_check:
            try:
                # Verifica solo i file (non le cartelle)
                if item.is_file():
                    total_files += 1
                    
                    # Verifica se il file è vuoto (0 byte)
                    if item.stat().st_size == 0:
                        empty_files.append(str(item))
                        
            except (PermissionError, OSError) as e:
                # Raccogli errori per file inaccessibili
                errors.append(f"Errore accesso a '{item}': {str(e)}")
                continue
                
    except PermissionError:
        raise PermissionError(f"Permessi insufficienti per accedere alla cartella '{folder_path}'")
    
    # Restituisci risultati basati sui parametri
    if return_details:
        return {
            'has_empty_files': len(empty_files) > 0,
            'empty_files': empty_files,
            'empty_count': len(empty_files),
            'total_files': total_files,
            'folder_path': str(folder),
            'recursive_search': recursive,
            'errors': errors
        }
    else:
        if len(empty_files) > 0:
            return empty_files
        else:
            return False


def print_empty_files_report(folder_path: Union[str, Path], recursive: bool = False):
    """
    Stampa un report dettagliato sui file vuoti trovati nella cartella.
    
    Args:
        folder_path (str|Path): Percorso della cartella da verificare
        recursive (bool): Se True, cerca ricorsivamente nelle sottocartelle
    """
    
    try:
        result = check_empty_files(folder_path, recursive=recursive, return_details=True)
        
        print("=" * 60)
        print("📁 REPORT FILE VUOTI")
        print("=" * 60)
        print(f"Cartella analizzata: {result['folder_path']}")
        print(f"Ricerca ricorsiva: {'Sì' if result['recursive_search'] else 'No'}")
        print(f"File totali trovati: {result['total_files']}")
        print(f"File vuoti trovati: {result['empty_count']}")
        
        if result['has_empty_files']:
            print("\n🚨 FILE VUOTI RILEVATI:")
            print("-" * 40)
            for i, empty_file in enumerate(result['empty_files'], 1):
                print(f"{i:2d}. {empty_file}")
        else:
            print("\n✅ Nessun file vuoto trovato!")
        
        if result['errors']:
            print(f"\n⚠️ ERRORI RILEVATI ({len(result['errors'])}):")
            print("-" * 40)
            for error in result['errors']:
                print(f"   {error}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {str(e)}")


def remove_empty_files(folder_path: Union[str, Path], 
                      recursive: bool = False, 
                      confirm: bool = True) -> Dict[str, any]:
    """
    Rimuove i file vuoti dalla cartella specificata.
    
    Args:
        folder_path (str|Path): Percorso della cartella
        recursive (bool): Se True, cerca ricorsivamente nelle sottocartelle
        confirm (bool): Se True, chiede conferma prima di eliminare
        
    Returns:
        Dict: Statistiche sull'operazione di rimozione
    """
    
    # Prima trova tutti i file vuoti
    result = check_empty_files(folder_path, recursive=recursive, return_details=True)
    
    if not result['has_empty_files']:
        return {
            'files_removed': 0,
            'files_found': 0,
            'errors': [],
            'operation': 'completed - no empty files found'
        }
    
    empty_files = result['empty_files']
    
    # Chiedi conferma se richiesto
    if confirm:
        print(f"\n🚨 Trovati {len(empty_files)} file vuoti.")
        print("File da eliminare:")
        for f in empty_files[:5]:  # Mostra solo i primi 5
            print(f"  - {f}")
        if len(empty_files) > 5:
            print(f"  ... e altri {len(empty_files) - 5} file")
        
        response = input(f"\nVuoi eliminare tutti i {len(empty_files)} file vuoti? (s/N): ")
        if response.lower() not in ['s', 'si', 'sì', 'y', 'yes']:
            return {
                'files_removed': 0,
                'files_found': len(empty_files),
                'errors': [],
                'operation': 'cancelled by user'
            }
    
    # Procedi con l'eliminazione
    removed_count = 0
    errors = []
    
    for file_path in empty_files:
        try:
            os.remove(file_path)
            removed_count += 1
            print(f"✅ Eliminato: {file_path}")
        except Exception as e:
            errors.append(f"Errore eliminando '{file_path}': {str(e)}")
            print(f"❌ Errore: {file_path} - {str(e)}")
    
    return {
        'files_removed': removed_count,
        'files_found': len(empty_files),
        'errors': errors,
        'operation': 'completed'
    }


# Esempi d'uso
if __name__ == "__main__":
    
    print("🔍 ESEMPI D'USO DELLA FUNZIONE check_empty_files")
    print("=" * 50)
    
    # Esempio 1: Verifica semplice (restituisce True/False o lista)
    folder_to_check = "/home/nick/test3/full_dataset/transport/plans"  # Cartella corrente
    
    print(f"\n1️⃣ Verifica semplice in '{folder_to_check}':")
    try:
        result = check_empty_files(folder_to_check)
        if result:
            print(f"   ⚠️ Trovati file vuoti: {len(result) if isinstance(result, list) else 'Sì'}")
            if isinstance(result, list):
                for f in result[:3]:  # Mostra solo i primi 3
                    print(f"     - {f}")
        else:
            print("   ✅ Nessun file vuoto trovato")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Esempio 2: Verifica con dettagli completi
    print(f"\n2️⃣ Verifica dettagliata in '{folder_to_check}':")
    try:
        result = check_empty_files(folder_to_check, return_details=True)
        print(f"   File totali: {result['total_files']}")
        print(f"   File vuoti: {result['empty_count']}")
        print(f"   Ha file vuoti: {result['has_empty_files']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")
    
    # Esempio 3: Report completo
    print(f"\n3️⃣ Report completo:")
    print_empty_files_report(folder_to_check)
    
    print("\n" + "=" * 50)
    print("💡 COME USARE LE FUNZIONI:")
    print("=" * 50)
    print("# Verifica base:")
    print("has_empty = check_empty_files('/path/to/folder')")
    print()
    print("# Verifica ricorsiva con dettagli:")
    print("details = check_empty_files('/path/to/folder', recursive=True, return_details=True)")
    print()
    print("# Report stampato:")
    print("print_empty_files_report('/path/to/folder', recursive=True)")
    print()
    print("# Rimozione file vuoti:")
    print("result = remove_empty_files('/path/to/folder', recursive=True)")
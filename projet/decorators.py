
import functools
import time

# Ceci est un décorateur
def log_execution_time(func):
    """
    Un décorateur simple qui mesure et affiche le temps d'exécution d'une fonction.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"--- Début de l'exécution de {func.__name__} ---")
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"--- Fin de l'exécution de {func.__name__} en {duration:.4f} secondes ---")
        return result
    return wrapper

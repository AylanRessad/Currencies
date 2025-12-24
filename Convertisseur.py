import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import os

# Nom du fichier où sera stockée la clé
CONFIG_FILE = "api_key.txt"

def load_api_key():
    """Charge la clé depuis le fichier ou demande à l'utilisateur de la saisir."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    else:
        # Demande la clé à l'utilisateur
        key = simpledialog.askstring("Configuration", "Veuillez entrer votre clé API (ExchangeRatesAPI) :", parent=root)
        if key:
            # Sauvegarde la clé pour la prochaine fois
            with open(CONFIG_FILE, "w") as f:
                f.write(key)
            return key
        return None

def convert_currency():
    # On récupère la clé stockée
    api_key = load_api_key()
    
    if not api_key:
        messagebox.showwarning("Clé manquante", "Vous devez entrer une clé API pour continuer.")
        return

    try:
        montant = float(entry_montant.get())
        monnaie1 = entry_monnaie1.get().upper()
        monnaie2 = entry_monnaie2.get().upper()
        
        api_url = f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}"
        
        taux = requests.get(api_url).json()
        
        if 'error' in taux:
            messagebox.showerror("Erreur API", taux['error']['message'])
            return

        rate = taux['rates'][monnaie2] / taux['rates'][monnaie1]
        conversion = rate * montant
        
        result_label.config(text=f"{montant} {monnaie1} = {conversion:.2f} {monnaie2}")
        
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# --- Interface TKinter ---
root = tk.Tk()
root.title("Convertisseur de devises")
root.geometry("400x300")

# On s'assure que la fenêtre est créée avant de demander la clé si besoin
root.withdraw() # Cache la fenêtre principale temporairement
API_KEY = load_api_key()
if not API_KEY:
    root.destroy() # Quitte si aucune clé n'est fournie
else:
    root.deiconify() # Réaffiche la fenêtre principale

# Layout
label_montant = tk.Label(root, text="Montant :")
label_montant.grid(row=0, column=0, padx=10, pady=10)
entry_montant = tk.Entry(root)
entry_montant.grid(row=0, column=1, padx=10, pady=10)

label_monnaie1 = tk.Label(root, text="De (ex: EUR) :")
label_monnaie1.grid(row=1, column=0, padx=10, pady=10)
entry_monnaie1 = tk.Entry(root)
entry_monnaie1.grid(row=1, column=1, padx=10, pady=10)

label_monnaie2 = tk.Label(root, text="Vers (ex: USD) :")
label_monnaie2.grid(row=2, column=0, padx=10, pady=10)
entry_monnaie2 = tk.Entry(root)
entry_monnaie2.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="Convertir", command=convert_currency, bg="#4CAF50", fg="white")
convert_button.grid(row=3, columnspan=2, padx=10, pady=20)

result_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
result_label.grid(row=4, columnspan=2, padx=10, pady=10)

root.mainloop()
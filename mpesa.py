"""
By Jose Okitandende Okungu 

"""

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class VodacomMpesa:
    """Classe gérant la logique des transactions M-Pesa."""
    
    def __init__(self):
        self.solde = 0
        self.historique_transactions = []

    def recharger_compte(self, montant):
        if montant <= 0:
            return "Montant invalide. Veuillez entrer un montant positif."
        self.solde += montant
        self.historique_transactions.append(f"Rechargé : {montant} unités.")
        return f"Recharge réussie ! Nouveau solde : {self.solde} unités."

    def acheter_forfait(self, forfait):
        forfaits = {
            "Appels": {"nom": "Forfait Appels", "prix": 600},
            "SMS": {"nom": "Forfait SMS", "prix": 300},
            "Internet": {"nom": "Forfait Internet", "prix": 1500}
        }
        if forfait not in forfaits:
            return "Forfait invalide."
        prix = forfaits[forfait]["prix"]
        nom = forfaits[forfait]["nom"]
        if self.solde < prix:
            return f"Solde insuffisant. Prix du {nom} : {prix} unités."
        self.solde -= prix
        self.historique_transactions.append(f"Acheté : {nom} ({prix} unités).")
        return f"{nom} acheté avec succès ! Nouveau solde : {self.solde} unités."

    def afficher_historique(self):
        if not self.historique_transactions:
            return "Aucune transaction disponible."
        return "\n".join(self.historique_transactions)

    def effacer_historique(self):
        self.historique_transactions = []
        return "Historique des transactions effacé."

    def reinitialiser_solde(self):
        self.solde = 0
        return "Solde réinitialisé à zéro."


class MpesaApp:
    """Interface graphique pour l'application M-Pesa."""

    def __init__(self, root):
        self.mpesa = VodacomMpesa()
        self.root = root
        self.root.title("Vodacom M-Pesa")
        self.root.geometry("600x600")

        # Titre principal
        self.title_label = ctk.CTkLabel(root, text="Vodacom M-Pesa", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Section Solde
        self.solde_frame = ctk.CTkFrame(root, corner_radius=10)
        self.solde_frame.pack(pady=10, padx=20, fill="x")
        self.solde_label = ctk.CTkLabel(self.solde_frame, text="Solde : 0 unités", font=("Helvetica", 18))
        self.solde_label.pack(pady=10)

        # Section Recharge
        self.recharge_frame = ctk.CTkFrame(root, corner_radius=10)
        self.recharge_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.recharge_frame, text="Montant à recharger :", font=("Helvetica", 14)).pack(anchor="w", padx=10, pady=5)
        self.montant_recharge = ctk.CTkEntry(self.recharge_frame, placeholder_text="Entrez le montant")
        self.montant_recharge.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(self.recharge_frame, text="Recharger", command=self.recharger_compte).pack(pady=10)

        # Section Achat Forfait
        self.forfait_frame = ctk.CTkFrame(root, corner_radius=10)
        self.forfait_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.forfait_frame, text="Choisir un forfait :", font=("Helvetica", 14)).pack(anchor="w", padx=10, pady=5)
        self.forfait_var = ctk.StringVar(value="Appels")
        ctk.CTkOptionMenu(self.forfait_frame, variable=self.forfait_var, values=["Appels", "SMS", "Internet"]).pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(self.forfait_frame, text="Acheter Forfait", command=self.acheter_forfait).pack(pady=10)

        # Section Historique
        self.historique_frame = ctk.CTkFrame(root, corner_radius=10)
        self.historique_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.historique_frame, text="Afficher Historique", command=self.afficher_historique).pack(pady=5)
        ctk.CTkButton(self.historique_frame, text="Effacer Historique", command=self.effacer_historique).pack(pady=5)

        # Section Réinitialisation
        self.reset_frame = ctk.CTkFrame(root, corner_radius=10)
        self.reset_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.reset_frame, text="Réinitialiser le Solde", command=self.reinitialiser_solde).pack(pady=5)

    def recharger_compte(self):
        try:
            montant = int(self.montant_recharge.get())
            message = self.mpesa.recharger_compte(montant)
            self.solde_label.configure(text=f"Solde : {self.mpesa.solde} unités")
            messagebox.showinfo("Recharge", message)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    def acheter_forfait(self):
        forfait = self.forfait_var.get()
        message = self.mpesa.acheter_forfait(forfait)
        self.solde_label.configure(text=f"Solde : {self.mpesa.solde} unités")
        messagebox.showinfo("Achat Forfait", message)

    def afficher_historique(self):
        historique = self.mpesa.afficher_historique()
        messagebox.showinfo("Historique", historique)

    def effacer_historique(self):
        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer l'historique ?")
        if confirmation:
            message = self.mpesa.effacer_historique()
            messagebox.showinfo("Historique", message)

    def reinitialiser_solde(self):
        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment réinitialiser le solde ?")
        if confirmation:
            message = self.mpesa.reinitialiser_solde()
            self.solde_label.configure(text="Solde : 0 unités")
            messagebox.showinfo("Solde", message)


# Créer la fenêtre principale
if __name__ == "__main__":
    root = ctk.CTk()
    app = MpesaApp(root)
    root.mainloop()

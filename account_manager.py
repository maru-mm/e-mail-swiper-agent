"""
Gestore multi-account per Gmail OAuth 2.0
"""

import json
import os
from typing import List, Dict, Optional


class AccountManager:
    """
    Gestisce multipli account Gmail con diverse credenziali OAuth 2.0
    """
    
    def __init__(self, config_file: str = 'google_accounts.json'):
        """
        Inizializza il gestore account
        
        Args:
            config_file: Path al file di configurazione JSON
        """
        self.config_file = config_file
        self.accounts = self._load_accounts()
    
    def _load_accounts(self) -> List[Dict]:
        """
        Carica gli account dal file di configurazione
        """
        if not os.path.exists(self.config_file):
            # Crea un file di default
            default_config = {
                "accounts": [
                    {
                        "name": "Account Default",
                        "email": "",
                        "client_id": "",
                        "client_secret": "",
                        "token_file": "token.pickle",
                        "active": True
                    }
                ]
            }
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config['accounts']
        
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        return config.get('accounts', [])
    
    def _save_accounts(self):
        """
        Salva gli account nel file di configurazione
        """
        with open(self.config_file, 'w') as f:
            json.dump({'accounts': self.accounts}, f, indent=2)
    
    def get_all_accounts(self) -> List[Dict]:
        """
        Recupera tutti gli account configurati
        """
        return self.accounts
    
    def get_active_account(self) -> Optional[Dict]:
        """
        Recupera l'account attualmente attivo
        """
        for account in self.accounts:
            if account.get('active', False):
                return account
        
        # Se nessun account è attivo, attiva il primo
        if self.accounts:
            self.accounts[0]['active'] = True
            self._save_accounts()
            return self.accounts[0]
        
        return None
    
    def set_active_account(self, index: int) -> bool:
        """
        Imposta un account come attivo
        
        Args:
            index: Indice dell'account (0-based)
        
        Returns:
            True se l'operazione ha successo
        """
        if 0 <= index < len(self.accounts):
            # Disattiva tutti gli account
            for account in self.accounts:
                account['active'] = False
            
            # Attiva l'account selezionato
            self.accounts[index]['active'] = True
            self._save_accounts()
            return True
        return False
    
    def add_account(self, name: str, email: str, client_id: str, client_secret: str) -> bool:
        """
        Aggiunge un nuovo account
        
        Args:
            name: Nome dell'account
            email: Email associata
            client_id: Google Client ID
            client_secret: Google Client Secret
        
        Returns:
            True se l'account è stato aggiunto
        """
        # Genera un nome file token unico
        token_file = f"token_account{len(self.accounts) + 1}.pickle"
        
        new_account = {
            "name": name,
            "email": email,
            "client_id": client_id,
            "client_secret": client_secret,
            "token_file": token_file,
            "active": False
        }
        
        self.accounts.append(new_account)
        self._save_accounts()
        return True
    
    def remove_account(self, index: int) -> bool:
        """
        Rimuove un account
        
        Args:
            index: Indice dell'account da rimuovere
        
        Returns:
            True se l'account è stato rimosso
        """
        if 0 <= index < len(self.accounts):
            # Rimuovi il file token se esiste
            token_file = self.accounts[index].get('token_file')
            if token_file and os.path.exists(token_file):
                os.remove(token_file)
            
            # Rimuovi l'account
            self.accounts.pop(index)
            
            # Se era l'account attivo, attiva il primo disponibile
            if self.accounts and not any(acc.get('active') for acc in self.accounts):
                self.accounts[0]['active'] = True
            
            self._save_accounts()
            return True
        return False
    
    def create_credentials_file(self, account: Dict, output_file: str = 'credentials.json'):
        """
        Crea un file credentials.json per un account specifico
        
        Args:
            account: Dizionario con i dati dell'account
            output_file: Nome del file di output
        """
        credentials = {
            "installed": {
                "client_id": account['client_id'],
                "project_id": "gmail-extractor",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": account['client_secret'],
                "redirect_uris": ["http://localhost:8080/", "http://localhost:8080"]
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        print(f"✅ File credentials.json creato per {account['name']}")


def main():
    """
    Interfaccia interattiva per gestire gli account
    """
    manager = AccountManager()
    
    while True:
        print("\n" + "="*80)
        print("📋 GESTIONE ACCOUNT GMAIL")
        print("="*80)
        
        accounts = manager.get_all_accounts()
        
        if not accounts:
            print("\n⚠️ Nessun account configurato.")
        else:
            print("\n👥 Account configurati:")
            for i, account in enumerate(accounts):
                active = "✓ ATTIVO" if account.get('active') else ""
                print(f"  [{i+1}] {account['name']}")
                print(f"      Email: {account.get('email', 'Non specificata')}")
                print(f"      Client ID: {account['client_id'][:30]}...")
                print(f"      Token: {account['token_file']} {active}")
                print()
        
        print("\nAzioni disponibili:")
        print("  [1] Seleziona account attivo")
        print("  [2] Aggiungi nuovo account")
        print("  [3] Rimuovi account")
        print("  [4] Genera credentials.json per account attivo")
        print("  [5] Mostra account attivo")
        print("  [0] Esci")
        
        choice = input("\nScegli un'azione: ").strip()
        
        if choice == '0':
            print("\n👋 Arrivederci!")
            break
        
        elif choice == '1':
            if not accounts:
                print("\n⚠️ Nessun account disponibile.")
                continue
            
            print("\nSeleziona l'account da attivare:")
            for i, account in enumerate(accounts):
                print(f"  [{i+1}] {account['name']}")
            
            try:
                index = int(input("\nNumero account: ").strip()) - 1
                if manager.set_active_account(index):
                    print(f"\n✅ Account '{accounts[index]['name']}' attivato!")
                    
                    # Crea il file credentials.json per l'account attivo
                    manager.create_credentials_file(accounts[index])
                else:
                    print("\n❌ Indice non valido.")
            except ValueError:
                print("\n❌ Input non valido.")
        
        elif choice == '2':
            print("\n➕ Aggiungi nuovo account")
            name = input("Nome account: ").strip()
            email = input("Email (opzionale): ").strip()
            client_id = input("Client ID: ").strip()
            client_secret = input("Client Secret: ").strip()
            
            if name and client_id and client_secret:
                manager.add_account(name, email, client_id, client_secret)
                print(f"\n✅ Account '{name}' aggiunto!")
            else:
                print("\n❌ Tutti i campi sono obbligatori tranne l'email.")
        
        elif choice == '3':
            if not accounts:
                print("\n⚠️ Nessun account da rimuovere.")
                continue
            
            print("\nSeleziona l'account da rimuovere:")
            for i, account in enumerate(accounts):
                print(f"  [{i+1}] {account['name']}")
            
            try:
                index = int(input("\nNumero account: ").strip()) - 1
                if manager.remove_account(index):
                    print(f"\n✅ Account rimosso!")
                else:
                    print("\n❌ Indice non valido.")
            except ValueError:
                print("\n❌ Input non valido.")
        
        elif choice == '4':
            active = manager.get_active_account()
            if active:
                manager.create_credentials_file(active)
                print(f"\n✅ File credentials.json pronto per '{active['name']}'")
            else:
                print("\n⚠️ Nessun account attivo.")
        
        elif choice == '5':
            active = manager.get_active_account()
            if active:
                print(f"\n✅ Account attivo: {active['name']}")
                print(f"   Email: {active.get('email', 'Non specificata')}")
                print(f"   Token file: {active['token_file']}")
            else:
                print("\n⚠️ Nessun account attivo.")


if __name__ == '__main__':
    main()


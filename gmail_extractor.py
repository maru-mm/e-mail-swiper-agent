"""
Modulo per estrarre email da Gmail usando OAuth 2.0
"""

import os
import pickle
import base64
from typing import List, Dict, Optional
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Scopes necessari per leggere le email
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailExtractor:
    """
    Classe per estrarre email da Gmail usando OAuth 2.0
    """
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle', account_manager=None):
        """
        Inizializza l'estrattore Gmail
        
        Args:
            credentials_file: Path al file credentials.json scaricato da Google Cloud Console
            token_file: Path dove salvare/caricare il token di autenticazione
            account_manager: Opzionale AccountManager per gestire multipli account
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        
        # Se viene passato un account manager, usa l'account attivo
        if account_manager:
            active_account = account_manager.get_active_account()
            if active_account:
                # Crea il file credentials.json per l'account attivo
                account_manager.create_credentials_file(active_account, self.credentials_file)
                self.token_file = active_account['token_file']
                print(f"📧 Usando account: {active_account['name']}")
        
        self._authenticate()
    
    def _authenticate(self):
        """
        Gestisce l'autenticazione OAuth 2.0
        """
        creds = None
        
        # Carica il token salvato se esiste
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Se non ci sono credenziali valide, fai login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"File {self.credentials_file} non trovato. "
                        "Scarica le credenziali da Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            # Salva il token per il prossimo utilizzo
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Crea il servizio Gmail
        self.service = build('gmail', 'v1', credentials=creds)
        print("Autenticazione completata con successo!")
    
    def get_messages(self, max_results: Optional[int] = None, query: str = '') -> List[Dict]:
        """
        Recupera la lista dei messaggi
        
        Args:
            max_results: Numero massimo di messaggi da recuperare (None = tutti)
            query: Query di ricerca Gmail (es: 'from:example@gmail.com')
        
        Returns:
            Lista di dizionari con i metadati dei messaggi
        """
        try:
            messages = []
            page_size = 500  # Massimo permesso dall'API Gmail per pagina
            
            request = self.service.users().messages().list(
                userId='me',
                maxResults=page_size,
                q=query
            )
            
            page_num = 0
            while request is not None:
                page_num += 1
                response = request.execute()
                
                if 'messages' in response:
                    messages.extend(response['messages'])
                    print(f"Pagina {page_num}: {len(messages)} messaggi totali scaricati...", end='\r')
                
                # Se abbiamo un limite e l'abbiamo raggiunto, fermiamoci
                if max_results is not None and len(messages) >= max_results:
                    messages = messages[:max_results]
                    break
                
                # Altrimenti continua alla prossima pagina
                request = self.service.users().messages().list_next(
                    request, response
                )
            
            print(f"\nTrovati {len(messages)} messaggi totali")
            return messages
        
        except HttpError as error:
            print(f'Errore durante il recupero dei messaggi: {error}')
            return []
    
    def get_message_detail(self, message_id: str) -> Optional[Dict]:
        """
        Recupera i dettagli completi di un messaggio
        
        Args:
            message_id: ID del messaggio da recuperare
        
        Returns:
            Dizionario con i dettagli del messaggio
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            return self._parse_message(message)
        
        except HttpError as error:
            print(f'Errore durante il recupero del messaggio {message_id}: {error}')
            return None
    
    def _parse_message(self, message: Dict) -> Dict:
        """
        Parsa un messaggio Gmail estraendo le informazioni principali
        
        Args:
            message: Messaggio raw da Gmail API
        
        Returns:
            Dizionario con i dati parsati del messaggio
        """
        headers = message['payload']['headers']
        
        # Estrai gli header principali
        subject = ''
        sender = ''
        recipient = ''
        date = ''
        
        for header in headers:
            name = header['name'].lower()
            if name == 'subject':
                subject = header['value']
            elif name == 'from':
                sender = header['value']
            elif name == 'to':
                recipient = header['value']
            elif name == 'date':
                date = header['value']
        
        # Estrai il corpo del messaggio
        body = self._get_message_body(message['payload'])
        
        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'subject': subject,
            'from': sender,
            'to': recipient,
            'date': date,
            'body': body,
            'snippet': message.get('snippet', ''),
            'labels': message.get('labelIds', [])
        }
    
    def _get_message_body(self, payload: Dict) -> str:
        """
        Estrae il corpo del messaggio dal payload
        
        Args:
            payload: Payload del messaggio
        
        Returns:
            Corpo del messaggio decodificato
        """
        if 'parts' in payload:
            # Messaggio multiparte
            parts = payload['parts']
            body = ''
            
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
            
            return body
        else:
            # Messaggio semplice
            if 'data' in payload['body']:
                return base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')
        
        return ''
    
    def extract_all_emails(self, max_results: Optional[int] = None, query: str = '') -> List[Dict]:
        """
        Estrae tutte le email con i loro dettagli completi
        
        Args:
            max_results: Numero massimo di email da estrarre (None = tutte le email)
            query: Query di ricerca Gmail (es: 'is:unread', 'from:example@gmail.com')
        
        Returns:
            Lista di dizionari con tutti i dettagli delle email
        """
        if max_results is None:
            print("Inizio estrazione di TUTTE le email dell'account...")
        else:
            print(f"Inizio estrazione di massimo {max_results} email...")
        
        # Recupera la lista dei messaggi
        messages = self.get_messages(max_results=max_results, query=query)
        
        # Recupera i dettagli di ogni messaggio
        emails = []
        total = len(messages)
        
        for idx, message in enumerate(messages, 1):
            print(f"Estrazione email {idx}/{total}...", end='\r')
            
            email_detail = self.get_message_detail(message['id'])
            if email_detail:
                emails.append(email_detail)
        
        print(f"\nEstrazione completata! Totale email estratte: {len(emails)}")
        return emails
    
    def get_labels(self) -> List[Dict]:
        """
        Recupera tutte le etichette (labels) dell'account
        
        Returns:
            Lista delle etichette disponibili
        """
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            return labels
        except HttpError as error:
            print(f'Errore durante il recupero delle etichette: {error}')
            return []
    
    def get_profile(self) -> Optional[Dict]:
        """
        Recupera il profilo dell'utente Gmail
        
        Returns:
            Dizionario con le informazioni del profilo
        """
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            return profile
        except HttpError as error:
            print(f'Errore durante il recupero del profilo: {error}')
            return None


def main():
    """
    Esempio di utilizzo del modulo
    """
    try:
        # Inizializza l'estrattore
        extractor = GmailExtractor()
        
        # Mostra il profilo
        profile = extractor.get_profile()
        if profile:
            print(f"\nAccount: {profile['emailAddress']}")
            print(f"Totale messaggi: {profile['messagesTotal']}")
            print(f"Totale thread: {profile['threadsTotal']}")
        
        # Mostra le etichette disponibili
        print("\nEtichette disponibili:")
        labels = extractor.get_labels()
        for label in labels:
            print(f"  - {label['name']} (ID: {label['id']})")
        
        # Estrai TUTTE le email (passa None o non specificare max_results)
        print("\nEstrazione di TUTTE le email dell'account...")
        print("ATTENZIONE: Questo può richiedere molto tempo se hai migliaia di email!")
        print("Per testare, puoi usare max_results=10 invece.")
        
        # Decommenta la riga seguente per estrarre tutte le email:
        # emails = extractor.extract_all_emails()
        
        # Per ora estrai solo le ultime 10 come test:
        emails = extractor.extract_all_emails(max_results=10)
        
        # Mostra i risultati
        print("\n" + "="*80)
        for idx, email in enumerate(emails, 1):
            print(f"\nEmail #{idx}")
            print(f"Da: {email['from']}")
            print(f"A: {email['to']}")
            print(f"Data: {email['date']}")
            print(f"Oggetto: {email['subject']}")
            print(f"Snippet: {email['snippet'][:100]}...")
            print("-"*80)
    
    except FileNotFoundError as e:
        print(f"\nErrore: {e}")
        print("\nPer utilizzare questo modulo devi:")
        print("1. Andare su https://console.cloud.google.com/")
        print("2. Creare un nuovo progetto o selezionarne uno esistente")
        print("3. Abilitare la Gmail API")
        print("4. Creare credenziali OAuth 2.0 (tipo 'Desktop app')")
        print("5. Scaricare il file JSON delle credenziali e rinominarlo in 'credentials.json'")
        print("6. Mettere il file credentials.json nella stessa directory di questo script")
    
    except Exception as e:
        print(f"\nErrore imprevisto: {e}")


if __name__ == '__main__':
    main()


"""
Script di test per verificare la connessione OpenAI API
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Chiave API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY non trovata nel file .env")
    print("Crea un file .env con: OPENAI_API_KEY=your_key_here")
    exit(1)


def test_openai_connection():
    """
    Testa la connessione all'API OpenAI
    """
    print("="*80)
    print("🧪 TEST CONNESSIONE OPENAI API")
    print("="*80)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        print("\n📡 Invio richiesta di test a OpenAI...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello World' in JSON format with a field called 'message'"
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = response.choices[0].message.content
        
        print("\n✅ CONNESSIONE RIUSCITA!")
        print("\n📨 Risposta da OpenAI:")
        print(result)
        
        print("\n📊 Dettagli utilizzo:")
        print(f"  Modello: {response.model}")
        print(f"  Token usati: {response.usage.total_tokens}")
        print(f"  - Input: {response.usage.prompt_tokens}")
        print(f"  - Output: {response.usage.completion_tokens}")
        
        print("\n" + "="*80)
        print("✅ OpenAI API è pronta per l'uso!")
        print("="*80)
        
    except Exception as e:
        print("\n❌ ERRORE nella connessione OpenAI!")
        print(f"\nDettagli: {e}")
        print("\nVerifica:")
        print("1. La chiave API è corretta")
        print("2. Hai credito disponibile sul tuo account OpenAI")
        print("3. La connessione internet funziona")


if __name__ == '__main__':
    test_openai_connection()


"""
Script per sincronizzare email locali (SQLite) con Supabase
"""

from database import EmailDatabase
from products_manager import ProductsManager
from supabase_sync import SupabaseSync


def main():
    """
    Sincronizza tutte le email dal database locale a Supabase
    """
    print("="*80)
    print("☁️  SINCRONIZZAZIONE SUPABASE")
    print("="*80)
    
    try:
        # Inizializza connessioni
        print("\n📦 Inizializzazione database locale...")
        local_db = EmailDatabase()
        products_mgr = ProductsManager()
        
        print("☁️  Connessione a Supabase...")
        supabase = SupabaseSync()
        
        # Test connessione
        if not supabase.test_connection():
            print("\n❌ Connessione Supabase fallita")
            return
        
        # Recupera dati locali
        print("\n📊 Recupero dati dal database locale...")
        local_emails = local_db.get_all_emails()
        local_products = products_mgr.get_all_products()
        
        print(f"   Email locali: {len(local_emails)}")
        print(f"   Prodotti locali: {len(local_products)}")
        
        # Chiedi conferma
        print("\n" + "="*80)
        risposta = input(f"Sincronizzare {len(local_emails)} email e {len(local_products)} prodotti su Supabase? (s/n): ")
        
        if risposta.lower() not in ['s', 'si', 'sì', 'y', 'yes']:
            print("❌ Sincronizzazione annullata")
            return
        
        # Sincronizza email
        print("\n📤 Sincronizzazione email...")
        email_stats = supabase.sync_batch(local_emails)
        
        # Sincronizza prodotti
        if local_products:
            print("\n📤 Sincronizzazione prodotti...")
            supabase.sync_products(local_products)
        
        # Riepilogo
        print("\n" + "="*80)
        print("✅ SINCRONIZZAZIONE COMPLETATA")
        print("="*80)
        print(f"\n📧 Email:")
        print(f"   Totali: {email_stats['total']}")
        print(f"   Sincronizzate: {email_stats['success']}")
        print(f"   Errori: {email_stats['errors']}")
        
        if local_products:
            print(f"\n🎨 Prodotti: {len(local_products)} sincronizzati")
        
        print("\n💡 Le email sono ora disponibili su Supabase!")
        print("   Dashboard: https://app.supabase.com/project/_/editor")
    
    except ValueError as e:
        print(f"\n❌ Errore configurazione: {e}")
        print("\n💡 Configura Supabase nel file .env:")
        print("   SUPABASE_URL=https://your-project.supabase.co")
        print("   SUPABASE_KEY=your-anon-key")
        print("\n   Ottieni le credenziali da:")
        print("   https://app.supabase.com/project/_/settings/api")
    
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()


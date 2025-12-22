"""
Test del sistema di monitoraggio email
"""

from email_monitor import EmailMonitor


def test_monitor():
    """
    Testa il monitor eseguendo un singolo controllo
    """
    print("="*80)
    print("🧪 TEST EMAIL MONITOR")
    print("="*80)
    print("\nQuesto script esegue un singolo controllo per testare il sistema.")
    print("Per il monitoraggio continuo, usa: ./start_monitor.sh\n")
    
    # Crea il monitor
    monitor = EmailMonitor()
    
    # Inizializza
    if not monitor.initialize_extractor():
        print("\n❌ Impossibile inizializzare il monitor")
        return
    
    print("\n" + "="*80)
    print("✅ Monitor inizializzato correttamente!")
    print("="*80)
    
    print("\nEsecuzione controllo email...")
    
    # Esegui un singolo controllo
    monitor.check_for_new_emails()
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETATO")
    print("="*80)
    print("\nIl monitor funziona correttamente!")
    print("\nPer avviare il monitoraggio continuo:")
    print("  ./start_monitor.sh")
    print("\nPer vedere lo stato:")
    print("  http://localhost:5000/monitor")


if __name__ == '__main__':
    try:
        test_monitor()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrotto")
    except Exception as e:
        print(f"\n❌ Errore durante il test: {e}")
        import traceback
        traceback.print_exc()


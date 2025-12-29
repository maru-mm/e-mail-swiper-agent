"""
Web App Flask per visualizzare le email analizzate
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from database import EmailDatabase
from products_manager import ProductsManager
from document_processor import DocumentProcessor
from swipe_generator import SwipeGenerator
from supabase_sync import SupabaseSync
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
import os

# Carica variabili d'ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurazione upload
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.md'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Crea cartella upload se non esiste
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inizializza il database e il gestore prodotti
db = EmailDatabase()
products_mgr = ProductsManager()

# Inizializza Supabase
try:
    supabase_sync = SupabaseSync()
    print("✅ Supabase connesso")
except Exception as e:
    supabase_sync = None
    print(f"⚠️ Supabase non disponibile: {e}")

# Inizializza il generatore di swipe con OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    swipe_gen = SwipeGenerator(api_key=OPENAI_API_KEY, use_ai=True)
else:
    print("⚠️ OPENAI_API_KEY non trovata - Swipe in modalità simulata")
    swipe_gen = SwipeGenerator(use_ai=False)


@app.route('/')
def index():
    """
    Homepage - Vista tabella con dati da Supabase
    """
    return render_template('table_view.html')


@app.route('/api/senders')
def get_senders():
    """
    API: Recupera tutti i sender con conteggio email da Supabase
    """
    if not supabase_sync:
        return jsonify({'error': 'Supabase non configurato'}), 500
    
    try:
        emails = supabase_sync.get_all_emails(limit=5000)
        
        # Raggruppa per sender
        sender_counts = {}
        for email in emails:
            sender = email.get('sender', 'Unknown')
            if sender not in sender_counts:
                sender_counts[sender] = 0
            sender_counts[sender] += 1
        
        # Converti in lista ordinata
        senders = [
            {'sender': sender, 'count': count}
            for sender, count in sender_counts.items()
        ]
        senders.sort(key=lambda x: x['count'], reverse=True)
        
        return jsonify(senders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sender/<path:sender>')
def get_sender_emails(sender):
    """
    API: Recupera tutte le email di un sender specifico da Supabase
    """
    if not supabase_sync:
        return jsonify({'error': 'Supabase non configurato'}), 500
    
    try:
        emails = supabase_sync.get_emails_by_sender(sender)
        return jsonify(emails)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """
    API: Recupera statistiche generali da Supabase
    """
    if not supabase_sync:
        return jsonify({'error': 'Supabase non configurato'}), 500
    
    try:
        emails = supabase_sync.get_all_emails(limit=5000)
        
        # Calcola statistiche
        sender_set = set()
        for email in emails:
            sender_set.add(email.get('sender', 'Unknown'))
        
        stats = {
            'total_emails': len(emails),
            'total_senders': len(sender_set)
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search')
def search():
    """
    API: Cerca email in Supabase
    """
    if not supabase_sync:
        return jsonify({'error': 'Supabase non configurato'}), 500
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    try:
        # Cerca in tutti i campi
        all_emails = supabase_sync.get_all_emails(limit=5000)
        query_lower = query.lower()
        
        results = [
            email for email in all_emails
            if query_lower in (email.get('sender', '') or '').lower()
            or query_lower in (email.get('subject', '') or '').lower()
            or query_lower in (email.get('body', '') or '').lower()
        ]
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/emails')
def get_all_emails():
    """
    API: Recupera tutte le email da Supabase (con limite opzionale)
    """
    if not supabase_sync:
        return jsonify({'error': 'Supabase non configurato'}), 500
    
    try:
        limit = request.args.get('limit', 1000, type=int)
        emails = supabase_sync.get_all_emails(limit=limit)
        return jsonify(emails)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/sender/<path:sender>')
def sender_view(sender):
    """
    Vista dettagliata per un sender specifico
    """
    return render_template('sender.html', sender=sender)


@app.route('/simple')
def simple_view():
    """
    Vista semplice raggruppata: sender, body, link
    """
    return render_template('simple_view.html')


@app.route('/table')
def table_view():
    """
    Vista tabella Excel/Airtable con export
    """
    return render_template('table_view.html')


@app.route('/products')
def products_view():
    """
    Vista gestione prodotti
    """
    return render_template('products.html')


@app.route('/monitor')
def monitor_view():
    """
    Vista monitoraggio email automatico
    """
    return render_template('monitor.html')


# API Prodotti
@app.route('/api/products', methods=['GET'])
def get_products():
    """
    API: Recupera tutti i prodotti
    """
    products = products_mgr.get_all_products()
    return jsonify(products)


@app.route('/api/products', methods=['POST'])
def add_product():
    """
    API: Aggiunge un nuovo prodotto
    """
    data = request.json
    name = data.get('name', '')
    brief = data.get('brief', '')
    
    if not name:
        return jsonify({'error': 'Nome richiesto'}), 400
    
    product_id = products_mgr.add_product(name, brief)
    return jsonify({'id': product_id, 'message': 'Prodotto aggiunto'})


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    API: Aggiorna un prodotto
    """
    data = request.json
    name = data.get('name', '')
    brief = data.get('brief', '')
    
    if not name:
        return jsonify({'error': 'Nome richiesto'}), 400
    
    success = products_mgr.update_product(product_id, name, brief)
    if success:
        return jsonify({'message': 'Prodotto aggiornato'})
    return jsonify({'error': 'Prodotto non trovato'}), 404


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    API: Elimina un prodotto
    """
    success = products_mgr.delete_product(product_id)
    if success:
        return jsonify({'message': 'Prodotto eliminato'})
    return jsonify({'error': 'Prodotto non trovato'}), 404


@app.route('/api/swipes', methods=['POST'])
def save_swipe():
    """
    API: Salva uno swipe
    """
    data = request.json
    email_id = data.get('email_id')
    product_id = data.get('product_id')
    notes = data.get('notes', '')
    
    if not email_id or not product_id:
        return jsonify({'error': 'email_id e product_id richiesti'}), 400
    
    swipe_id = products_mgr.save_swipe(email_id, product_id, notes)
    return jsonify({'id': swipe_id, 'message': 'Swipe salvato'})


@app.route('/api/swipes', methods=['GET'])
def get_swipes():
    """
    API: Recupera gli swipe
    """
    product_id = request.args.get('product_id', type=int)
    swipes = products_mgr.get_swipes(product_id)
    return jsonify(swipes)


@app.route('/api/products/<int:product_id>/upload', methods=['POST'])
def upload_document(product_id):
    """
    API: Upload documento per un prodotto
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Nessun file fornito'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nessun file selezionato'}), 400
    
    # Verifica estensione
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': f'Tipo di file non supportato. Supportati: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        # Salva il file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{product_id}_{filename}")
        file.save(filepath)
        
        # Estrai il testo
        extracted_text, file_type = DocumentProcessor.extract_text(filepath)
        
        # Salva nel database
        file_size = os.path.getsize(filepath)
        doc_id = products_mgr.add_document(product_id, filename, file_type, extracted_text, file_size)
        
        # Elimina il file dopo l'estrazione (opzionale, teniamo solo il testo)
        # os.remove(filepath)
        
        return jsonify({
            'id': doc_id,
            'message': 'Documento caricato ed elaborato con successo',
            'extracted_length': len(extracted_text),
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': f'Errore nel processamento del file: {str(e)}'}), 500


@app.route('/api/products/<int:product_id>/documents', methods=['GET'])
def get_product_documents(product_id):
    """
    API: Recupera i documenti di un prodotto
    """
    documents = products_mgr.get_product_documents(product_id)
    return jsonify(documents)


@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """
    API: Elimina un documento
    """
    success = products_mgr.delete_document(doc_id)
    if success:
        return jsonify({'message': 'Documento eliminato'})
    return jsonify({'error': 'Documento non trovato'}), 404


@app.route('/api/monitor/status', methods=['GET'])
def monitor_status():
    """
    API: Controlla lo stato del monitor
    """
    import subprocess
    
    try:
        # Controlla se il processo è attivo
        result = subprocess.run(['pgrep', '-f', 'email_monitor.py'], 
                              capture_output=True, text=True)
        
        is_running = result.returncode == 0
        
        # Leggi il PID se esiste
        pid = None
        if os.path.exists('monitor.pid'):
            with open('monitor.pid', 'r') as f:
                pid = f.read().strip()
        
        # Leggi gli ultimi log
        last_logs = []
        if os.path.exists('monitor.log'):
            with open('monitor.log', 'r') as f:
                lines = f.readlines()
                last_logs = [line.strip() for line in lines[-20:] if line.strip()]
        
        return jsonify({
            'running': is_running,
            'pid': pid,
            'last_logs': last_logs
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/swipe/generate', methods=['POST'])
def generate_swipe():
    """
    API: Genera uno swipe email (versione interna)
    """
    import time
    start_time = time.time()
    
    data = request.json
    email_body = data.get('email_body', '')
    email_subject = data.get('email_subject', '')
    product_name = data.get('product_name', '')
    product_brief = data.get('product_brief', '')
    
    # Genera lo swipe
    result = swipe_gen.generate_swipe(
        email_body=email_body,
        email_subject=email_subject,
        product_name=product_name,
        product_brief=product_brief
    )
    
    processing_time = time.time() - start_time
    result['processing_time'] = round(processing_time, 2)
    
    return jsonify(result)


@app.route('/api/v1/swipe', methods=['POST'])
def swipe_api_v1():
    """
    API REST v1 per swipe email - Formato standardizzato
    
    Esempio richiesta:
    {
        "rawText": "Email originale completa (subject + body)",
        "productDetails": "Brief dettagliato del prodotto"
    }
    
    Risposta:
    {
        "success": true,
        "rawText": "Email originale",
        "productDetails": "Brief prodotto",
        "swiped": "Email generata/swipata",
        "usedAI": true,
        "aiProvider": "OpenAI GPT-4o",
        "timestamp": "2024-12-17T16:00:00.000Z"
    }
    """
    import time
    
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body required'
            }), 400
        
        raw_text = data.get('rawText', '')
        product_details = data.get('productDetails', '')
        
        if not raw_text or not product_details:
            return jsonify({
                'success': False,
                'error': 'rawText and productDetails are required'
            }), 400
        
        # Separa subject dal body se presente
        lines = raw_text.split('\n', 1)
        email_subject = lines[0] if len(lines) > 0 else 'Email'
        email_body = lines[1] if len(lines) > 1 else raw_text
        
        # Estrai nome prodotto dal brief (prima riga o primi 50 char)
        product_name = product_details.split('\n')[0][:50] if product_details else 'Your Product'
        
        # Genera lo swipe usando OpenAI
        result = swipe_gen.generate_swipe(
            email_body=email_body,
            email_subject=email_subject,
            product_name=product_name,
            product_brief=product_details
        )
        
        # Combina subject e body swipati
        swiped_text = f"{result.get('swiped_subject', email_subject)}\n\n{result.get('swiped_body', email_body)}"
        
        # Risposta standardizzata
        response = {
            'success': result.get('success', True),
            'rawText': raw_text,
            'productDetails': product_details,
            'swiped': swiped_text,
            'usedAI': result.get('method') == 'ai',
            'aiProvider': result.get('ai_provider', 'Simulated'),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'metadata': {
                'subject': result.get('swiped_subject'),
                'body': result.get('swiped_body'),
                'changes': result.get('changes', []),
                'key_insights': result.get('key_insights', '')
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


if __name__ == '__main__':
    # Crea la cartella templates se non esiste
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("="*80)
    print("🚀 EMAIL ANALYZER WEB APP")
    print("="*80)
    print("\n📊 Dashboard disponibile su: http://localhost:5000")
    print("💡 Premi CTRL+C per fermare il server\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')


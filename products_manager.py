"""
Gestore prodotti dell'utente
"""

import sqlite3
from typing import List, Dict, Optional


class ProductsManager:
    """
    Gestisce i prodotti dell'utente
    """
    
    def __init__(self, db_path: str = 'emails.db'):
        """
        Inizializza il gestore prodotti
        
        Args:
            db_path: Path del file database
        """
        self.db_path = db_path
    
    def add_product(self, name: str, brief: str = '', documents_text: str = '') -> int:
        """
        Aggiunge un nuovo prodotto
        
        Args:
            name: Nome del prodotto
            brief: Brief/descrizione del prodotto
            documents_text: Testo estratto dai documenti
        
        Returns:
            ID del prodotto creato
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO my_products (name, brief, documents_text)
            VALUES (?, ?, ?)
        ''', (name, brief, documents_text))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_all_products(self) -> List[Dict]:
        """
        Recupera tutti i prodotti
        
        Returns:
            Lista di prodotti
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM my_products ORDER BY name')
        
        products = []
        for row in cursor.fetchall():
            products.append(dict(row))
        
        conn.close()
        return products
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """
        Recupera un prodotto specifico
        
        Args:
            product_id: ID del prodotto
        
        Returns:
            Dizionario con i dati del prodotto
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM my_products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_product(self, product_id: int, name: str, brief: str, documents_text: str = None) -> bool:
        """
        Aggiorna un prodotto
        
        Args:
            product_id: ID del prodotto
            name: Nuovo nome
            brief: Nuovo brief
            documents_text: Testo estratto dai documenti (opzionale)
        
        Returns:
            True se aggiornato con successo
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if documents_text is not None:
            cursor.execute('''
                UPDATE my_products 
                SET name = ?, brief = ?, documents_text = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, brief, documents_text, product_id))
        else:
            cursor.execute('''
                UPDATE my_products 
                SET name = ?, brief = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, brief, product_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un prodotto
        
        Args:
            product_id: ID del prodotto
        
        Returns:
            True se eliminato con successo
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM my_products WHERE id = ?', (product_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def save_swipe(self, email_id: str, product_id: int, notes: str = '') -> int:
        """
        Salva uno swipe email
        
        Args:
            email_id: ID dell'email
            product_id: ID del prodotto
            notes: Note sullo swipe
        
        Returns:
            ID dello swipe
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_swipes (email_id, product_id, swipe_notes)
            VALUES (?, ?, ?)
        ''', (email_id, product_id, notes))
        
        swipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return swipe_id
    
    def get_swipes(self, product_id: Optional[int] = None) -> List[Dict]:
        """
        Recupera gli swipe
        
        Args:
            product_id: Filtra per prodotto (opzionale)
        
        Returns:
            Lista di swipe
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if product_id:
            cursor.execute('SELECT * FROM email_swipes WHERE product_id = ? ORDER BY created_at DESC', (product_id,))
        else:
            cursor.execute('SELECT * FROM email_swipes ORDER BY created_at DESC')
        
        swipes = []
        for row in cursor.fetchall():
            swipes.append(dict(row))
        
        conn.close()
        return swipes
    
    def add_document(self, product_id: int, filename: str, file_type: str, extracted_text: str, file_size: int) -> int:
        """
        Aggiunge un documento a un prodotto
        
        Args:
            product_id: ID del prodotto
            filename: Nome del file
            file_type: Tipo di file
            extracted_text: Testo estratto
            file_size: Dimensione del file
        
        Returns:
            ID del documento
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO product_documents (product_id, filename, file_type, extracted_text, file_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, filename, file_type, extracted_text, file_size))
        
        doc_id = cursor.lastrowid
        
        # Aggiorna il campo documents_text del prodotto
        cursor.execute('''
            SELECT documents_text FROM my_products WHERE id = ?
        ''', (product_id,))
        
        row = cursor.fetchone()
        current_text = row[0] if row and row[0] else ''
        
        # Aggiungi il nuovo testo
        separator = '\n\n--- ' + filename + ' ---\n\n'
        new_text = current_text + separator + extracted_text if current_text else extracted_text
        
        cursor.execute('''
            UPDATE my_products 
            SET documents_text = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_text, product_id))
        
        conn.commit()
        conn.close()
        
        return doc_id
    
    def get_product_documents(self, product_id: int) -> List[Dict]:
        """
        Recupera tutti i documenti di un prodotto
        
        Args:
            product_id: ID del prodotto
        
        Returns:
            Lista di documenti
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_type, file_size, uploaded_at
            FROM product_documents 
            WHERE product_id = ?
            ORDER BY uploaded_at DESC
        ''', (product_id,))
        
        documents = []
        for row in cursor.fetchall():
            documents.append(dict(row))
        
        conn.close()
        return documents
    
    def delete_document(self, doc_id: int) -> bool:
        """
        Elimina un documento
        
        Args:
            doc_id: ID del documento
        
        Returns:
            True se eliminato
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM product_documents WHERE id = ?', (doc_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success


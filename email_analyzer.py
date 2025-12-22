"""
Modulo per analizzare email con OpenAI API
"""

import json
import re
from typing import Dict, List, Optional
from openai import OpenAI
from datetime import datetime


class EmailAnalyzer:
    """
    Analizza email usando OpenAI per estrarre informazioni strutturate
    """
    
    def __init__(self, api_key: str):
        """
        Inizializza l'analizzatore email
        
        Args:
            api_key: Chiave API di OpenAI
        """
        self.client = OpenAI(api_key=api_key)
    
    def extract_urls(self, email_body: str) -> List[str]:
        """
        Estrae tutti gli URL dal corpo dell'email
        
        Args:
            email_body: Corpo dell'email
        
        Returns:
            Lista di URL trovati
        """
        # Pattern per trovare URL
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, email_body)
        return list(set(urls))  # Rimuovi duplicati
    
    def analyze_email(self, email: Dict) -> Dict:
        """
        Analizza un'email usando OpenAI per categorizzarla ed estrarre informazioni
        
        Args:
            email: Dizionario con i dati dell'email
        
        Returns:
            Dizionario con i dati analizzati
        """
        try:
            # Estrai URL dal body
            urls = self.extract_urls(email.get('body', ''))
            
            # Prepara il prompt per OpenAI
            prompt = self._create_analysis_prompt(email)
            
            # Chiama OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert email marketing analyst. Analyze emails and extract structured information in JSON format. Be precise and consistent with your categorization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Parse la risposta
            analysis = json.loads(response.choices[0].message.content)
            
            # Combina i dati originali con l'analisi
            result = {
                'sender': email.get('from', ''),
                'subject': email.get('subject', ''),
                'email_body': email.get('body', ''),
                'snippet': email.get('snippet', ''),
                'date': email.get('date', ''),
                'time_usa': self._extract_time_usa(email.get('date', '')),
                'notes': analysis.get('notes', ''),
                'email_type': analysis.get('email_type', ''),
                'campaign_type': analysis.get('campaign_type', ''),
                'pricing_extract': analysis.get('pricing_extract', ''),
                'target_audience': analysis.get('target_audience', ''),
                'product_mentioned': analysis.get('product_mentioned', ''),
                'retention': analysis.get('retention', ''),
                'funnel_stage': analysis.get('funnel_stage', ''),
                'urls': urls,
                'labels': email.get('labels', []),
                'thread_id': email.get('thread_id', ''),
                'email_id': email.get('id', '')
            }
            
            return result
        
        except Exception as e:
            print(f"Errore durante l'analisi dell'email: {e}")
            # Ritorna dati base senza analisi
            return {
                'sender': email.get('from', ''),
                'subject': email.get('subject', ''),
                'email_body': email.get('body', ''),
                'snippet': email.get('snippet', ''),
                'date': email.get('date', ''),
                'time_usa': self._extract_time_usa(email.get('date', '')),
                'notes': '',
                'email_type': 'unknown',
                'campaign_type': 'unknown',
                'pricing_extract': '',
                'target_audience': '',
                'product_mentioned': '',
                'retention': '',
                'funnel_stage': '',
                'urls': self.extract_urls(email.get('body', '')),
                'labels': email.get('labels', []),
                'thread_id': email.get('thread_id', ''),
                'email_id': email.get('id', ''),
                'error': str(e)
            }
    
    def _create_analysis_prompt(self, email: Dict) -> str:
        """
        Crea il prompt per l'analisi dell'email
        """
        sender = email.get('from', '')
        subject = email.get('subject', '')
        body = email.get('body', '')
        snippet = email.get('snippet', '')
        
        # Limita il body a 4000 caratteri per non superare i token
        body_preview = body[:4000] if len(body) > 4000 else body
        
        prompt = f"""Analyze this email and extract the following information in JSON format:

EMAIL DATA:
Sender: {sender}
Subject: {subject}
Body Preview: {body_preview}
Snippet: {snippet}

Please provide a JSON response with these fields:

{{
  "notes": "Brief summary or key insights about the email (1-2 sentences)",
  "email_type": "One of: marketing, transactional, promotion, personal, recruiting, product education, onboarding, retention",
  "campaign_type": "One of: marketing, promo, seasonal, abandoned checkout, win-back, recruitment, retention, transactional, personal, product education, onboarding, or more specific",
  "pricing_extract": "Any pricing info, discounts, or offers mentioned (e.g., '20% off', '$50 credit', 'Free shipping'). Leave empty if none.",
  "target_audience": "Who is this email targeting? (e.g., 'prospective customers', 'existing subscribers', 'cart abandoners', 'women 25-45 interested in weight loss')",
  "product_mentioned": "Main product or service mentioned in the email. Be specific.",
  "retention": "Is this a retention/re-engagement email? Leave empty if no, or describe the retention strategy",
  "funnel_stage": "One of: awareness, consideration, conversion, onboarding, retention"
}}

IMPORTANT GUIDELINES:
- Be concise and precise
- Use consistent categorization
- Extract exact pricing/discount information when present
- Identify the primary funnel stage
- For email_type and campaign_type, stick to the provided options when possible
- Return valid JSON only
"""
        return prompt
    
    def _extract_time_usa(self, date_str: str) -> str:
        """
        Estrae l'ora in formato USA dalla stringa della data
        
        Args:
            date_str: Stringa della data dell'email
        
        Returns:
            Ora formattata
        """
        try:
            # Prova a parsare vari formati di data
            # Es: "Wed, 15 Dec 2025 10:30:00 +0100"
            if not date_str:
                return ''
            
            # Estrai solo l'ora se presente
            import email.utils
            parsed = email.utils.parsedate_tz(date_str)
            if parsed:
                dt = datetime(*parsed[:6])
                return dt.strftime("%H:%M")
            
            return ''
        except:
            return ''
    
    def analyze_batch(self, emails: List[Dict], progress_callback=None) -> List[Dict]:
        """
        Analizza un batch di email
        
        Args:
            emails: Lista di email da analizzare
            progress_callback: Funzione callback per il progresso (opzionale)
        
        Returns:
            Lista di email analizzate
        """
        analyzed_emails = []
        total = len(emails)
        
        for idx, email in enumerate(emails, 1):
            if progress_callback:
                progress_callback(idx, total)
            else:
                print(f"Analisi email {idx}/{total}...", end='\r')
            
            analyzed = self.analyze_email(email)
            analyzed_emails.append(analyzed)
        
        print(f"\n✅ Analizzate {len(analyzed_emails)} email!")
        return analyzed_emails


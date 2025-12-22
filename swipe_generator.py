"""
Generatore di email swipe con OpenAI (opzionale)
"""

from openai import OpenAI
from typing import Dict, List
import os
import json


class SwipeGenerator:
    """
    Genera email swipe usando OpenAI o simulazione
    """
    
    def __init__(self, api_key: str = None, use_ai: bool = False):
        """
        Inizializza il generatore
        
        Args:
            api_key: Chiave API OpenAI (opzionale)
            use_ai: Se True, usa OpenAI. Se False, usa simulazione
        """
        self.use_ai = use_ai and api_key is not None
        if self.use_ai:
            self.client = OpenAI(api_key=api_key)
    
    def generate_swipe(self, email_body: str, email_subject: str, 
                      product_name: str, product_brief: str = '') -> Dict:
        """
        Genera uno swipe email
        
        Args:
            email_body: Body dell'email originale
            email_subject: Subject dell'email originale
            product_name: Nome del prodotto
            product_brief: Brief del prodotto
        
        Returns:
            Dizionario con i risultati dello swipe
        """
        if self.use_ai:
            return self._generate_with_ai(email_body, email_subject, product_name, product_brief)
        else:
            return self._generate_simulated(email_body, email_subject, product_name, product_brief)
    
    def _generate_with_ai(self, email_body: str, email_subject: str,
                         product_name: str, product_brief: str) -> Dict:
        """
        Genera swipe usando OpenAI
        """
        prompt = f"""You are an expert email copywriter and marketing strategist. I need you to adapt this marketing email for a different product.

ORIGINAL EMAIL:
Subject: {email_subject}
Body: {email_body[:3000]}

MY PRODUCT:
Name: {product_name}
Brief: {product_brief}

TASK:
Rewrite this email completely for MY PRODUCT while:
1. Keeping the same EMAIL STRUCTURE (hook, body, CTA layout)
2. Maintaining the TONE and EMOTIONAL APPEAL
3. Replacing ALL product mentions with my product
4. Adapting ALL BENEFITS to match my product's unique value proposition
5. Keeping the same URGENCY tactics and CTA approach
6. Using insights from my product brief to make it authentic
7. Making it sound natural and not like a template

IMPORTANT: 
- Use the product brief to understand my product's unique selling points
- Don't just replace brand names - rewrite the benefits and features
- Keep the email length similar
- Maintain any personalization, emojis, or formatting style

Return your response as a JSON object with this structure:
{{
  "subject": "The rewritten subject line",
  "body": "The complete rewritten email body",
  "changes": [
    {{"type": "hook", "original": "original hook", "new": "new hook", "reasoning": "why changed"}},
    {{"type": "benefit", "original": "original benefit", "new": "new benefit", "reasoning": "why changed"}},
    {{"type": "cta", "original": "original CTA", "new": "new CTA", "reasoning": "why changed"}}
  ],
  "key_insights": "Brief explanation of the swipe strategy used"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert email copywriter and marketing strategist. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # Parse il risultato JSON
            swiped_subject = result.get('subject', email_subject)
            swiped_body = result.get('body', email_body)
            changes = result.get('changes', [])
            key_insights = result.get('key_insights', '')
            
            # Formatta le modifiche per la UI
            formatted_changes = []
            for change in changes:
                formatted_changes.append({
                    'type': change.get('type', 'other'),
                    'original': change.get('original', ''),
                    'swipe': change.get('new', ''),
                    'description': change.get('reasoning', '')
                })
            
            return {
                'success': True,
                'swiped_subject': swiped_subject,
                'swiped_body': swiped_body,
                'changes': formatted_changes,
                'key_insights': key_insights,
                'method': 'ai',
                'ai_provider': 'OpenAI GPT-4o'
            }
        
        except Exception as e:
            print(f"Errore OpenAI: {e}")
            # Fallback a simulazione
            return self._generate_simulated(email_body, email_subject, product_name, product_brief)
    
    def _generate_simulated(self, email_body: str, email_subject: str,
                           product_name: str, product_brief: str) -> Dict:
        """
        Genera swipe con sostituzioni simulate
        """
        # Sostituzioni nel subject
        swiped_subject = email_subject
        
        # Brand names comuni da sostituire
        common_brands = ['Bioma', 'Skaler', 'Loom', 'Marie', 'Soraya']
        
        for brand in common_brands:
            if brand in swiped_subject:
                swiped_subject = swiped_subject.replace(brand, product_name)
        
        # Sostituzioni nel body
        swiped_body = email_body
        changes = []
        
        replacements = {
            'Bioma Health': product_name,
            'Bioma': product_name,
            'bioma.health': 'your-product.com',
            'hello@bioma.health': 'hello@your-product.com',
            'Skaler': product_name,
            'Loom': product_name,
            'Psychic Marie': product_name,
            'SpiritualGlows': product_name
        }
        
        for old, new in replacements.items():
            if old in swiped_body:
                swiped_body = swiped_body.replace(old, new)
                changes.append({
                    'type': 'brand',
                    'original': old,
                    'swipe': new,
                    'description': f'Brand "{old}" sostituito con "{new}"'
                })
        
        # Note se non ci sono modifiche
        if not changes:
            changes.append({
                'description': 'Swipe simulato - Integra con OpenAI per sostituzioni intelligenti'
            })
        
        return {
            'success': True,
            'swiped_subject': swiped_subject,
            'swiped_body': swiped_body,
            'changes': changes,
            'method': 'simulated'
        }


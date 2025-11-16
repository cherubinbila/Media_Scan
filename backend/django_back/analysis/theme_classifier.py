#!/usr/bin/env python3
"""
Classificateur thématique utilisant Ollama + Mistral
Classification automatique des articles en catégories
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ThemeClassifier:
    """Classificateur thématique avec Mistral via Ollama"""
    
    # Catégories disponibles
    CATEGORIES = [
        'Politique',
        'Économie',
        'Sécurité',
        'Santé',
        'Culture',
        'Sport',
        'Autres'
    ]
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialise le classificateur
        
        Args:
            ollama_url: URL du serveur Ollama
            model: Nom du modèle (mistral par défaut)
        """
        self.ollama_url = ollama_url
        self.model = model
        self.api_url = f"{ollama_url}/api/generate"
    
    def check_ollama_status(self) -> bool:
        """
        Vérifier si Ollama est accessible
        
        Returns:
            True si Ollama est accessible, False sinon
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def classify_article(self, titre: str, contenu: str, max_tokens: int = 500) -> Dict[str, any]:
        """
        Classifier un article dans une catégorie thématique
        
        Args:
            titre: Titre de l'article
            contenu: Contenu de l'article
            max_tokens: Nombre maximum de tokens à analyser
        
        Returns:
            Dictionnaire avec catégorie, confiance, et mots-clés
        """
        # Tronquer le contenu si trop long
        text_to_analyze = f"{titre}\n\n{contenu[:2000]}"
        
        # Prompt pour Mistral
        prompt = f"""Tu es un expert en classification d'articles de presse burkinabè.

Analyse cet article et détermine sa catégorie principale parmi :

- Politique : gouvernement, ministre, président, assemblée nationale, conseil des ministres, transition, MPSR, capitaine Ibrahim Traoré, diplomatie, élections, parti politique, décret, loi, réforme institutionnelle, conseil constitutionnel, primature, députés, sénat, collectivités territoriales, décentralisation, autorités administratives

- Économie : finance, budget, FCFA, commerce, entreprise, banque, agriculture, coton, or, mines, industrie, emploi, chômage, investissement, marché, production, exportation, importation, croissance économique, PIB, inflation, dette, BCEAO, bourse, entrepreneuriat, PME, secteur privé, développement économique

- Sécurité : armée, FDS (Forces de Défense et Sécurité), VDP (Volontaires pour la Défense de la Patrie), police, gendarmerie, terrorisme, djihadistes, attaque, neutralisation, opération militaire, sécurité intérieure, justice, tribunal, procès, condamnation, criminalité, délinquance, trafic, frontières, renseignement

- Santé : hôpital, CHU, CSPS, médecin, infirmier, maladie, épidémie, paludisme, COVID-19, vaccination, médicament, soins, santé publique, ministère de la santé, OMS, malnutrition, mortalité infantile, planning familial, hygiène, assainissement

- Culture : FESPACO, SIAO, festival, artiste, musique, cinéma, théâtre, danse, littérature, livre, patrimoine, tradition, coutume, éducation, école, université, étudiant, enseignant, alphabétisation, recherche, bibliothèque, musée, arts plastiques, sculpture

- Sport : football, Étalons (équipe nationale), CAN, championnat, match, victoire, défaite, joueur, entraîneur, stade, compétition, athlétisme, basketball, handball, cyclisme, lutte traditionnelle, sport scolaire, fédération sportive

- Autres : si l'article ne correspond clairement à aucune catégorie ci-dessus, ou traite de sujets divers (faits divers généraux, météo, nécrologie, annonces, etc.)

Article à analyser :
---
{text_to_analyze}
---

Réponds UNIQUEMENT au format JSON suivant (sans texte avant ou après) :
{{
    "categorie": "nom_de_la_categorie",
    "confiance": 0.95,
    "mots_cles": ["mot1", "mot2", "mot3"],
    "justification": "courte explication"
}}"""

        try:
            # Appel à Ollama
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Basse température pour plus de cohérence
                        "num_predict": 200,
                    }
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return self._fallback_classification(titre, contenu)
            
            result = response.json()
            response_text = result.get('response', '').strip()
            
            # Parser la réponse JSON
            try:
                # Extraire le JSON de la réponse
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    classification = json.loads(json_str)
                    
                    # Valider la catégorie
                    categorie = classification.get('categorie', 'Autres')
                    if categorie not in self.CATEGORIES:
                        categorie = 'Autres'
                    
                    return {
                        'categorie': categorie,
                        'confiance': float(classification.get('confiance', 0.7)),
                        'mots_cles': classification.get('mots_cles', [])[:5],
                        'justification': classification.get('justification', ''),
                        'methode': 'mistral_ollama'
                    }
                else:
                    return self._fallback_classification(titre, contenu)
            
            except json.JSONDecodeError:
                return self._fallback_classification(titre, contenu)
        
        except Exception as e:
            print(f"⚠️ Erreur classification Mistral: {e}")
            return self._fallback_classification(titre, contenu)
    
    def _fallback_classification(self, titre: str, contenu: str) -> Dict[str, any]:
        """
        Classification de secours basée sur des mots-clés
        
        Args:
            titre: Titre de l'article
            contenu: Contenu de l'article
        
        Returns:
            Dictionnaire avec catégorie et confiance
        """
        text = f"{titre} {contenu}".lower()
        
        # Mots-clés par catégorie (enrichis pour le contexte burkinabè)
        keywords = {
            'Politique': [
                'gouvernement', 'ministre', 'président', 'assemblée', 'député', 'sénat',
                'élection', 'vote', 'parti', 'politique', 'diplomatie', 'conseil',
                'transition', 'mpsr', 'capitaine', 'traore', 'ibrahim', 'primature',
                'décret', 'loi', 'réforme', 'constitutionnel', 'institutionnel',
                'collectivité', 'décentralisation', 'préfet', 'gouverneur', 'maire',
                'ambassadeur', 'sommet', 'cedeao', 'aes', 'souveraineté'
            ],
            'Économie': [
                'économie', 'fcfa', 'budget', 'commerce', 'entreprise', 'banque',
                'agriculture', 'industrie', 'emploi', 'investissement', 'marché',
                'production', 'exportation', 'croissance', 'pib', 'inflation',
                'coton', 'or', 'mine', 'minier', 'bceao', 'bourse', 'dette',
                'entrepreneuriat', 'pme', 'secteur privé', 'développement',
                'financier', 'fiscal', 'douane', 'import', 'export', 'chômage'
            ],
            'Sécurité': [
                'sécurité', 'armée', 'militaire', 'police', 'terrorisme', 'attaque',
                'fds', 'vdp', 'gendarmerie', 'criminalité', 'justice', 'tribunal',
                'procès', 'condamnation', 'terroriste', 'djihadiste', 'neutralisation',
                'opération', 'combat', 'combattant', 'défense', 'sécuritaire',
                'frontière', 'renseignement', 'délinquance', 'trafic', 'banditisme',
                'enlèvement', 'otage', 'attentat', 'explosion', 'engin explosif'
            ],
            'Santé': [
                'santé', 'hôpital', 'médecin', 'maladie', 'épidémie', 'vaccination',
                'chu', 'csps', 'patient', 'traitement', 'médicament', 'covid',
                'paludisme', 'soins', 'sanitaire', 'infirmier', 'clinique',
                'oms', 'malnutrition', 'mortalité', 'planning familial', 'hygiène',
                'assainissement', 'prévention', 'dépistage', 'consultation',
                'pharmacie', 'urgence', 'chirurgie', 'maternité'
            ],
            'Culture': [
                'culture', 'festival', 'artiste', 'musique', 'cinéma', 'théâtre',
                'éducation', 'école', 'université', 'étudiant', 'livre', 'fespaco',
                'siao', 'tradition', 'patrimoine', 'art', 'culturel', 'enseignant',
                'alphabétisation', 'recherche', 'bibliothèque', 'musée', 'sculpture',
                'danse', 'littérature', 'poésie', 'concert', 'exposition',
                'coutume', 'folklore', 'griot', 'tam-tam', 'masque', 'cérémonies'
            ],
            'Sport': [
                'sport', 'football', 'match', 'équipe', 'joueur', 'entraîneur',
                'championnat', 'coupe', 'étalons', 'compétition', 'victoire',
                'défaite', 'but', 'stade', 'can', 'qualification', 'sélection',
                'athlétisme', 'basketball', 'handball', 'cyclisme', 'lutte',
                'fédération', 'sportif', 'performance', 'médaille', 'podium',
                'tournoi', 'finale', 'penalty', 'arbitre', 'supporters'
            ]
        }
        
        # Compter les occurrences
        scores = {}
        for categorie, mots in keywords.items():
            score = sum(1 for mot in mots if mot in text)
            if score > 0:
                scores[categorie] = score
        
        # Déterminer la catégorie
        if scores:
            categorie = max(scores, key=scores.get)
            max_score = scores[categorie]
            total_keywords = sum(len(mots) for mots in keywords.values())
            confiance = min(0.9, max_score / 10)  # Confiance basée sur le nombre de mots-clés
            
            # Extraire les mots-clés trouvés
            mots_cles_trouves = [mot for mot in keywords[categorie] if mot in text][:5]
            
            return {
                'categorie': categorie,
                'confiance': confiance,
                'mots_cles': mots_cles_trouves,
                'justification': f"{max_score} mots-clés trouvés",
                'methode': 'keywords_fallback'
            }
        
        return {
            'categorie': 'Autres',
            'confiance': 0.5,
            'mots_cles': [],
            'justification': 'Aucun mot-clé spécifique trouvé',
            'methode': 'keywords_fallback'
        }
    
    def classify_batch(self, articles: List[Dict[str, str]], show_progress: bool = True) -> List[Dict[str, any]]:
        """
        Classifier un lot d'articles
        
        Args:
            articles: Liste de dictionnaires avec 'titre' et 'contenu'
            show_progress: Afficher la progression
        
        Returns:
            Liste des classifications
        """
        results = []
        total = len(articles)
        
        if show_progress:
            print(f"🤖 Classification de {total} articles...")
        
        for i, article in enumerate(articles, 1):
            if show_progress and i % 10 == 0:
                print(f"   Progression: {i}/{total} articles")
            
            classification = self.classify_article(
                article.get('titre', ''),
                article.get('contenu', '')
            )
            
            results.append({
                'article_id': article.get('id'),
                **classification
            })
        
        if show_progress:
            print(f"✅ Classification terminée")
        
        return results
    
    def get_statistics(self, classifications: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Obtenir des statistiques sur les classifications
        
        Args:
            classifications: Liste des classifications
        
        Returns:
            Dictionnaire de statistiques
        """
        if not classifications:
            return {}
        
        # Compter par catégorie
        categories_count = {}
        for classif in classifications:
            cat = classif.get('categorie', 'Autres')
            categories_count[cat] = categories_count.get(cat, 0) + 1
        
        # Confiance moyenne
        avg_confidence = sum(c.get('confiance', 0) for c in classifications) / len(classifications)
        
        # Méthodes utilisées
        methodes = {}
        for classif in classifications:
            method = classif.get('methode', 'unknown')
            methodes[method] = methodes.get(method, 0) + 1
        
        return {
            'total_articles': len(classifications),
            'categories': categories_count,
            'confiance_moyenne': round(avg_confidence, 2),
            'methodes': methodes
        }

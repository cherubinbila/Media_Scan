"""
Scraper X (Twitter) utilisant l'API v2
"""

import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class TwitterScraper:
    """Scraper pour récupérer les tweets via Twitter API v2"""
    
    def __init__(self, bearer_token: str):
        """
        Initialise le scraper Twitter
        
        Args:
            bearer_token: Bearer Token de l'API Twitter v2
        """
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Twitter
        
        Returns:
            True si la connexion fonctionne
        """
        try:
            # Tester avec un utilisateur connu (Twitter officiel)
            response = self.session.get(
                f"{self.base_url}/users/by/username/Twitter",
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def get_user_id(self, username: str) -> Optional[str]:
        """
        Récupère l'ID d'un utilisateur Twitter
        
        Args:
            username: Nom d'utilisateur (sans @)
            
        Returns:
            ID de l'utilisateur ou None
        """
        try:
            # Enlever le @ si présent
            username = username.lstrip('@')
            
            response = self.session.get(
                f"{self.base_url}/users/by/username/{username}",
                params={
                    'user.fields': 'id,name,username,public_metrics'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('id')
            else:
                print(f"Erreur API: {response.status_code}")
                print(f"Réponse: {response.text}")
            
            return None
        
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ID: {e}")
            return None
    
    def get_user_tweets(self, user_id: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Récupère les tweets d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur Twitter
            max_results: Nombre de tweets à récupérer (5-100)
            
        Returns:
            Liste des tweets avec leurs métriques
        """
        try:
            # Limiter entre 5 et 100
            max_results = max(5, min(100, max_results))
            
            response = self.session.get(
                f"{self.base_url}/users/{user_id}/tweets",
                params={
                    'max_results': max_results,
                    'tweet.fields': 'id,text,created_at,public_metrics,entities,attachments',
                    'expansions': 'attachments.media_keys',
                    'media.fields': 'url,preview_image_url'
                },
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Erreur API: {response.status_code}")
                print(f"Réponse: {response.text}")
                return []
            
            data = response.json()
            tweets = []
            
            # Récupérer les médias si présents
            media_dict = {}
            if 'includes' in data and 'media' in data['includes']:
                for media in data['includes']['media']:
                    media_dict[media['media_key']] = media.get('url') or media.get('preview_image_url')
            
            for tweet in data.get('data', []):
                metrics = tweet.get('public_metrics', {})
                
                # Récupérer l'URL de l'image si présente
                image_url = None
                if 'attachments' in tweet and 'media_keys' in tweet['attachments']:
                    media_key = tweet['attachments']['media_keys'][0]
                    image_url = media_dict.get(media_key)
                
                # Formater la date
                created_at = tweet.get('created_at', '')
                try:
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    date_publication = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_publication = created_at
                
                # Construire l'URL du tweet
                tweet_url = f"https://twitter.com/i/web/status/{tweet.get('id')}"
                
                tweets.append({
                    'tweet_id': tweet.get('id'),
                    'text': tweet.get('text', ''),
                    'url': tweet_url,
                    'image_url': image_url,
                    'date_publication': date_publication,
                    'retweets': metrics.get('retweet_count', 0),
                    'replies': metrics.get('reply_count', 0),
                    'likes': metrics.get('like_count', 0),
                    'quotes': metrics.get('quote_count', 0),
                    'impressions': metrics.get('impression_count', 0),
                    'engagement_total': (
                        metrics.get('retweet_count', 0) +
                        metrics.get('reply_count', 0) +
                        metrics.get('like_count', 0) +
                        metrics.get('quote_count', 0)
                    )
                })
            
            return tweets
        
        except Exception as e:
            print(f"Erreur lors de la récupération des tweets: {e}")
            return []
    
    def scrape_user(self, username: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Scrape un compte Twitter complet
        
        Args:
            username: Nom d'utilisateur (avec ou sans @)
            max_results: Nombre de tweets à récupérer
            
        Returns:
            Dictionnaire avec les infos du compte et les tweets
        """
        result = {
            'user_info': {},
            'tweets': [],
            'stats': {},
            'error': None
        }
        
        # Enlever le @ si présent
        username = username.lstrip('@')
        
        # Récupérer l'ID de l'utilisateur
        user_id = self.get_user_id(username)
        
        if not user_id:
            result['error'] = f"Utilisateur '@{username}' introuvable"
            return result
        
        result['user_info'] = {
            'id': user_id,
            'username': username
        }
        
        # Récupérer les tweets
        tweets = self.get_user_tweets(user_id, max_results)
        
        if not tweets:
            result['error'] = "Aucun tweet récupéré"
            return result
        
        result['tweets'] = tweets
        
        # Calculer les statistiques
        total_retweets = sum(t['retweets'] for t in tweets)
        total_replies = sum(t['replies'] for t in tweets)
        total_likes = sum(t['likes'] for t in tweets)
        total_quotes = sum(t['quotes'] for t in tweets)
        total_impressions = sum(t['impressions'] for t in tweets)
        total_engagement = total_retweets + total_replies + total_likes + total_quotes
        
        result['stats'] = {
            'total_tweets': len(tweets),
            'total_retweets': total_retweets,
            'total_replies': total_replies,
            'total_likes': total_likes,
            'total_quotes': total_quotes,
            'total_impressions': total_impressions,
            'total_engagement': total_engagement,
            'avg_engagement': total_engagement / len(tweets) if tweets else 0
        }
        
        return result

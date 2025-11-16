"""
Scraper Facebook utilisant l'API Graph
"""

import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class FacebookScraper:
    """Scraper pour récupérer les posts Facebook via Graph API"""
    
    def __init__(self, access_token: str):
        """
        Initialise le scraper Facebook
        
        Args:
            access_token: Token d'accès Facebook Graph API
        """
        self.access_token = access_token
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.session = requests.Session()
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Facebook
        
        Returns:
            True si la connexion fonctionne
        """
        try:
            response = self.session.get(
                f"{self.base_url}/me",
                params={'access_token': self.access_token},
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def get_page_id(self, page_name: str) -> Optional[str]:
        """
        Récupère l'ID d'une page Facebook
        
        Args:
            page_name: Nom de la page (username)
            
        Returns:
            ID de la page ou None
        """
        try:
            response = self.session.get(
                f"{self.base_url}/{page_name}",
                params={
                    'access_token': self.access_token,
                    'fields': 'id,name'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('id')
            
            return None
        
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ID: {e}")
            return None
    
    def get_page_posts(self, page_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Récupère les posts d'une page
        
        Args:
            page_id: ID de la page Facebook
            limit: Nombre de posts à récupérer
            
        Returns:
            Liste des posts avec leurs métriques
        """
        try:
            response = self.session.get(
                f"{self.base_url}/{page_id}/posts",
                params={
                    'access_token': self.access_token,
                    'fields': 'id,message,created_time,permalink_url,full_picture,reactions.summary(true),comments.summary(true),shares',
                    'limit': limit
                },
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Erreur API: {response.status_code}")
                print(f"Réponse: {response.text}")
                return []
            
            data = response.json()
            posts = []
            
            for post in data.get('data', []):
                # Extraire les métriques
                reactions = post.get('reactions', {}).get('summary', {}).get('total_count', 0)
                comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                shares = post.get('shares', {}).get('count', 0)
                
                # Formater la date
                created_time = post.get('created_time', '')
                try:
                    date_obj = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                    date_publication = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_publication = created_time
                
                posts.append({
                    'post_id': post.get('id'),
                    'message': post.get('message', ''),
                    'url': post.get('permalink_url', ''),
                    'image_url': post.get('full_picture'),
                    'date_publication': date_publication,
                    'likes': reactions,
                    'comments': comments,
                    'shares': shares,
                    'engagement_total': reactions + comments + shares
                })
            
            return posts
        
        except Exception as e:
            print(f"Erreur lors de la récupération des posts: {e}")
            return []
    
    def scrape_page(self, page_name: str, limit: int = 5) -> Dict[str, Any]:
        """
        Scrape une page Facebook complète
        
        Args:
            page_name: Nom de la page (username)
            limit: Nombre de posts à récupérer
            
        Returns:
            Dictionnaire avec les infos de la page et les posts
        """
        result = {
            'page_info': {},
            'posts': [],
            'stats': {},
            'error': None
        }
        
        # Récupérer l'ID de la page
        page_id = self.get_page_id(page_name)
        
        if not page_id:
            result['error'] = f"Page '{page_name}' introuvable"
            return result
        
        result['page_info'] = {
            'id': page_id,
            'name': page_name
        }
        
        # Récupérer les posts
        posts = self.get_page_posts(page_id, limit)
        
        if not posts:
            result['error'] = "Aucun post récupéré"
            return result
        
        result['posts'] = posts
        
        # Calculer les statistiques
        total_likes = sum(p['likes'] for p in posts)
        total_comments = sum(p['comments'] for p in posts)
        total_shares = sum(p['shares'] for p in posts)
        total_engagement = total_likes + total_comments + total_shares
        
        result['stats'] = {
            'total_posts': len(posts),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_engagement': total_engagement,
            'avg_engagement': total_engagement / len(posts) if posts else 0
        }
        
        return result

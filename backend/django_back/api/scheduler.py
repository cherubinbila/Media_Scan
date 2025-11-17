"""
Scheduler pour l'automatisation du scraping
"""

import threading
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from database.db_manager import DatabaseManager


class ScrapingScheduler:
    """Scheduler pour exécuter automatiquement les tâches de scraping"""
    
    def __init__(self, check_interval: int = 60):
        """
        Initialise le scheduler
        
        Args:
            check_interval: Intervalle de vérification en secondes (défaut: 60s)
        """
        self.check_interval = check_interval
        self.db = DatabaseManager()
        self.running = False
        self.thread = None
    
    def start(self):
        """Démarre le scheduler en arrière-plan"""
        if self.running:
            print("⚠️  Le scheduler est déjà en cours d'exécution")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"✅ Scheduler démarré (vérification toutes les {self.check_interval}s)")
    
    def stop(self):
        """Arrête le scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🛑 Scheduler arrêté")
    
    def _run(self):
        """Boucle principale du scheduler"""
        while self.running:
            try:
                self._check_and_execute()
            except Exception as e:
                print(f"❌ Erreur dans le scheduler: {e}")
            
            # Attendre avant la prochaine vérification
            time.sleep(self.check_interval)
    
    def _check_and_execute(self):
        """Vérifie si une tâche doit être exécutée"""
        schedule = self.db.get_scraping_schedule()
        
        if not schedule or not schedule['enabled']:
            return
        
        # Vérifier si next_run est dépassé
        next_run = datetime.fromisoformat(schedule['next_run'])
        now = datetime.now()
        
        if now >= next_run:
            print(f"🚀 Lancement du scraping automatique (fréquence: {schedule['frequency']})")
            self._execute_scraping(schedule)
    
    def _execute_scraping(self, schedule: dict):
        """Exécute le scraping automatique"""
        try:
            # Créer une tâche de scraping
            task_id = self.db.create_scraping_task('automatic', {
                'frequency': schedule['frequency'],
                'days': schedule['days'],
                'fb_posts': schedule['fb_posts'],
                'tweets': schedule['tweets']
            })
            
            # Construire la commande
            script_path = Path(__file__).parent.parent / 'scrape_with_social.py'
            cmd = [
                sys.executable,
                str(script_path),
                '--all',
                '--days', str(schedule['days']),
                '--fb-posts', str(schedule['fb_posts']),
                '--tweets', str(schedule['tweets'])
            ]
            
            # Exécuter le scraping
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            
            if result.returncode == 0:
                # Compter les résultats
                days = schedule['days']
                articles = self.db.get_recent_articles(days=days, limit=10000)
                fb_posts = self.db.get_recent_facebook_posts(days=days, limit=10000)
                tweets = self.db.get_recent_twitter_tweets(days=days, limit=10000)
                
                total_articles = len(articles)
                total_fb_posts = len(fb_posts)
                total_tweets = len(tweets)
                
                # Mettre à jour la tâche
                self.db.update_scraping_task(
                    task_id, 'completed',
                    total_articles=total_articles,
                    total_fb_posts=total_fb_posts,
                    total_tweets=total_tweets
                )
                
                print(f"✅ Scraping automatique terminé: {total_articles} articles, {total_fb_posts} posts FB, {total_tweets} tweets")
            else:
                error_msg = result.stderr or 'Erreur inconnue'
                self.db.update_scraping_task(task_id, 'failed', error_message=error_msg)
                print(f"❌ Échec du scraping automatique: {error_msg}")
            
            # Mettre à jour last_run et next_run
            self.db.update_schedule_last_run()
            
        except subprocess.TimeoutExpired:
            self.db.update_scraping_task(task_id, 'failed', error_message='Timeout')
            print("❌ Le scraping automatique a pris trop de temps")
        except Exception as e:
            if 'task_id' in locals():
                self.db.update_scraping_task(task_id, 'failed', error_message=str(e))
            print(f"❌ Erreur lors du scraping automatique: {e}")


# Instance globale du scheduler
_scheduler_instance = None


def get_scheduler() -> ScrapingScheduler:
    """Récupère l'instance globale du scheduler"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = ScrapingScheduler()
    return _scheduler_instance


def start_scheduler():
    """Démarre le scheduler global"""
    scheduler = get_scheduler()
    scheduler.start()


def stop_scheduler():
    """Arrête le scheduler global"""
    scheduler = get_scheduler()
    scheduler.stop()

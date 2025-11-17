#!/usr/bin/env python
"""
Script pour vérifier que toutes les tables nécessaires existent
"""

from database.db_manager import DatabaseManager

def check_tables():
    """Vérifier que toutes les tables existent"""
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row['name'] for row in cursor.fetchall()]
        
        print("📋 Tables existantes dans la base de données:")
        print("=" * 50)
        for table in tables:
            print(f"  ✓ {table}")
        
        print("\n" + "=" * 50)
        
        # Vérifier les tables critiques pour le scraping
        required_tables = ['scraping_schedule', 'scraping_tasks']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n❌ Tables manquantes: {', '.join(missing_tables)}")
            print("\n💡 Solution: Redémarrez le serveur Django")
            print("   Les tables seront créées automatiquement au démarrage")
            return False
        else:
            print("\n✅ Toutes les tables de scraping sont présentes!")
            
            # Vérifier le contenu
            cursor.execute("SELECT COUNT(*) as count FROM scraping_tasks")
            task_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM scraping_schedule")
            schedule_count = cursor.fetchone()['count']
            
            print(f"\n📊 Statistiques:")
            print(f"  • Tâches de scraping: {task_count}")
            print(f"  • Configurations d'automatisation: {schedule_count}")
            
            return True
    
    finally:
        conn.close()

if __name__ == '__main__':
    check_tables()

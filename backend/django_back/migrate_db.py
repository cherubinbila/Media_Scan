#!/usr/bin/env python3
"""
Script de migration pour ajouter les colonnes manquantes à la table content_moderation
"""

import sqlite3
import os

def migrate_database():
    """Ajoute les colonnes manquantes à la table content_moderation"""
    db_path = 'data/media_scan.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(content_moderation)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"📊 Colonnes actuelles: {columns}")
        
        # Ajouter les colonnes manquantes
        columns_to_add = [
            ("toxicity_details", "TEXT"),
            ("misinformation_details", "TEXT"),
            ("sensitivity_details", "TEXT"),
            ("primary_issue", "TEXT DEFAULT 'none'")
        ]
        
        for col_name, col_type in columns_to_add:
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE content_moderation ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Colonne '{col_name}' ajoutée")
                except sqlite3.OperationalError as e:
                    print(f"⚠️ Erreur lors de l'ajout de '{col_name}': {e}")
            else:
                print(f"ℹ️ Colonne '{col_name}' existe déjà")
        
        conn.commit()
        print("\n✅ Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        conn.rollback()
    
    finally:
        conn.close()


if __name__ == '__main__':
    print("🔧 Démarrage de la migration de la base de données...\n")
    migrate_database()

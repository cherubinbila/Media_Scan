#!/usr/bin/env python
"""Script pour tester les APIs de scraping"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_scraping_trigger():
    """Tester le déclenchement d'un scraping"""
    print("\n" + "="*60)
    print("TEST: POST /api/scraping/trigger/")
    print("="*60)
    
    url = f"{BASE_URL}/scraping/trigger/"
    data = {
        "all": True,
        "days": 7,
        "fb_posts": 10,
        "tweets": 10
    }
    
    print(f"\n📤 Requête: {url}")
    print(f"📦 Body: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"\n📊 Status: {response.status_code}")
        print(f"📄 Réponse:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Scraping lancé avec succès!")
        else:
            print(f"\n❌ Erreur: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️ Timeout - Le scraping prend du temps (c'est normal)")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

def test_scraping_history():
    """Tester la récupération de l'historique"""
    print("\n" + "="*60)
    print("TEST: GET /api/scraping/history/")
    print("="*60)
    
    url = f"{BASE_URL}/scraping/history/?limit=5"
    
    print(f"\n📤 Requête: {url}")
    
    try:
        response = requests.get(url)
        print(f"\n📊 Status: {response.status_code}")
        print(f"📄 Réponse:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Historique récupéré avec succès!")
        else:
            print(f"\n❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

def test_scraping_schedule():
    """Tester la récupération de la configuration"""
    print("\n" + "="*60)
    print("TEST: GET /api/scraping/schedule/")
    print("="*60)
    
    url = f"{BASE_URL}/scraping/schedule/"
    
    print(f"\n📤 Requête: {url}")
    
    try:
        response = requests.get(url)
        print(f"\n📊 Status: {response.status_code}")
        print(f"📄 Réponse:")
        if response.status_code == 404:
            print("  Aucune configuration (normal si première utilisation)")
        else:
            print(json.dumps(response.json(), indent=2))
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    print("\n🧪 TEST DES APIS DE SCRAPING")
    print("="*60)
    
    # Test 1: Historique
    test_scraping_history()
    
    # Test 2: Configuration
    test_scraping_schedule()
    
    # Test 3: Trigger (commenté car prend du temps)
    # test_scraping_trigger()
    
    print("\n" + "="*60)
    print("✅ Tests terminés!")
    print("="*60 + "\n")

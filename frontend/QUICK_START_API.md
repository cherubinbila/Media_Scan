# 🚀 Quick Start - Services API

## ⚡ Démarrage en 3 minutes

### 1. Configuration (30 secondes)

```bash
# Dans le dossier frontend
cd frontend

# Créer le fichier .env
echo VITE_API_URL=http://localhost:8000 > .env
```

### 2. Lancer le backend (1 minute)

```bash
# Dans un autre terminal
cd backend/django_back
python manage.py runserver
```

Le backend doit afficher :

```
Starting development server at http://127.0.0.1:8000/
```

### 3. Tester la connexion (1 minute)

Dans votre code React ou dans la console du navigateur :

```typescript
import { testApi } from "@/services";

// Tester tous les services
await testApi();
```

Vous devriez voir :

```
🧪 Test de connexion à l'API...

1️⃣ Test Health Check...
✅ Health Check réussi: { status: "healthy", database: "connected", version: "1.0.0" }

2️⃣ Test récupération des médias...
✅ 10 médias récupérés

3️⃣ Test récupération des articles...
✅ 135 articles récupérés

...

🎉 Tests terminés !
```

## 📝 Utilisation basique

### Récupérer les médias

```typescript
import { mediaService } from "@/services";

const { data, error } = await mediaService.getAll();

if (data) {
  console.log("Médias:", data);
}
```

### Récupérer le classement

```typescript
import { rankingService } from "@/services";

const { data } = await rankingService.get(30); // 30 derniers jours

if (data) {
  data.forEach((media, index) => {
    console.log(`#${index + 1} - ${media.nom}: ${media.engagement_total}`);
  });
}
```

### Récupérer les statistiques

```typescript
import { statsService } from "@/services";

const { data } = await statsService.get(30);

if (data) {
  console.log(`Total médias: ${data.total_medias}`);
  console.log(`Total articles: ${data.total_articles}`);
  console.log(`Top média: ${data.top_media.nom}`);
}
```

## 🎯 Exemple de composant React

```typescript
import { useState, useEffect } from "react";
import { rankingService, Ranking } from "@/services";

export function RankingList() {
  const [ranking, setRanking] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRanking() {
      const { data } = await rankingService.get(30);
      if (data) setRanking(data);
      setLoading(false);
    }
    fetchRanking();
  }, []);

  if (loading) return <div>Chargement...</div>;

  return (
    <div>
      <h2>Classement des Médias</h2>
      <ol>
        {ranking.map((media) => (
          <li key={media.id}>
            <strong>{media.nom}</strong> -{" "}
            {media.engagement_total.toLocaleString()} engagements
          </li>
        ))}
      </ol>
    </div>
  );
}
```

## 🔧 Dépannage rapide

### ❌ Erreur "Property 'env' does not exist"

✅ **Solution** : Le fichier `vite-env.d.ts` a été créé dans `services/`. Redémarrez votre IDE.

### ❌ Erreur "Failed to fetch"

✅ **Solution** : Vérifiez que le backend Django est bien lancé sur `http://localhost:8000`

```bash
cd backend/django_back
python manage.py runserver
```

### ❌ Erreur "Cannot find module '@/services'"

✅ **Solution** : Vérifiez votre `tsconfig.json` :

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### ❌ Timeout de requête

✅ **Solution** : Le timeout par défaut est de 30 secondes. Si nécessaire, modifiez dans `api.config.ts` :

```typescript
export const API_CONFIG = {
  TIMEOUT: 60000, // 60 secondes
  // ...
};
```

## 📚 Documentation complète

- **Services** : `frontend/services/README.md`
- **Exemples** : `frontend/services/EXAMPLES.md`
- **Intégration** : `frontend/services/INTEGRATION.md`
- **API Backend** : `backend/django_back/API_ENDPOINTS.md`
- **Résumé** : `SERVICES_API_SUMMARY.md`

## ✅ Checklist

- [ ] Fichier `.env` créé
- [ ] Backend Django lancé
- [ ] Test `testApi()` réussi
- [ ] Premier composant créé
- [ ] Données affichées dans l'UI

## 🎉 C'est prêt !

Vous pouvez maintenant utiliser tous les services API dans votre application React !

**Services disponibles** :

- `mediaService` - Médias
- `articleService` - Articles
- `rankingService` - Classement
- `audienceService` - Audience
- `scrapingService` - Scraping
- `statsService` - Statistiques
- `socialService` - Facebook & Twitter
- `classificationService` - Classifications

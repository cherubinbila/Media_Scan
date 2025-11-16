# Guide d'intégration des services API

## 📦 Ce qui a été créé

### Fichiers de configuration

- ✅ `api.config.ts` - Configuration de l'API et endpoints
- ✅ `api.client.ts` - Client HTTP générique avec gestion d'erreurs
- ✅ `types.ts` - Tous les types TypeScript
- ✅ `vite-env.d.ts` - Définitions TypeScript pour Vite

### Services API

- ✅ `media.service.ts` - Gestion des médias
- ✅ `article.service.ts` - Gestion des articles
- ✅ `classification.service.ts` - Classifications thématiques
- ✅ `social.service.ts` - Facebook & Twitter
- ✅ `audience.service.ts` - Analyse d'audience
- ✅ `ranking.service.ts` - Classement des médias
- ✅ `scraping.service.ts` - Déclenchement du scraping
- ✅ `stats.service.ts` - Statistiques et health check

### Documentation

- ✅ `README.md` - Documentation complète
- ✅ `EXAMPLES.md` - Exemples d'utilisation avec React
- ✅ `index.ts` - Point d'entrée pour les imports

### Configuration

- ✅ `.env.example` - Exemple de configuration
- ✅ `tsconfig.app.json` - Mis à jour pour inclure le dossier services

## 🚀 Démarrage rapide

### 1. Configuration de l'environnement

Créer un fichier `.env` à la racine du frontend :

```bash
# Copier l'exemple
cp .env.example .env
```

Contenu du `.env` :

```env
VITE_API_URL=http://localhost:8000
```

### 2. Vérifier que le backend est lancé

```bash
cd backend/django_back
python manage.py runserver
```

Le backend doit être accessible sur `http://localhost:8000`

### 3. Importer les services dans votre code

```typescript
// Import simple
import { mediaService, articleService } from "@/services";

// Import avec types
import { mediaService, articleService, Media, Article } from "@/services";

// Import de tous les services
import * as services from "@/services";
```

### 4. Utilisation basique

```typescript
// Dans un composant React
import { useEffect, useState } from "react";
import { mediaService, Media } from "@/services";

function MyComponent() {
  const [medias, setMedias] = useState<Media[]>([]);

  useEffect(() => {
    async function loadMedias() {
      const { data, error } = await mediaService.getAll();
      if (data) setMedias(data);
    }
    loadMedias();
  }, []);

  return <div>{/* Votre UI */}</div>;
}
```

## 📋 Checklist d'intégration

### Configuration

- [ ] Créer le fichier `.env` avec `VITE_API_URL`
- [ ] Vérifier que le backend Django est lancé
- [ ] Tester la connexion avec `statsService.health()`

### Développement

- [ ] Créer les hooks personnalisés (voir `EXAMPLES.md`)
- [ ] Créer les composants UI
- [ ] Gérer les états de chargement
- [ ] Gérer les erreurs
- [ ] Ajouter le rafraîchissement des données

### Tests

- [ ] Tester chaque service individuellement
- [ ] Tester la gestion des erreurs
- [ ] Tester les timeouts
- [ ] Tester avec le backend déconnecté

## 🔧 Exemples de hooks à créer

### Hook pour les médias

```typescript
// hooks/useMedias.ts
import { useState, useEffect } from "react";
import { mediaService, Media } from "@/services";

export function useMedias() {
  const [medias, setMedias] = useState<Media[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetch() {
      const { data, error } = await mediaService.getAll();
      if (error) setError(error);
      else if (data) setMedias(data);
      setLoading(false);
    }
    fetch();
  }, []);

  return { medias, loading, error };
}
```

### Hook pour le classement

```typescript
// hooks/useRanking.ts
import { useState, useEffect } from "react";
import { rankingService, Ranking } from "@/services";

export function useRanking(days = 30) {
  const [ranking, setRanking] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetch() {
      const { data } = await rankingService.get(days);
      if (data) setRanking(data);
      setLoading(false);
    }
    fetch();
  }, [days]);

  return { ranking, loading };
}
```

### Hook pour les statistiques

```typescript
// hooks/useStats.ts
import { useState, useEffect } from "react";
import { statsService, Stats } from "@/services";

export function useStats(days = 30) {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetch() {
      const { data } = await statsService.get(days);
      if (data) setStats(data);
      setLoading(false);
    }
    fetch();
  }, [days]);

  return { stats, loading };
}
```

## 🎯 Composants suggérés à créer

### 1. Dashboard principal

```
components/
├── Dashboard.tsx           # Vue d'ensemble
├── StatsCards.tsx         # Cartes de statistiques
├── RankingTable.tsx       # Tableau de classement
└── ApiHealthCheck.tsx     # Indicateur de santé de l'API
```

### 2. Gestion des médias

```
components/
├── MediaList.tsx          # Liste des médias
├── MediaCard.tsx          # Carte d'un média
└── MediaDetails.tsx       # Détails d'un média
```

### 3. Articles

```
components/
├── ArticleList.tsx        # Liste des articles
├── ArticleCard.tsx        # Carte d'un article
└── ArticleFilters.tsx     # Filtres pour les articles
```

### 4. Audience

```
components/
├── AudienceChart.tsx      # Graphique d'audience
├── AudienceTable.tsx      # Tableau d'audience
└── PlatformMetrics.tsx    # Métriques par plateforme
```

### 5. Scraping

```
components/
├── ScrapingForm.tsx       # Formulaire de scraping
├── ScrapingStatus.tsx     # Statut du scraping
└── ScrapingHistory.tsx    # Historique des scrapings
```

## 🔄 Gestion des états

### Pattern recommandé avec React Query (optionnel)

Si vous voulez utiliser React Query pour la gestion du cache :

```bash
npm install @tanstack/react-query
```

```typescript
// hooks/useMediasQuery.ts
import { useQuery } from "@tanstack/react-query";
import { mediaService } from "@/services";

export function useMediasQuery() {
  return useQuery({
    queryKey: ["medias"],
    queryFn: async () => {
      const { data, error } = await mediaService.getAll();
      if (error) throw new Error(error);
      return data;
    },
  });
}
```

## 🛡️ Gestion des erreurs

### Composant ErrorBoundary

```typescript
// components/ErrorBoundary.tsx
import { Component, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Une erreur est survenue</h2>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Hook pour la gestion des erreurs

```typescript
// hooks/useErrorHandler.ts
import { useState } from "react";

export function useErrorHandler() {
  const [error, setError] = useState<string | null>(null);

  const handleError = (error: string | null) => {
    setError(error);
    if (error) {
      console.error("API Error:", error);
      // Vous pouvez aussi envoyer à un service de monitoring
    }
  };

  const clearError = () => setError(null);

  return { error, handleError, clearError };
}
```

## 📊 Monitoring et logging

### Service de logging

```typescript
// services/logger.service.ts
export const logger = {
  info: (message: string, data?: any) => {
    console.log(`[INFO] ${message}`, data);
  },

  error: (message: string, error?: any) => {
    console.error(`[ERROR] ${message}`, error);
    // Envoyer à un service de monitoring (Sentry, etc.)
  },

  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data);
  },
};
```

## 🎨 Intégration UI

### Avec Tailwind CSS

```typescript
// components/MediaCard.tsx
import { Media } from "@/services";

export function MediaCard({ media }: { media: Media }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
      <h3 className="text-xl font-bold mb-2">{media.nom}</h3>
      <p className="text-gray-600 mb-4">{media.url}</p>
      <div className="flex gap-2">
        {media.facebook_page && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
            Facebook
          </span>
        )}
        {media.twitter_account && (
          <span className="px-2 py-1 bg-sky-100 text-sky-800 rounded text-sm">
            Twitter
          </span>
        )}
      </div>
    </div>
  );
}
```

## 🚦 Prochaines étapes

1. **Créer les hooks personnalisés** dans `src/hooks/`
2. **Créer les composants UI** dans `src/components/`
3. **Tester la connexion** avec le backend
4. **Implémenter le dashboard** principal
5. **Ajouter la gestion des erreurs**
6. **Optimiser les performances** (cache, lazy loading)
7. **Ajouter les tests** unitaires et d'intégration

## 📚 Ressources

- Documentation API Backend : `backend/django_back/API_ENDPOINTS.md`
- Exemples d'utilisation : `services/EXAMPLES.md`
- Documentation des services : `services/README.md`

## ✅ Validation

Pour vérifier que tout fonctionne :

```typescript
// Test rapide dans la console du navigateur
import { statsService } from "@/services";

const { data, error } = await statsService.health();
console.log("API Health:", data);
```

Si vous voyez `{ status: "healthy", database: "connected", version: "1.0.0" }`, tout est prêt ! 🎉

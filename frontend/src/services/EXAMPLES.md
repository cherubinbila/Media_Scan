# Exemples d'utilisation des services API

## 🎯 Exemples pratiques pour le frontend React

### 1. Hook personnalisé pour récupérer les médias

```typescript
// hooks/useMedias.ts
import { useState, useEffect } from "react";
import { mediaService, Media } from "@/services";

export function useMedias() {
  const [medias, setMedias] = useState<Media[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = async () => {
    setLoading(true);
    const { data, error } = await mediaService.getAll();

    if (error) {
      setError(error);
    } else if (data) {
      setMedias(data);
      setError(null);
    }

    setLoading(false);
  };

  useEffect(() => {
    refetch();
  }, []);

  return { medias, loading, error, refetch };
}
```

### 2. Hook pour le classement des médias

```typescript
// hooks/useRanking.ts
import { useState, useEffect } from "react";
import { rankingService, Ranking } from "@/services";

export function useRanking(days = 30) {
  const [ranking, setRanking] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRanking() {
      setLoading(true);
      const { data, error } = await rankingService.get(days);

      if (error) {
        setError(error);
      } else if (data) {
        setRanking(data);
        setError(null);
      }

      setLoading(false);
    }

    fetchRanking();
  }, [days]);

  return { ranking, loading, error };
}
```

### 3. Hook pour l'audience globale

```typescript
// hooks/useAudience.ts
import { useState, useEffect } from "react";
import { audienceService, AudienceGlobal } from "@/services";

export function useAudience(days = 30) {
  const [audience, setAudience] = useState<AudienceGlobal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAudience() {
      setLoading(true);
      const { data, error } = await audienceService.getGlobal(days);

      if (error) {
        setError(error);
      } else if (data) {
        setAudience(data);
        setError(null);
      }

      setLoading(false);
    }

    fetchAudience();
  }, [days]);

  return { audience, loading, error };
}
```

### 4. Hook pour les statistiques

```typescript
// hooks/useStats.ts
import { useState, useEffect } from "react";
import { statsService, Stats } from "@/services";

export function useStats(days = 30) {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStats() {
      setLoading(true);
      const { data, error } = await statsService.get(days);

      if (error) {
        setError(error);
      } else if (data) {
        setStats(data);
        setError(null);
      }

      setLoading(false);
    }

    fetchStats();
  }, [days]);

  return { stats, loading, error };
}
```

### 5. Hook pour le scraping

```typescript
// hooks/useScraping.ts
import { useState } from "react";
import { scrapingService, ScrapingResponse } from "@/services";

export function useScraping() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ScrapingResponse | null>(null);

  const scrapeMedia = async (
    url: string,
    options?: {
      days?: number;
      fbPosts?: number;
      tweets?: number;
    }
  ) => {
    setLoading(true);
    setError(null);

    const { data, error } = await scrapingService.scrapeMedia(url, options);

    if (error) {
      setError(error);
    } else if (data) {
      setResult(data);
    }

    setLoading(false);
  };

  const scrapeAll = async (options?: {
    days?: number;
    fbPosts?: number;
    tweets?: number;
  }) => {
    setLoading(true);
    setError(null);

    const { data, error } = await scrapingService.scrapeAll(options);

    if (error) {
      setError(error);
    } else if (data) {
      setResult(data);
    }

    setLoading(false);
  };

  return { scrapeMedia, scrapeAll, loading, error, result };
}
```

### 6. Composant Dashboard

```typescript
// components/Dashboard.tsx
import { useStats } from "@/hooks/useStats";
import { useRanking } from "@/hooks/useRanking";

export function Dashboard() {
  const { stats, loading: statsLoading } = useStats(30);
  const { ranking, loading: rankingLoading } = useRanking(30);

  if (statsLoading || rankingLoading) {
    return <div>Chargement...</div>;
  }

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Médias</h3>
          <p>{stats?.total_medias}</p>
        </div>
        <div className="stat-card">
          <h3>Total Articles</h3>
          <p>{stats?.total_articles}</p>
        </div>
        <div className="stat-card">
          <h3>Top Média</h3>
          <p>{stats?.top_media.nom}</p>
        </div>
      </div>

      <div className="ranking">
        <h2>Classement des Médias</h2>
        <table>
          <thead>
            <tr>
              <th>Rang</th>
              <th>Média</th>
              <th>Engagement Total</th>
            </tr>
          </thead>
          <tbody>
            {ranking.map((media, index) => (
              <tr key={media.id}>
                <td>{index + 1}</td>
                <td>{media.nom}</td>
                <td>{media.engagement_total.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

### 7. Composant de scraping

```typescript
// components/ScrapingForm.tsx
import { useState } from "react";
import { useScraping } from "@/hooks/useScraping";

export function ScrapingForm() {
  const [url, setUrl] = useState("");
  const { scrapeMedia, loading, error, result } = useScraping();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await scrapeMedia(url, {
      days: 30,
      fbPosts: 10,
      tweets: 10,
    });
  };

  return (
    <div className="scraping-form">
      <form onSubmit={handleSubmit}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="URL du média"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Scraping en cours..." : "Lancer le scraping"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Résultat du scraping</h3>
          <p>Articles: {result.total_articles}</p>
          <p>Posts Facebook: {result.total_fb_posts}</p>
          <p>Tweets: {result.total_tweets}</p>
        </div>
      )}
    </div>
  );
}
```

### 8. Composant liste d'articles

```typescript
// components/ArticleList.tsx
import { useState, useEffect } from "react";
import { articleService, Article } from "@/services";

export function ArticleList({ mediaId }: { mediaId?: number }) {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchArticles() {
      const { data } = mediaId
        ? await articleService.getByMedia(mediaId, 50)
        : await articleService.getRecent(7, 50);

      if (data) {
        setArticles(data);
      }
      setLoading(false);
    }

    fetchArticles();
  }, [mediaId]);

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="article-list">
      {articles.map((article) => (
        <div key={article.id} className="article-card">
          {article.image_url && (
            <img src={article.image_url} alt={article.titre} />
          )}
          <h3>{article.titre}</h3>
          <p>{article.extrait}</p>
          <div className="meta">
            <span>
              {new Date(article.date_publication).toLocaleDateString()}
            </span>
            {article.auteur && <span>Par {article.auteur}</span>}
          </div>
          <a href={article.url} target="_blank" rel="noopener noreferrer">
            Lire l'article
          </a>
        </div>
      ))}
    </div>
  );
}
```

### 9. Composant d'audience

```typescript
// components/AudienceChart.tsx
import { useAudience } from "@/hooks/useAudience";

export function AudienceChart() {
  const { audience, loading } = useAudience(30);

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="audience-chart">
      <h2>Analyse d'Audience (30 jours)</h2>
      {audience.map((media) => (
        <div key={media.id} className="media-audience">
          <h3>{media.nom}</h3>
          <div className="metrics">
            <div className="metric">
              <span>Publications</span>
              <strong>{media.total_publications}</strong>
            </div>
            <div className="metric">
              <span>Engagement Total</span>
              <strong>{media.total_engagement.toLocaleString()}</strong>
            </div>
            <div className="metric">
              <span>Score d'Influence</span>
              <strong>{media.score_influence.toFixed(2)}</strong>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 10. Vérification de la santé de l'API

```typescript
// components/ApiHealthCheck.tsx
import { useState, useEffect } from "react";
import { statsService, HealthCheck } from "@/services";

export function ApiHealthCheck() {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function checkHealth() {
      const { data, error } = await statsService.health();

      if (error) {
        setError(error);
      } else if (data) {
        setHealth(data);
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Vérifier toutes les 30s

    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div className="health-check error">❌ API non disponible: {error}</div>
    );
  }

  if (!health) {
    return <div className="health-check">Vérification...</div>;
  }

  return (
    <div className="health-check success">
      ✅ API: {health.status} | DB: {health.database} | v{health.version}
    </div>
  );
}
```

## 🔄 Gestion du cache et rafraîchissement

### Hook avec cache et rafraîchissement automatique

```typescript
// hooks/useDataWithRefresh.ts
import { useState, useEffect, useCallback } from "react";

export function useDataWithRefresh<T>(
  fetchFn: () => Promise<{ data?: T; error?: string }>,
  refreshInterval?: number
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    const result = await fetchFn();

    if (result.error) {
      setError(result.error);
    } else if (result.data) {
      setData(result.data);
      setError(null);
    }

    setLoading(false);
  }, [fetchFn]);

  useEffect(() => {
    fetch();

    if (refreshInterval) {
      const interval = setInterval(fetch, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetch, refreshInterval]);

  return { data, loading, error, refetch: fetch };
}

// Utilisation
const { data: stats, refetch } = useDataWithRefresh(
  () => statsService.get(30),
  60000 // Rafraîchir toutes les minutes
);
```

## 🎨 Intégration complète

```typescript
// App.tsx
import { ApiHealthCheck } from "@/components/ApiHealthCheck";
import { Dashboard } from "@/components/Dashboard";
import { ArticleList } from "@/components/ArticleList";
import { AudienceChart } from "@/components/AudienceChart";
import { ScrapingForm } from "@/components/ScrapingForm";

export function App() {
  return (
    <div className="app">
      <header>
        <h1>Media Scanner</h1>
        <ApiHealthCheck />
      </header>

      <main>
        <Dashboard />
        <AudienceChart />
        <ArticleList />
        <ScrapingForm />
      </main>
    </div>
  );
}
```

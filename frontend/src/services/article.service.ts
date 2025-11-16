/**
 * Service pour la gestion des articles
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Article } from './types';

export interface ArticleParams {
  media_id?: number;
  days?: number;
  limit?: number;
}

export const articleService = {
  /**
   * Récupérer les articles avec filtres optionnels
   */
  async getAll(params?: ArticleParams): Promise<ApiResponse<Article[]>> {
    return apiClient.get<Article[]>(API_ENDPOINTS.ARTICLES, params);
  },

  /**
   * Récupérer les articles d'un média spécifique
   */
  async getByMedia(mediaId: number, limit = 100): Promise<ApiResponse<Article[]>> {
    return apiClient.get<Article[]>(API_ENDPOINTS.ARTICLES, {
      media_id: mediaId,
      limit,
    });
  },

  /**
   * Récupérer les articles récents
   */
  async getRecent(days = 7, limit = 100): Promise<ApiResponse<Article[]>> {
    return apiClient.get<Article[]>(API_ENDPOINTS.ARTICLES, {
      days,
      limit,
    });
  },
};

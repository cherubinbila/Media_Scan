/**
 * Service pour la gestion des réseaux sociaux (Facebook & Twitter)
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { FacebookPost, Tweet } from './types';

export interface SocialParams {
  media_id: number;
  limit?: number;
}

export const socialService = {
  facebook: {
    /**
     * Récupérer les posts Facebook d'un média
     */
    async getPosts(mediaId: number, limit = 100): Promise<ApiResponse<FacebookPost[]>> {
      return apiClient.get<FacebookPost[]>(API_ENDPOINTS.FACEBOOK_POSTS, {
        media_id: mediaId,
        limit,
      });
    },
  },

  twitter: {
    /**
     * Récupérer les tweets d'un média
     */
    async getTweets(mediaId: number, limit = 100): Promise<ApiResponse<Tweet[]>> {
      return apiClient.get<Tweet[]>(API_ENDPOINTS.TWITTER_TWEETS, {
        media_id: mediaId,
        limit,
      });
    },
  },
};

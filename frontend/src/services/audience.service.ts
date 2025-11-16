/**
 * Service pour l'analyse d'audience
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import {
  AudienceWeb,
  AudienceFacebook,
  AudienceTwitter,
  AudienceGlobal,
  InactiveMedias,
} from './types';

export const audienceService = {
  /**
   * Récupérer l'audience Web
   */
  async getWeb(days = 30): Promise<ApiResponse<AudienceWeb[]>> {
    return apiClient.get<AudienceWeb[]>(API_ENDPOINTS.AUDIENCE_WEB, { days });
  },

  /**
   * Récupérer l'audience Facebook
   */
  async getFacebook(days = 30): Promise<ApiResponse<AudienceFacebook[]>> {
    return apiClient.get<AudienceFacebook[]>(API_ENDPOINTS.AUDIENCE_FACEBOOK, {
      days,
    });
  },

  /**
   * Récupérer l'audience Twitter
   */
  async getTwitter(days = 30): Promise<ApiResponse<AudienceTwitter[]>> {
    return apiClient.get<AudienceTwitter[]>(API_ENDPOINTS.AUDIENCE_TWITTER, {
      days,
    });
  },

  /**
   * Récupérer l'audience globale (toutes plateformes)
   */
  async getGlobal(days = 30): Promise<ApiResponse<AudienceGlobal[]>> {
    return apiClient.get<AudienceGlobal[]>(API_ENDPOINTS.AUDIENCE_GLOBAL, {
      days,
    });
  },

  /**
   * Récupérer les médias inactifs
   */
  async getInactive(daysThreshold = 7): Promise<ApiResponse<InactiveMedias>> {
    return apiClient.get<InactiveMedias>(API_ENDPOINTS.AUDIENCE_INACTIVE, {
      days_threshold: daysThreshold,
    });
  },
};

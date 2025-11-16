/**
 * Service pour le scraping
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { ScrapingRequest, ScrapingResponse } from './types';

export const scrapingService = {
  /**
   * Déclencher un scraping
   */
  async trigger(request: ScrapingRequest): Promise<ApiResponse<ScrapingResponse>> {
    return apiClient.post<ScrapingResponse>(
      API_ENDPOINTS.SCRAPING_TRIGGER,
      request
    );
  },

  /**
   * Scraper un média spécifique
   */
  async scrapeMedia(
    url: string,
    options?: {
      days?: number;
      fbPosts?: number;
      tweets?: number;
      skipFacebook?: boolean;
      skipTwitter?: boolean;
    }
  ): Promise<ApiResponse<ScrapingResponse>> {
    return this.trigger({
      url,
      all: false,
      days: options?.days,
      fb_posts: options?.fbPosts,
      tweets: options?.tweets,
      skip_facebook: options?.skipFacebook,
      skip_twitter: options?.skipTwitter,
    });
  },

  /**
   * Scraper tous les médias
   */
  async scrapeAll(options?: {
    days?: number;
    fbPosts?: number;
    tweets?: number;
  }): Promise<ApiResponse<ScrapingResponse>> {
    return this.trigger({
      all: true,
      days: options?.days,
      fb_posts: options?.fbPosts,
      tweets: options?.tweets,
    });
  },
};

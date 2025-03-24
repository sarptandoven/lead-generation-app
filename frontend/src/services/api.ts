import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export interface LeadGenerationConfig {
  industry: string;
  targetMarket: string;
  companySize: string;
  location: string;
  keywords: string[];
  excludeKeywords: string[];
  minimumScore: number;
}

export interface Lead {
  firstName: string;
  lastName: string;
  email: string | null;
  phone: string | null;
  location: string | null;
  source: string;
  qualityScore: number;
  timestamp: string;
}

export interface LeadInsight {
  category: string;
  score: number;
  recommendation: string;
}

export interface AnalyticsData {
  leadsBySource: Record<string, number>;
  conversionRates: Record<string, number>;
  qualityScores: Record<string, number>;
  trends: {
    date: string;
    leads: number;
    conversions: number;
  }[];
}

export interface ScrapingResult {
  leads: Lead[];
  totalFound: number;
  qualityScore: number;
  source: string;
  timestamp: string;
}

class ApiService {
  private axios = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Initialize the API service with authentication
  public initialize(token: string) {
    this.axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  // Web Scraping
  public async scrapeSource(sources: string[], query: string): Promise<ScrapingResult> {
    const response = await this.axios.post<ScrapingResult>('/api/scrape', {
      sources,
      query,
      options: {
        requireContactInfo: true,
        maxResults: 100,
      },
    });
    return response.data;
  }

  public async exportToCSV(leads: Lead[]): Promise<string> {
    const response = await this.axios.post<Blob>('/api/export/csv', { leads }, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `leads_${new Date().toISOString()}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return url;
  }

  // Lead Management
  public async getLeads(params: {
    page: number;
    limit: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
    status?: string;
    minScore?: number;
    source?: string;
    hasEmail?: boolean;
    hasPhone?: boolean;
  }) {
    const response = await this.axios.get('/api/leads', { params });
    return response.data;
  }

  public async updateLead(id: string, data: Partial<Lead>) {
    const response = await this.axios.patch(`/api/leads/${id}`, data);
    return response.data;
  }

  // AI Analysis
  public async analyzeLeadQuality(leads: Lead[]) {
    const response = await this.axios.post('/api/analyze/quality', { leads });
    return response.data;
  }

  public async getLeadInsights(leadId: string) {
    const response = await this.axios.get(`/api/leads/${leadId}/insights`);
    return response.data;
  }

  public async getAggregatedInsights() {
    const response = await this.axios.get('/api/insights/aggregate');
    return response.data;
  }

  // Analytics
  public async getAnalytics(timeframe: '7d' | '30d' | '90d') {
    const response = await this.axios.get('/api/analytics', {
      params: { timeframe },
    });
    return response.data as AnalyticsData;
  }

  // Error Handling
  private handleError(error: any) {
    if (error.response) {
      throw new Error(error.response.data.message || 'An error occurred');
    } else if (error.request) {
      throw new Error('No response from server');
    } else {
      throw new Error('Error setting up request');
    }
  }
}

export const apiService = new ApiService(); 
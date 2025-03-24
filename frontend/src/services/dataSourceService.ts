import { SourceConfig } from '../contexts/DataSourceContext';

export interface LeadSearchParams {
  query?: string;
  location?: string[];
  industry?: string[];
  companySize?: string[];
  founded?: string;
  revenue?: string;
  page?: number;
  limit?: number;
}

export interface Lead {
  id: string;
  source: string;
  companyName: string;
  industry?: string;
  location?: string;
  size?: string;
  revenue?: string;
  founded?: string;
  description?: string;
  website?: string;
  contacts?: Contact[];
  lastUpdated: string;
  confidence: number;
}

interface Contact {
  name: string;
  title?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
}

class DataSourceService {
  private apiBaseUrl: string;

  constructor() {
    this.apiBaseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
  }

  async configureSource(sourceId: string, config: Partial<SourceConfig>): Promise<SourceConfig> {
    const response = await fetch(`${this.apiBaseUrl}/api/sources/${sourceId}/configure`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });

    if (!response.ok) {
      throw new Error(`Failed to configure source: ${response.statusText}`);
    }

    return response.json();
  }

  async testSourceConnection(sourceId: string): Promise<{ success: boolean; error?: string }> {
    const response = await fetch(`${this.apiBaseUrl}/api/sources/${sourceId}/test`, {
      method: 'POST',
    });

    return response.json();
  }

  async searchLeads(
    sources: string[],
    params: LeadSearchParams
  ): Promise<{ leads: Lead[]; total: number }> {
    const queryParams = new URLSearchParams({
      sources: sources.join(','),
      ...Object.entries(params).reduce((acc, [key, value]) => ({
        ...acc,
        [key]: Array.isArray(value) ? value.join(',') : value,
      }), {}),
    });

    const response = await fetch(`${this.apiBaseUrl}/api/leads/search?${queryParams}`);

    if (!response.ok) {
      throw new Error(`Failed to search leads: ${response.statusText}`);
    }

    return response.json();
  }

  async getSourceStats(sourceId: string): Promise<{
    totalLeads: number;
    lastSync: string;
    requestsRemaining: number;
    requestsLimit: number;
  }> {
    const response = await fetch(`${this.apiBaseUrl}/api/sources/${sourceId}/stats`);

    if (!response.ok) {
      throw new Error(`Failed to get source stats: ${response.statusText}`);
    }

    return response.json();
  }

  async syncSource(sourceId: string): Promise<{ status: string; message: string }> {
    const response = await fetch(`${this.apiBaseUrl}/api/sources/${sourceId}/sync`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Failed to sync source: ${response.statusText}`);
    }

    return response.json();
  }

  async getSourceFilters(sourceId: string): Promise<{
    locations: string[];
    industries: string[];
    companySizes: string[];
  }> {
    const response = await fetch(`${this.apiBaseUrl}/api/sources/${sourceId}/filters`);

    if (!response.ok) {
      throw new Error(`Failed to get source filters: ${response.statusText}`);
    }

    return response.json();
  }
}

export const dataSourceService = new DataSourceService();
export default dataSourceService; 
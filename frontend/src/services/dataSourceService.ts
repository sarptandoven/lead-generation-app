import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface LeadSearchParams {
  query?: string;
  location?: string[];
  industry?: string[];
  companySize?: string[];
  founded?: string;
  revenue?: string;
  roles?: string[];
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
  roles?: string[];
}

export interface Contact {
  name: string;
  title?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
}

export interface RoleCategory {
  id: string;
  name: string;
  roles: string[];
  description: string;
}

class DataSourceService {
  async configureSource(sourceId: string, config: any): Promise<any> {
    try {
      const response = await apiClient.post(`/sources/${sourceId}/configure`, config);
      return response.data;
    } catch (error) {
      console.error('Error configuring source:', error);
      throw error;
    }
  }

  async testSourceConnection(sourceId: string): Promise<{ success: boolean; error?: string }> {
    try {
      const response = await apiClient.post(`/sources/${sourceId}/test`);
      return response.data as { success: boolean; error?: string };
    } catch (error) {
      console.error('Error testing source connection:', error);
      throw error;
    }
  }

  async searchLeads(
    sources: string[],
    params: LeadSearchParams
  ): Promise<{ leads: Lead[]; total: number }> {
    try {
      const queryParams = new URLSearchParams();
      queryParams.append('sources', sources.join(','));
      
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          if (Array.isArray(value)) {
            queryParams.append(key, value.join(','));
          } else {
            queryParams.append(key, String(value));
          }
        }
      });

      const response = await apiClient.get(`/leads/search?${queryParams}`);
      return response.data as { leads: Lead[]; total: number };
    } catch (error) {
      console.error('Error searching leads:', error);
      throw error;
    }
  }

  async getSourceStats(sourceId: string): Promise<{
    totalLeads: number;
    lastSync: string;
    requestsRemaining: number;
    requestsLimit: number;
  }> {
    try {
      const response = await apiClient.get(`/sources/${sourceId}/stats`);
      return response.data as {
        totalLeads: number;
        lastSync: string;
        requestsRemaining: number;
        requestsLimit: number;
      };
    } catch (error) {
      console.error('Error getting source stats:', error);
      throw error;
    }
  }

  async syncSource(sourceId: string): Promise<{ status: string; message: string }> {
    try {
      const response = await apiClient.post(`/sources/${sourceId}/sync`);
      return response.data as { status: string; message: string };
    } catch (error) {
      console.error('Error syncing source:', error);
      throw error;
    }
  }

  async getSourceFilters(sourceId: string): Promise<{
    locations: string[];
    industries: string[];
    companySizes: string[];
  }> {
    try {
      const response = await apiClient.get(`/sources/${sourceId}/filters`);
      return response.data as {
        locations: string[];
        industries: string[];
        companySizes: string[];
      };
    } catch (error) {
      console.error('Error getting source filters:', error);
      throw error;
    }
  }

  async getRoleCategories(): Promise<RoleCategory[]> {
    try {
      const response = await apiClient.get(`/roles/categories`);
      return response.data as RoleCategory[];
    } catch (error) {
      console.error('Error getting role categories:', error);
      throw error;
    }
  }

  async searchRoles(query: string): Promise<string[]> {
    try {
      const response = await apiClient.get(`/roles/search?q=${encodeURIComponent(query)}`);
      return response.data as string[];
    } catch (error) {
      console.error('Error searching roles:', error);
      throw error;
    }
  }

  async getPopularRoles(): Promise<string[]> {
    try {
      const response = await apiClient.get(`/roles/popular`);
      return response.data as string[];
    } catch (error) {
      console.error('Error getting popular roles:', error);
      throw error;
    }
  }

  async getRoleStats(roles: string[]): Promise<{
    totalLeads: number;
    averageSeniority: string;
    topIndustries: { industry: string; count: number }[];
    roleDistribution: { role: string; percentage: number }[];
  }> {
    try {
      const queryParams = new URLSearchParams({
        roles: roles.join(','),
      });

      const response = await apiClient.get(`/roles/stats?${queryParams}`);
      return response.data as {
        totalLeads: number;
        averageSeniority: string;
        topIndustries: { industry: string; count: number }[];
        roleDistribution: { role: string; percentage: number }[];
      };
    } catch (error) {
      console.error('Error getting role stats:', error);
      throw error;
    }
  }
}

export const dataSourceService = new DataSourceService();
export default dataSourceService; 
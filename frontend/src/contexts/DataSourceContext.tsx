import React, { createContext, useContext, useState, useCallback } from 'react';
import { DataSource } from '../components/DataSourceSelector';

interface DataSourceContextType {
  selectedSources: string[];
  sourceConfigs: Record<string, SourceConfig>;
  setSelectedSources: (sources: string[]) => void;
  updateSourceConfig: (sourceId: string, config: Partial<SourceConfig>) => void;
  isConfigured: (sourceId: string) => boolean;
}

export interface SourceConfig {
  apiKey?: string;
  credentials?: {
    clientId?: string;
    clientSecret?: string;
    refreshToken?: string;
  };
  filters?: {
    location?: string[];
    industry?: string[];
    companySize?: string[];
    founded?: string;
    revenue?: string;
    roles?: string[];
  };
  rateLimit?: {
    requestsPerMinute: number;
    maxRequests: number;
  };
  status: 'unconfigured' | 'configuring' | 'configured' | 'error';
  lastSync?: string;
  error?: string;
}

const defaultSourceConfigs: Record<string, SourceConfig> = {
  linkedin: {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 100,
      maxRequests: 1000,
    },
  },
  google: {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 300,
      maxRequests: 3000,
    },
  },
  bing: {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 150,
      maxRequests: 1500,
    },
  },
  'yellow-pages': {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 200,
      maxRequests: 2000,
    },
  },
  crunchbase: {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 50,
      maxRequests: 500,
    },
  },
  'role-based': {
    status: 'unconfigured',
    rateLimit: {
      requestsPerMinute: 200,
      maxRequests: 2000,
    },
    filters: {
      roles: [],
    },
  },
};

const DataSourceContext = createContext<DataSourceContextType | undefined>(undefined);

export const DataSourceProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [sourceConfigs, setSourceConfigs] = useState<Record<string, SourceConfig>>(defaultSourceConfigs);

  const updateSourceConfig = useCallback((sourceId: string, config: Partial<SourceConfig>) => {
    setSourceConfigs(prev => ({
      ...prev,
      [sourceId]: {
        ...prev[sourceId],
        ...config,
      },
    }));
  }, []);

  const isConfigured = useCallback((sourceId: string) => {
    return sourceConfigs[sourceId]?.status === 'configured';
  }, [sourceConfigs]);

  const value = {
    selectedSources,
    sourceConfigs,
    setSelectedSources,
    updateSourceConfig,
    isConfigured,
  };

  return (
    <DataSourceContext.Provider value={value}>
      {children}
    </DataSourceContext.Provider>
  );
};

export const useDataSources = () => {
  const context = useContext(DataSourceContext);
  if (context === undefined) {
    throw new Error('useDataSources must be used within a DataSourceProvider');
  }
  return context;
};

export default DataSourceContext; 
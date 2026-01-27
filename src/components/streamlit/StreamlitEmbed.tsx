'use client';

import React, { useState, useEffect } from 'react';
import { BarChart3, ExternalLink, AlertCircle } from 'lucide-react';

interface StreamlitEmbedProps {
  streamlitUrl?: string;
  height?: string;
  showControls?: boolean;
}

const StreamlitEmbed: React.FC<StreamlitEmbedProps> = ({
  streamlitUrl = 'https://business-health-dashboard-1.onrender.com',
  height = '800px',
  showControls = true
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              📊 Streamlit Dashboard
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Advanced analytics with real-time controls
            </p>
          </div>
        </div>
        
        {showControls && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => window.open(streamlitUrl, '_blank')}
              className="flex items-center gap-2 px-3 py-1.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
            >
              <ExternalLink className="w-4 h-4" />
              Open in New Tab
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="relative" style={{ height }}>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-gray-600 dark:text-gray-400">Loading Streamlit Dashboard...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="flex items-center gap-3 text-red-500">
              <AlertCircle className="w-6 h-6" />
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Streamlit Embed */}
        <iframe
          src={streamlitUrl}
          className="w-full h-full border-0"
          onLoad={() => setIsLoading(false)}
          onError={() => setError('Failed to load Streamlit dashboard')}
          title="Executive Dashboard"
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
        />
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            🔗 Powered by Streamlit
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Full dashboard functionality available in new tab
          </div>
        </div>
      </div>
    </div>
  );
};

export default StreamlitEmbed;

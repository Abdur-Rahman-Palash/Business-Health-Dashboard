'use client';

import React, { useState, useEffect } from 'react';
import { BarChart3, ExternalLink, AlertCircle, RefreshCw } from 'lucide-react';

interface LocalStreamlitEmbedProps {
  height?: string;
  showControls?: boolean;
}

const LocalStreamlitEmbed: React.FC<LocalStreamlitEmbedProps> = ({
  height = '800px',
  showControls = true
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [streamlitUrl] = useState('http://localhost:8501');

  const handleRefresh = () => {
    setIsLoading(true);
    setError(null);
    // Force iframe reload
    const iframe = document.querySelector('iframe[src*="localhost:8501"]') as HTMLIFrameElement;
    if (iframe) {
      iframe.src = iframe.src;
    }
  };

  return (
    <div className="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              📊 Local Streamlit Dashboard
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Development server with file upload support
            </p>
          </div>
        </div>
        
        {showControls && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleRefresh}
              className="flex items-center gap-2 px-3 py-1.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            <button
              onClick={() => window.open(streamlitUrl, '_blank')}
              className="flex items-center gap-2 px-3 py-1.5 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm"
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
              <span className="text-gray-600 dark:text-gray-400">Loading Local Streamlit...</span>
            </div>
          </div>
        )}

        <iframe
          src={streamlitUrl}
          className="w-full h-full border-0"
          onLoad={() => setIsLoading(false)}
          onError={() => setError('Failed to load Streamlit dashboard. Please make sure Streamlit server is running on port 8501.')}
          title="Local Executive Dashboard"
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-top-navigation"
        />

        {error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 p-8">
            <div className="flex items-center gap-3 text-red-500 mb-4">
              <AlertCircle className="w-6 h-6" />
              <span className="font-medium">{error}</span>
            </div>
            <div className="text-center space-y-4">
              <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
                <h4 className="font-semibold mb-2">🚀 Quick Start:</h4>
                <div className="text-sm space-y-2 text-left">
                  <p>1. Open a new terminal</p>
                  <p>2. Run: <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">cd "c:\Users\USER\Desktop\executive-dashboard"</code></p>
                  <p>3. Run: <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">.\.venv\Scripts\streamlit.exe run run_local_streamlit.py --server.port 8501</code></p>
                </div>
              </div>
              <button
                onClick={handleRefresh}
                className="flex items-center gap-2 mx-auto px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Retry Connection
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            🔗 Local Streamlit Server: {streamlitUrl}
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-400">
            File uploads enabled locally
          </div>
        </div>
      </div>
    </div>
  );
};

export default LocalStreamlitEmbed;

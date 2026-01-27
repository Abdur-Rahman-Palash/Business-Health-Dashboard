'use client';

import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';

const ThemeToggle: React.FC = () => {
  try {
    const { theme, toggleTheme } = useTheme();

    const handleClick = () => {
      console.log('Theme toggle clicked, current theme:', theme);
      toggleTheme();
    };

    return (
      <button
        onClick={handleClick}
        className="flex items-center gap-2 p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
        aria-label="Toggle theme"
        title="Toggle between light and dark mode"
      >
        {theme === 'light' ? (
          <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
        ) : (
          <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300" />
        )}
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 hidden sm:inline">
          {theme === 'light' ? 'Dark' : 'Light'}
        </span>
      </button>
    );
  } catch (error) {
    console.error('ThemeToggle error:', error);
    return (
      <button
        className="flex items-center gap-2 p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
        aria-label="Toggle theme"
        onClick={() => console.log('Theme toggle fallback')}
      >
        <Moon className="w-5 h-5 text-gray-700" />
        <span className="text-sm font-medium text-gray-700 hidden sm:inline">Theme</span>
      </button>
    );
  }
};

export default ThemeToggle;

import React, { useState, useEffect } from 'react';
import { adminAPI } from '../services/api';

const AdminStats = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getDashboardStats();
      setStats(data);
    } catch (err) {
      setError('Failed to load dashboard statistics');
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="text-red-400">⚠️</div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">{error}</div>
            <div className="mt-4">
              <button
                onClick={fetchStats}
                className="bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded text-sm"
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Users',
      value: stats?.total_users || 0,
      icon: '👥',
      color: 'bg-blue-500',
      textColor: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Active Users',
      value: stats?.active_users || 0,
      icon: '✅',
      color: 'bg-green-500',
      textColor: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Admin Users',
      value: stats?.admin_users || 0,
      icon: '👑',
      color: 'bg-purple-500',
      textColor: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      title: 'Inactive Users',
      value: stats?.inactive_users || 0,
      icon: '⏸️',
      color: 'bg-yellow-500',
      textColor: 'text-yellow-600',
      bgColor: 'bg-yellow-50',
    },
    {
      title: 'Total Todos',
      value: stats?.total_todos || 0,
      icon: '📝',
      color: 'bg-indigo-500',
      textColor: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
    },
    {
      title: 'Completed Todos',
      value: stats?.completed_todos || 0,
      icon: '✔️',
      color: 'bg-green-500',
      textColor: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Pending Todos',
      value: stats?.pending_todos || 0,
      icon: '⏳',
      color: 'bg-orange-500',
      textColor: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
    {
      title: 'New Users (7 days)',
      value: stats?.recent_users || 0,
      icon: '🆕',
      color: 'bg-pink-500',
      textColor: 'text-pink-600',
      bgColor: 'bg-pink-50',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard Overview</h2>
        <button
          onClick={fetchStats}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
        >
          <span>🔄</span>
          <span>Refresh</span>
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <div key={index} className={`${card.bgColor} overflow-hidden shadow rounded-lg`}>
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`${card.color} rounded-md p-3 text-white text-xl`}>
                    {card.icon}
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className={`text-sm font-medium ${card.textColor} truncate`}>
                      {card.title}
                    </dt>
                    <dd>
                      <div className={`text-2xl font-bold ${card.textColor}`}>
                        {card.value.toLocaleString()}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Completion Rate */}
      {stats && stats.total_todos > 0 && (
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Overall Completion Rate</h3>
            <div className="flex items-center">
              <div className="flex-1">
                <div className="bg-gray-200 rounded-full h-4">
                  <div
                    className="bg-green-500 h-4 rounded-full transition-all duration-500"
                    style={{ width: `${stats.completion_rate}%` }}
                  ></div>
                </div>
              </div>
              <div className="ml-4">
                <span className="text-2xl font-bold text-green-600">
                  {stats.completion_rate}%
                </span>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-600">
              {stats.completed_todos} of {stats.total_todos} todos completed
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => window.location.href = '/admin#users'}
              className="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-3 rounded-md text-sm font-medium flex items-center justify-center space-x-2 border border-blue-200"
            >
              <span>👥</span>
              <span>Manage Users</span>
            </button>
            <button
              onClick={() => window.location.href = '/admin#todos'}
              className="bg-green-50 hover:bg-green-100 text-green-700 px-4 py-3 rounded-md text-sm font-medium flex items-center justify-center space-x-2 border border-green-200"
            >
              <span>📝</span>
              <span>View All Todos</span>
            </button>
            <button
              onClick={() => window.location.href = '/dashboard'}
              className="bg-gray-50 hover:bg-gray-100 text-gray-700 px-4 py-3 rounded-md text-sm font-medium flex items-center justify-center space-x-2 border border-gray-200"
            >
              <span>🏠</span>
              <span>User Dashboard</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminStats;

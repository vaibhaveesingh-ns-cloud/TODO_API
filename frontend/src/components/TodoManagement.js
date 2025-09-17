import React, { useState, useEffect } from 'react';
import { adminAPI } from '../services/api';

const TodoManagement = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    user_id: '',
    completed: '',
    limit: 50,
    offset: 0
  });
  const [totalTodos, setTotalTodos] = useState(0);
  const [users, setUsers] = useState([]);
  const [actionLoading, setActionLoading] = useState({});

  useEffect(() => {
    fetchUsers();
    fetchTodos();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    fetchTodos();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  const fetchUsers = async () => {
    try {
      const userData = await adminAPI.getUsers();
      setUsers(userData);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== '' && value !== null)
      );
      const data = await adminAPI.getAllTodos(cleanFilters);
      setTodos(data.todos || []);
      setTotalTodos(data.total || 0);
    } catch (err) {
      setError('Failed to load todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    if (!window.confirm('Are you sure you want to delete this todo? This action cannot be undone.')) {
      return;
    }

    try {
      setActionLoading(prev => ({ ...prev, [todoId]: 'delete' }));
      await adminAPI.deleteTodo(todoId);
      setTodos(prev => prev.filter(todo => todo.id !== todoId));
      setTotalTodos(prev => prev - 1);
    } catch (err) {
      console.error('Error deleting todo:', err);
      alert('Failed to delete todo. Please try again.');
    } finally {
      setActionLoading(prev => ({ ...prev, [todoId]: null }));
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      offset: 0 // Reset offset when changing filters
    }));
  };

  const handleLoadMore = () => {
    setFilters(prev => ({
      ...prev,
      offset: prev.offset + prev.limit
    }));
  };

  const getStatusBadge = (completed) => {
    return completed ? (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        ✓ Completed
      </span>
    ) : (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        ⏳ Pending
      </span>
    );
  };

  if (loading && todos.length === 0) {
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
                onClick={fetchTodos}
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Todo Management</h2>
        <button
          onClick={fetchTodos}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
        >
          <span>🔄</span>
          <span>Refresh</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              User
            </label>
            <select
              value={filters.user_id}
              onChange={(e) => handleFilterChange('user_id', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Users</option>
              {users.map(user => (
                <option key={user.id} value={user.id}>
                  {user.username} ({user.email})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={filters.completed}
              onChange={(e) => handleFilterChange('completed', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Todos</option>
              <option value="true">Completed</option>
              <option value="false">Pending</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Limit
            </label>
            <select
              value={filters.limit}
              onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={25}>25 per page</option>
              <option value={50}>50 per page</option>
              <option value={100}>100 per page</option>
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={() => setFilters({ user_id: '', completed: '', limit: 50, offset: 0 })}
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Results Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
        <div className="flex items-center">
          <div className="text-blue-400">📊</div>
          <div className="ml-3">
            <p className="text-sm text-blue-800">
              Showing {todos.length} of {totalTodos} todos
              {filters.user_id && (
                <span className="ml-2">
                  • Filtered by user: {users.find(u => u.id.toString() === filters.user_id)?.username}
                </span>
              )}
              {filters.completed !== '' && (
                <span className="ml-2">
                  • Status: {filters.completed === 'true' ? 'Completed' : 'Pending'}
                </span>
              )}
            </p>
          </div>
        </div>
      </div>

      {/* Todos List */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {todos.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {todos.map((todo) => (
              <li key={todo.id} className="px-4 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3">
                      <div className="flex-shrink-0">
                        <div className={`h-8 w-8 rounded-full flex items-center justify-center text-white text-xs font-bold ${
                          todo.completed ? 'bg-green-500' : 'bg-yellow-500'
                        }`}>
                          {todo.owner_username.charAt(0).toUpperCase()}
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2">
                          <p className={`text-sm font-medium text-gray-900 truncate ${
                            todo.completed ? 'line-through' : ''
                          }`}>
                            {todo.title}
                          </p>
                          {getStatusBadge(todo.completed)}
                        </div>
                        {todo.description && (
                          <p className="text-sm text-gray-500 truncate mt-1">
                            {todo.description}
                          </p>
                        )}
                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-400">
                          <span>👤 {todo.owner_username}</span>
                          <span>📧 {todo.owner_email}</span>
                          <span>📅 {new Date(todo.created_at).toLocaleDateString()}</span>
                          <span>🆔 #{todo.id}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleDeleteTodo(todo.id)}
                      disabled={actionLoading[todo.id]}
                      className={`px-3 py-1 text-xs rounded bg-red-100 text-red-700 hover:bg-red-200 ${
                        actionLoading[todo.id] ? 'opacity-50 cursor-not-allowed' : ''
                      }`}
                    >
                      {actionLoading[todo.id] === 'delete' ? '...' : 'Delete'}
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="px-4 py-12 text-center">
            <div className="text-gray-400 text-4xl mb-4">📝</div>
            <p className="text-gray-500">No todos found with current filters</p>
          </div>
        )}
      </div>

      {/* Load More Button */}
      {todos.length > 0 && todos.length < totalTodos && (
        <div className="text-center">
          <button
            onClick={handleLoadMore}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading...' : `Load More (${totalTodos - todos.length} remaining)`}
          </button>
        </div>
      )}
    </div>
  );
};

export default TodoManagement;

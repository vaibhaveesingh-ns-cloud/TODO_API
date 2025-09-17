import React, { useState, useEffect } from 'react';
import { adminAPI } from '../services/api';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [userTodos, setUserTodos] = useState([]);
  const [loadingTodos, setLoadingTodos] = useState(false);
  const [actionLoading, setActionLoading] = useState({});

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getUsersWithStats();
      setUsers(data);
    } catch (err) {
      setError('Failed to load users');
      console.error('Error fetching users:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserTodos = async (userId) => {
    try {
      setLoadingTodos(true);
      const todos = await adminAPI.getUserTodos(userId);
      setUserTodos(todos);
    } catch (err) {
      console.error('Error fetching user todos:', err);
      setUserTodos([]);
    } finally {
      setLoadingTodos(false);
    }
  };

  const handleUserAction = async (userId, action) => {
    try {
      setActionLoading(prev => ({ ...prev, [userId]: action }));
      
      let result;
      switch (action) {
        case 'promote':
          result = await adminAPI.promoteUser(userId);
          break;
        case 'demote':
          result = await adminAPI.demoteUser(userId);
          break;
        case 'activate':
          result = await adminAPI.activateUser(userId);
          break;
        case 'deactivate':
          result = await adminAPI.deactivateUser(userId);
          break;
        case 'delete':
          if (window.confirm('Are you sure you want to delete this user and all their todos? This action cannot be undone.')) {
            await adminAPI.deleteUser(userId);
            await fetchUsers(); // Refresh the list
            if (selectedUser?.id === userId) {
              setSelectedUser(null);
              setUserTodos([]);
            }
            return;
          } else {
            return;
          }
        default:
          return;
      }

      // Update the user in the list
      setUsers(prev => prev.map(user => 
        user.id === userId ? { ...user, ...result } : user
      ));

      // Update selected user if it's the same
      if (selectedUser?.id === userId) {
        setSelectedUser(prev => ({ ...prev, ...result }));
      }

    } catch (err) {
      console.error(`Error performing ${action}:`, err);
      alert(`Failed to ${action} user. Please try again.`);
    } finally {
      setActionLoading(prev => ({ ...prev, [userId]: null }));
    }
  };

  const handleUserSelect = (user) => {
    setSelectedUser(user);
    fetchUserTodos(user.id);
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
                onClick={fetchUsers}
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
        <h2 className="text-2xl font-bold text-gray-900">User Management</h2>
        <button
          onClick={fetchUsers}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
        >
          <span>🔄</span>
          <span>Refresh</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Users List */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                All Users ({users.length})
              </h3>
            </div>
            <ul className="divide-y divide-gray-200">
              {users.map((user) => (
                <li key={user.id} className="px-4 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className={`h-10 w-10 rounded-full flex items-center justify-center text-white font-bold ${
                          user.is_admin ? 'bg-purple-500' : user.is_active ? 'bg-green-500' : 'bg-gray-400'
                        }`}>
                          {user.username.charAt(0).toUpperCase()}
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="flex items-center space-x-2">
                          <p className="text-sm font-medium text-gray-900">{user.username}</p>
                          {user.is_admin && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                              Admin
                            </span>
                          )}
                          {!user.is_active && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                              Inactive
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-500">{user.email}</p>
                        <div className="text-xs text-gray-400 mt-1">
                          {user.todo_count} todos • {user.completed_count} completed • {user.completion_rate}% rate
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleUserSelect(user)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        View Details
                      </button>
                      <div className="flex space-x-1">
                        {/* Admin Toggle */}
                        <button
                          onClick={() => handleUserAction(user.id, user.is_admin ? 'demote' : 'promote')}
                          disabled={actionLoading[user.id]}
                          className={`px-2 py-1 text-xs rounded ${
                            user.is_admin 
                              ? 'bg-purple-100 text-purple-700 hover:bg-purple-200' 
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          } ${actionLoading[user.id] ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          {actionLoading[user.id] === (user.is_admin ? 'demote' : 'promote') ? '...' : (user.is_admin ? 'Demote' : 'Promote')}
                        </button>
                        
                        {/* Active Toggle */}
                        <button
                          onClick={() => handleUserAction(user.id, user.is_active ? 'deactivate' : 'activate')}
                          disabled={actionLoading[user.id]}
                          className={`px-2 py-1 text-xs rounded ${
                            user.is_active 
                              ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                              : 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
                          } ${actionLoading[user.id] ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          {actionLoading[user.id] === (user.is_active ? 'deactivate' : 'activate') ? '...' : (user.is_active ? 'Deactivate' : 'Activate')}
                        </button>
                        
                        {/* Delete */}
                        <button
                          onClick={() => handleUserAction(user.id, 'delete')}
                          disabled={actionLoading[user.id]}
                          className={`px-2 py-1 text-xs rounded bg-red-100 text-red-700 hover:bg-red-200 ${
                            actionLoading[user.id] ? 'opacity-50 cursor-not-allowed' : ''
                          }`}
                        >
                          {actionLoading[user.id] === 'delete' ? '...' : 'Delete'}
                        </button>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* User Details Panel */}
        <div className="lg:col-span-1">
          <div className="bg-white shadow rounded-lg">
            {selectedUser ? (
              <div>
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    User Details
                  </h3>
                </div>
                <div className="px-4 py-5 sm:px-6">
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Username</h4>
                      <p className="mt-1 text-sm text-gray-900">{selectedUser.username}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Email</h4>
                      <p className="mt-1 text-sm text-gray-900">{selectedUser.email}</p>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Status</h4>
                      <div className="mt-1 flex space-x-2">
                        {selectedUser.is_admin && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                            Admin
                          </span>
                        )}
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          selectedUser.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {selectedUser.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Todo Statistics</h4>
                      <div className="mt-1 space-y-1">
                        <p className="text-sm text-gray-900">Total: {selectedUser.todo_count}</p>
                        <p className="text-sm text-gray-900">Completed: {selectedUser.completed_count}</p>
                        <p className="text-sm text-gray-900">Pending: {selectedUser.pending_count}</p>
                        <p className="text-sm text-gray-900">Completion Rate: {selectedUser.completion_rate}%</p>
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-500">Created</h4>
                      <p className="mt-1 text-sm text-gray-900">
                        {new Date(selectedUser.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>

                {/* User's Todos */}
                <div className="border-t border-gray-200">
                  <div className="px-4 py-5 sm:px-6">
                    <h4 className="text-sm font-medium text-gray-500 mb-3">User's Todos</h4>
                    {loadingTodos ? (
                      <div className="flex items-center justify-center py-4">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                      </div>
                    ) : userTodos.length > 0 ? (
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {userTodos.map((todo) => (
                          <div key={todo.id} className={`p-2 rounded text-xs ${
                            todo.completed ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'
                          }`}>
                            <div className="flex items-center justify-between">
                              <span className={`font-medium ${todo.completed ? 'text-green-800 line-through' : 'text-gray-800'}`}>
                                {todo.title}
                              </span>
                              <span className={`px-1.5 py-0.5 rounded text-xs ${
                                todo.completed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                              }`}>
                                {todo.completed ? '✓' : '⏳'}
                              </span>
                            </div>
                            {todo.description && (
                              <p className="mt-1 text-gray-600">{todo.description}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">No todos found</p>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="px-4 py-12 text-center">
                <div className="text-gray-400 text-4xl mb-4">👤</div>
                <p className="text-gray-500">Select a user to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserManagement;

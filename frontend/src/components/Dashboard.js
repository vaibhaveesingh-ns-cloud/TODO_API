import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CheckSquare, 
  Plus, 
  Search, 
  User, 
  LogOut,
  Trash2,
  Edit3,
  Check,
  X,
  Calendar,
  Clock,
  Flag,
  Tag,
  Moon,
  Sun,
  Bell,
  Settings,
  BarChart3,
  Target,
  TrendingUp
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { todosAPI } from '../services/api';

const Dashboard = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTodo, setNewTodo] = useState({ 
    title: '', 
    description: '', 
    priority: 'medium',
    category: 'general',
    dueDate: ''
  });
  const [showNewTodoForm, setShowNewTodoForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all'); // all, completed, pending
  const [sortBy, setSortBy] = useState('created'); // created, priority, dueDate
  const [isDarkMode, setIsDarkMode] = useState(false);
  // const [editingTodo, setEditingTodo] = useState(null);
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const priorities = [
    { value: 'low', label: 'Low', color: 'green', icon: Flag },
    { value: 'medium', label: 'Medium', color: 'yellow', icon: Flag },
    { value: 'high', label: 'High', color: 'red', icon: Flag }
  ];

  const categories = [
    { value: 'general', label: 'General', color: 'gray' },
    { value: 'work', label: 'Work', color: 'blue' },
    { value: 'personal', label: 'Personal', color: 'green' },
    { value: 'shopping', label: 'Shopping', color: 'purple' },
    { value: 'health', label: 'Health', color: 'red' }
  ];

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const data = await todosAPI.getTodos();
      setTodos(data);
    } catch (error) {
      console.error('Failed to load todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;

    try {
      const todo = await todosAPI.createTodo(newTodo);
      setTodos([todo, ...todos]);
      setNewTodo({ 
        title: '', 
        description: '', 
        priority: 'medium',
        category: 'general',
        dueDate: ''
      });
      setShowNewTodoForm(false);
    } catch (error) {
      console.error('Failed to create todo:', error);
    }
  };

  // const handleEditTodo = async (todoId, updatedData) => {
  //   try {
  //     const updatedTodo = await todosAPI.updateTodo(todoId, updatedData);
  //     setTodos(todos.map(t => t.id === todoId ? updatedTodo : t));
  //     setEditingTodo(null);
  //   } catch (error) {
  //     console.error('Failed to update todo:', error);
  //   }
  // };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle('dark');
  };

  const handleToggleTodo = async (todoId, completed) => {
    try {
      const todo = todos.find(t => t.id === todoId);
      const updatedTodo = await todosAPI.updateTodo(todoId, {
        title: todo.title,
        description: todo.description,
        completed: !completed
      });
      setTodos(todos.map(t => t.id === todoId ? updatedTodo : t));
    } catch (error) {
      console.error('Failed to update todo:', error);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    
    try {
      await todosAPI.deleteTodo(todoId);
      setTodos(todos.filter(t => t.id !== todoId));
    } catch (error) {
      console.error('Failed to delete todo:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const filteredAndSortedTodos = todos
    .filter(todo => {
      const matchesSearch = todo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           todo.description?.toLowerCase().includes(searchTerm.toLowerCase());
      
      if (filter === 'completed') return matchesSearch && todo.completed;
      if (filter === 'pending') return matchesSearch && !todo.completed;
      return matchesSearch;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return (priorityOrder[b.priority] || 2) - (priorityOrder[a.priority] || 2);
        case 'dueDate':
          if (!a.dueDate && !b.dueDate) return 0;
          if (!a.dueDate) return 1;
          if (!b.dueDate) return -1;
          return new Date(a.dueDate) - new Date(b.dueDate);
        case 'created':
        default:
          return new Date(b.created_at || b.id) - new Date(a.created_at || a.id);
      }
    });

  const stats = {
    total: todos.length,
    completed: todos.filter(t => t.completed).length,
    pending: todos.filter(t => !t.completed).length,
    highPriority: todos.filter(t => t.priority === 'high' && !t.completed).length,
    overdue: todos.filter(t => t.dueDate && new Date(t.dueDate) < new Date() && !t.completed).length
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900';
      case 'low': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900';
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900';
    }
  };

  const getCategoryColor = (category) => {
    const cat = categories.find(c => c.value === category);
    if (!cat) return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900';
    
    switch (cat.color) {
      case 'blue': return 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900';
      case 'green': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900';
      case 'purple': return 'text-purple-600 bg-purple-100 dark:text-purple-400 dark:bg-purple-900';
      case 'red': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900';
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-bounce-gentle">
            <CheckSquare className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          </div>
          <p className="text-gray-600 dark:text-gray-300 text-lg">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen gradient-bg transition-colors duration-300 ${isDarkMode ? 'dark' : ''}`}>
      {/* Header */}
      <header className="glass sticky top-0 z-50 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
        <div className="container">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary-100 dark:bg-primary-900 rounded-lg">
                  <CheckSquare className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                </div>
                <span className="text-2xl font-bold text-gray-900 dark:text-white">TaskMaster</span>
              </div>
              <nav className="hidden md:flex items-center gap-6">
                <button className="text-primary-600 dark:text-primary-400 font-medium flex items-center gap-2">
                  <BarChart3 className="h-4 w-4" />
                  Dashboard
                </button>
                <button className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center gap-2">
                  <Target className="h-4 w-4" />
                  Projects
                </button>
                <button className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center gap-2">
                  <CheckSquare className="h-4 w-4" />
                  Tasks
                </button>
                <button className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center gap-2">
                  <TrendingUp className="h-4 w-4" />
                  Analytics
                </button>
              </nav>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              >
                {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
              <button className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                <Bell className="h-5 w-5" />
              </button>
              <button className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                <Settings className="h-5 w-5" />
              </button>
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300 px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <User className="h-4 w-4" />
                <span className="font-medium">{user?.username}</span>
              </div>
              <button
                onClick={handleLogout}
                className="btn btn-secondary"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-80">
            {/* Stats Overview */}
            <div className="card mb-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary-600" />
                Overview
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Total Tasks</div>
                </div>
                <div className="text-center p-4 bg-green-50 dark:bg-green-900 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">{stats.completed}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Completed</div>
                </div>
                <div className="text-center p-4 bg-orange-50 dark:bg-orange-900 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">{stats.pending}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">Pending</div>
                </div>
                <div className="text-center p-4 bg-red-50 dark:bg-red-900 rounded-lg">
                  <div className="text-2xl font-bold text-red-600 dark:text-red-400">{stats.highPriority}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">High Priority</div>
                </div>
              </div>
              {stats.overdue > 0 && (
                <div className="mt-4 p-3 bg-red-100 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg">
                  <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm font-medium">{stats.overdue} overdue tasks</span>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="card mb-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Plus className="h-5 w-5 text-primary-600" />
                Quick Actions
              </h3>
              <button
                onClick={() => setShowNewTodoForm(true)}
                className="btn btn-primary w-full mb-3"
              >
                <Plus className="h-4 w-4" />
                New Task
              </button>
              <div className="grid grid-cols-2 gap-2">
                <button className="btn btn-outline text-sm py-2">
                  <Calendar className="h-4 w-4" />
                  Today
                </button>
                <button className="btn btn-outline text-sm py-2">
                  <Flag className="h-4 w-4" />
                  Priority
                </button>
              </div>
            </div>

            {/* Categories */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Tag className="h-5 w-5 text-primary-600" />
                Categories
              </h3>
              <div className="space-y-2">
                {categories.map((category) => {
                  const count = todos.filter(t => t.category === category.value).length;
                  return (
                    <div key={category.value} className="flex items-center justify-between p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg cursor-pointer">
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${
                          category.color === 'blue' ? 'bg-blue-500' :
                          category.color === 'green' ? 'bg-green-500' :
                          category.color === 'purple' ? 'bg-purple-500' :
                          category.color === 'red' ? 'bg-red-500' :
                          'bg-gray-500'
                        }`}></div>
                        <span className="text-sm text-gray-600 dark:text-gray-300">{category.label}</span>
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{count}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  {filteredAndSortedTodos.length} of {todos.length} tasks
                </p>
              </div>
              <button
                onClick={() => setShowNewTodoForm(true)}
                className="btn btn-primary"
              >
                <Plus className="h-4 w-4" />
                Add Task
              </button>
            </div>

            {/* Controls */}
            <div className="flex flex-col lg:flex-row gap-4 mb-8">
              <div className="flex-1 relative">
                <Search className="h-5 w-5 absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="form-input pl-12 text-lg"
                />
              </div>
              
              <div className="flex gap-3">
                <select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  className="form-input min-w-[140px]"
                >
                  <option value="all">All Tasks</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                </select>
                
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="form-input min-w-[140px]"
                >
                  <option value="created">Created Date</option>
                  <option value="priority">Priority</option>
                  <option value="dueDate">Due Date</option>
                </select>
              </div>
            </div>

            {/* New Todo Form */}
            {showNewTodoForm && (
              <div className="card mb-8 animate-slide-up">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Create New Task</h3>
                  <button
                    onClick={() => setShowNewTodoForm(false)}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
                <form onSubmit={handleCreateTodo} className="space-y-4">
                  <div className="form-group">
                    <label className="form-label">Task Title</label>
                    <input
                      type="text"
                      placeholder="What needs to be done?"
                      value={newTodo.title}
                      onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
                      className="form-input"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label className="form-label">Description</label>
                    <textarea
                      placeholder="Add more details (optional)"
                      value={newTodo.description}
                      onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
                      className="form-textarea"
                      rows={3}
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="form-group">
                      <label className="form-label">Priority</label>
                      <select
                        value={newTodo.priority}
                        onChange={(e) => setNewTodo({...newTodo, priority: e.target.value})}
                        className="form-input"
                      >
                        {priorities.map(priority => (
                          <option key={priority.value} value={priority.value}>
                            {priority.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="form-group">
                      <label className="form-label">Category</label>
                      <select
                        value={newTodo.category}
                        onChange={(e) => setNewTodo({...newTodo, category: e.target.value})}
                        className="form-input"
                      >
                        {categories.map(category => (
                          <option key={category.value} value={category.value}>
                            {category.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="form-group">
                      <label className="form-label">Due Date</label>
                      <input
                        type="date"
                        value={newTodo.dueDate}
                        onChange={(e) => setNewTodo({...newTodo, dueDate: e.target.value})}
                        className="form-input"
                      />
                    </div>
                  </div>
                  
                  <div className="flex gap-3 pt-4">
                    <button type="submit" className="btn btn-primary">
                      <Check className="h-4 w-4" />
                      Create Task
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowNewTodoForm(false)}
                      className="btn btn-secondary"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}

            {/* Tasks List */}
            <div className="space-y-4">
              {filteredAndSortedTodos.length === 0 ? (
                <div className="card text-center py-16">
                  <CheckSquare className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-6" />
                  <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">No tasks found</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-md mx-auto">
                    {searchTerm ? 'Try adjusting your search terms or filters.' : 'Create your first task to get started with TaskMaster.'}
                  </p>
                  {!searchTerm && (
                    <button
                      onClick={() => setShowNewTodoForm(true)}
                      className="btn btn-primary"
                    >
                      <Plus className="h-4 w-4" />
                      Create Your First Task
                    </button>
                  )}
                </div>
              ) : (
                filteredAndSortedTodos.map((todo, index) => {
                  const isOverdue = todo.dueDate && new Date(todo.dueDate) < new Date() && !todo.completed;
                  const priority = priorities.find(p => p.value === todo.priority);
                  const category = categories.find(c => c.value === todo.category);
                  
                  return (
                    <div 
                      key={todo.id} 
                      className={`card card-hover animate-slide-up ${
                        isOverdue ? 'border-l-4 border-l-red-500' : ''
                      }`}
                      style={{ animationDelay: `${index * 0.05}s` }}
                    >
                      <div className="flex items-start gap-4">
                        <button
                          onClick={() => handleToggleTodo(todo.id, todo.completed)}
                          className={`mt-1 w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all duration-200 ${
                            todo.completed
                              ? 'bg-green-500 border-green-500 text-white'
                              : 'border-gray-300 hover:border-green-500 hover:bg-green-50 dark:border-gray-600 dark:hover:border-green-400'
                          }`}
                        >
                          {todo.completed && <Check className="h-4 w-4" />}
                        </button>
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1 min-w-0">
                              <h3 className={`text-lg font-medium ${
                                todo.completed 
                                  ? 'text-gray-500 dark:text-gray-400 line-through' 
                                  : 'text-gray-900 dark:text-white'
                              }`}>
                                {todo.title}
                              </h3>
                              {todo.description && (
                                <p className={`text-sm mt-2 ${
                                  todo.completed 
                                    ? 'text-gray-400 dark:text-gray-500' 
                                    : 'text-gray-600 dark:text-gray-300'
                                }`}>
                                  {todo.description}
                                </p>
                              )}
                            </div>
                            
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => {/* TODO: Implement edit functionality */}}
                                className="p-2 text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900 transition-colors"
                              >
                                <Edit3 className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteTodo(todo.id)}
                                className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900 transition-colors"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          </div>
                          
                          <div className="flex items-center gap-3 mt-4">
                            <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                              todo.completed
                                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                : 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                            }`}>
                              {todo.completed ? 'Completed' : 'In Progress'}
                            </span>
                            
                            {priority && (
                              <span className={`text-xs px-3 py-1 rounded-full font-medium ${getPriorityColor(todo.priority)}`}>
                                <Flag className="h-3 w-3 inline mr-1" />
                                {priority.label}
                              </span>
                            )}
                            
                            {category && (
                              <span className={`text-xs px-3 py-1 rounded-full font-medium ${getCategoryColor(todo.category)}`}>
                                <Tag className="h-3 w-3 inline mr-1" />
                                {category.label}
                              </span>
                            )}
                            
                            {todo.dueDate && (
                              <span className={`text-xs px-3 py-1 rounded-full font-medium flex items-center gap-1 ${
                                isOverdue 
                                  ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                                  : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                              }`}>
                                <Calendar className="h-3 w-3" />
                                {new Date(todo.dueDate).toLocaleDateString()}
                                {isOverdue && <span className="text-red-600 dark:text-red-400">(Overdue)</span>}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

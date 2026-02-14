import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { systemsApi, socialApi, pagesApi } from '../services/api';

const Admin = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('systems');
  const [systems, setSystems] = useState([]);
  const [socialLinks, setSocialLinks] = useState([]);
  const [pages, setPages] = useState([]);
  const [editingItem, setEditingItem] = useState(null);
  const [loading, setLoading] = useState(true);

  const { register, handleSubmit, reset, setValue } = useForm();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
    } else {
      fetchData();
    }
  }, [navigate]);

  const fetchData = async () => {
    try {
      const [systemsRes, socialRes] = await Promise.all([
        systemsApi.getAll(),
        socialApi.getAll(),
      ]);
      setSystems(systemsRes.data);
      setSocialLinks(socialRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const onSystemSubmit = async (data) => {
    try {
      if (data.key_features) {
        data.key_features = data.key_features.split(',').map(f => f.trim());
      }
      
      if (editingItem) {
        await systemsApi.update(editingItem.id, data);
      } else {
        data.slug = data.name.toLowerCase().replace(/\s+/g, '-');
        await systemsApi.create(data);
      }
      
      fetchData();
      reset();
      setEditingItem(null);
    } catch (error) {
      console.error('Failed to save system:', error);
    }
  };

  const onSocialSubmit = async (data) => {
    try {
      if (editingItem) {
        await socialApi.update(editingItem.id, data);
      } else {
        await socialApi.create(data);
      }
      
      fetchData();
      reset();
      setEditingItem(null);
    } catch (error) {
      console.error('Failed to save social link:', error);
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    Object.keys(item).forEach(key => {
      if (key === 'key_features' && item[key]) {
        setValue(key, JSON.parse(item[key]).join(', '));
      } else {
        setValue(key, item[key]);
      }
    });
  };

  const handleDelete = async (type, id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        if (type === 'system') {
          await systemsApi.delete(id);
        } else if (type === 'social') {
          await socialApi.delete(id);
        }
        fetchData();
      } catch (error) {
        console.error('Failed to delete:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-accent"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12">
      <div className="container mx-auto px-6">
        <h1 className="text-4xl font-bold mb-8 gradient-text">Admin Dashboard</h1>

        {/* Tabs */}
        <div className="flex space-x-4 mb-8 border-b border-white/5">
          {['systems', 'social', 'pages'].map((tab) => (
            <button
              key={tab}
              onClick={() => {
                setActiveTab(tab);
                setEditingItem(null);
                reset();
              }}
              className={`px-4 py-2 font-medium capitalize transition-colors ${
                activeTab === tab
                  ? 'text-accent border-b-2 border-accent'
                  : 'text-text hover:text-text-light'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-effect rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold text-text-light mb-4">
              {editingItem ? 'Edit' : 'Add New'} {activeTab.slice(0, -1)}
            </h2>

            <form onSubmit={handleSubmit(activeTab === 'systems' ? onSystemSubmit : onSocialSubmit)}>
              {activeTab === 'systems' && (
                <>
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Name</label>
                    <input
                      {...register('name', { required: true })}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Title</label>
                    <input
                      {...register('title', { required: true })}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Description</label>
                    <textarea
                      {...register('description', { required: true })}
                      rows="4"
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Key Features (comma-separated)</label>
                    <input
                      {...register('key_features')}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                      placeholder="Feature 1, Feature 2, Feature 3"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Learn More URL</label>
                    <input
                      {...register('learn_more_url')}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Icon (emoji or URL)</label>
                    <input
                      {...register('icon')}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        {...register('is_active')}
                        className="mr-2"
                      />
                      <span className="text-text">Active</span>
                    </label>
                  </div>
                </>
              )}

              {activeTab === 'social' && (
                <>
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Platform</label>
                    <input
                      {...register('platform', { required: true })}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                      placeholder="Twitter, LinkedIn, GitHub, etc."
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">URL</label>
                    <input
                      {...register('url', { required: true })}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                      placeholder="https://..."
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="block text-text text-sm mb-2">Icon</label>
                    <input
                      {...register('icon')}
                      className="w-full px-4 py-2 bg-primary/50 border border-white/10 rounded-lg focus:border-accent focus:outline-none text-text-light"
                      placeholder="Icon name or emoji"
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        {...register('is_active')}
                        className="mr-2"
                      />
                      <span className="text-text">Active</span>
                    </label>
                  </div>
                </>
              )}

              <div className="flex space-x-4">
                <button
                  type="submit"
                  className="px-6 py-2 bg-accent text-primary font-semibold rounded-lg hover:bg-accent/90 transition-colors"
                >
                  {editingItem ? 'Update' : 'Create'}
                </button>
                
                {editingItem && (
                  <button
                    type="button"
                    onClick={() => {
                      setEditingItem(null);
                      reset();
                    }}
                    className="px-6 py-2 border border-white/10 text-text rounded-lg hover:bg-white/5 transition-colors"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
          </motion.div>

          {/* List */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-effect rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold text-text-light mb-4">
              Existing {activeTab}
            </h2>

            <div className="space-y-3">
              {activeTab === 'systems' && systems.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between p-3 bg-primary/30 rounded-lg"
                >
                  <div>
                    <h3 className="text-text-light font-medium">{item.title}</h3>
                    <p className="text-text text-sm">{item.slug}</p>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(item)}
                      className="px-3 py-1 text-sm bg-accent/20 text-accent rounded hover:bg-accent/30 transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete('system', item.id)}
                      className="px-3 py-1 text-sm bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}

              {activeTab === 'social' && socialLinks.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between p-3 bg-primary/30 rounded-lg"
                >
                  <div>
                    <h3 className="text-text-light font-medium">{item.platform}</h3>
                    <p className="text-text text-sm truncate max-w-[200px]">{item.url}</p>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(item)}
                      className="px-3 py-1 text-sm bg-accent/20 text-accent rounded hover:bg-accent/30 transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete('social', item.id)}
                      className="px-3 py-1 text-sm bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Admin;
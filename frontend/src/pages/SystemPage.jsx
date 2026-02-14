import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { systemsApi } from '../services/api';

const SystemPage = () => {
  const { slug } = useParams();
  const [system, setSystem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [features, setFeatures] = useState([]);

  useEffect(() => {
    const fetchSystem = async () => {
      try {
        const response = await systemsApi.getBySlug(slug);
        setSystem(response.data);
        if (response.data.key_features) {
          setFeatures(JSON.parse(response.data.key_features));
        }
      } catch (error) {
        console.error('Failed to fetch system:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSystem();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-accent"></div>
      </div>
    );
  }

  if (!system) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-text-light mb-4">System Not Found</h2>
          <Link to="/" className="text-accent hover:text-accent/80">
            Return to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-12">
      <div className="container mx-auto px-6">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <ol className="flex text-sm text-text">
            <li><Link to="/" className="hover:text-accent">Home</Link></li>
            <li className="mx-2">/</li>
            <li className="text-accent">{system.title}</li>
          </ol>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-effect rounded-xl p-8"
            >
              <h1 className="text-4xl font-bold mb-6 gradient-text">
                {system.title}
              </h1>
              
              <div className="prose prose-invert max-w-none">
                <p className="text-text-light text-lg mb-8">
                  {system.description}
                </p>

                <h2 className="text-2xl font-semibold text-text-light mb-4">
                  Key Features
                </h2>
                
                <ul className="space-y-3 mb-8">
                  {features.map((feature, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-start"
                    >
                      <span className="text-accent mr-3">→</span>
                      <span className="text-text">{feature}</span>
                    </motion.li>
                  ))}
                </ul>

                <a
                  href={system.learn_more_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-6 py-3 bg-accent text-primary font-semibold rounded-lg hover:bg-accent/90 transition-colors"
                >
                  Learn More
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass-effect rounded-xl p-6 sticky top-24"
            >
              <h3 className="text-xl font-semibold text-text-light mb-4">
                System Information
              </h3>
              
              <div className="space-y-4">
                <div>
                  <p className="text-text text-sm">System Name</p>
                  <p className="text-text-light font-medium">{system.name}</p>
                </div>
                
                <div>
                  <p className="text-text text-sm">Version</p>
                  <p className="text-text-light font-medium">v1.0.0</p>
                </div>
                
                <div>
                  <p className="text-text text-sm">Status</p>
                  <p className="text-green-400 font-medium">Active</p>
                </div>
                
                <div className="pt-4 border-t border-white/5">
                  <Link
                    to="/"
                    className="block w-full text-center px-4 py-2 border border-accent text-accent rounded-lg hover:bg-accent/10 transition-colors"
                  >
                    View All Systems
                  </Link>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemPage;
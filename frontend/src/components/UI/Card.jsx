import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Card = ({ system, index }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ y: -5 }}
      className="glass-effect rounded-xl overflow-hidden hover-glow"
    >
      <div className="p-6">
        {system.icon && (
          <div className="text-4xl mb-4">{system.icon}</div>
        )}
        <h3 className="text-xl font-semibold text-text-light mb-2">
          {system.title}
        </h3>
        <p className="text-text mb-4 line-clamp-3">
          {system.description}
        </p>
        <div className="flex justify-between items-center">
          <Link
            to={`/system/${system.slug}`}
            className="text-accent hover:text-accent/80 font-medium transition-colors"
          >
            Learn More →
          </Link>
          {system.key_features && (
            <span className="text-xs text-text">
              {JSON.parse(system.key_features).length} features
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default Card;
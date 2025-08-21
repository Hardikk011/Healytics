import React from 'react';
import { motion } from 'framer-motion';

const BlogDetail = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Blog Article
          </h1>
          <p className="text-gray-600">
            Detailed view of cancer awareness and educational content.
          </p>
        </motion.div>
        
        <div className="card">
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Coming Soon
            </h3>
            <p className="text-gray-600">
              This page will display detailed blog articles with full content and bookmarking functionality.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogDetail;

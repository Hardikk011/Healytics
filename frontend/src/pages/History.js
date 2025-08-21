import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const History = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access'); // Corrected key here
    if (!token) {
      console.error('No access token found — user not logged in');
      setLoading(false);
      return;
    }

    fetch('http://localhost:8000/api/predictions/list/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('Failed to fetch predictions — status ' + res.status);
        }
        return res.json();
      })
      .then(data => {
        console.log('Fetched predictions:', data);
        setPredictions(data.results ? data.results : data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching prediction history:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Prediction History
          </h1>
          <p className="text-gray-600">
            View all your previous cancer detection analyses and results.
          </p>
        </motion.div>

        {loading ? (
          <div className="text-center py-12">Loading history...</div>
        ) : predictions.length === 0 ? (
          <div className="card text-center py-12">
            <h3 className="text-lg font-medium text-gray-900 mb-2">No history yet</h3>
            <p className="text-gray-600">
              You haven’t made any predictions yet.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {predictions.map(p => (
              <motion.div
                key={p.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white shadow-md rounded-lg p-5 hover:shadow-lg transition"
              >
                {p.image && (
                  <img
                    src={p.image}
                    alt={p.predicted_cancer_type}
                    className="w-full h-48 object-cover rounded-md mb-4"
                  />
                )}
                <h2 className="text-xl font-bold mb-2 capitalize">
                  {p.predicted_cancer_type ? p.predicted_cancer_type.replace(/_/g, ' ') : 'Unknown'}
                </h2>
                <p className="text-gray-600 mb-2">
                  Confidence: {p.confidence_score}%
                </p>
                {p.symptoms && (
                  <p className="text-gray-500 mb-2">
                    Symptoms: {p.symptoms}
                  </p>
                )}
                {p.recommendations && (
                  <p className="text-gray-500 line-clamp-3">
                    {p.recommendations}
                  </p>
                )}
                <div className="text-sm text-gray-500 mt-3">
                  {p.created_at ? new Date(p.created_at).toLocaleDateString() : ''}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default History;

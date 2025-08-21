import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';
import { Upload, Image, Activity, AlertCircle, CheckCircle } from 'lucide-react';

const Prediction = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setFile(file);
      setPreview(URL.createObjectURL(file));
      setPrediction(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const handleSubmit = async () => {
    if (!file) {
      toast.error('Please select an image first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post('/api/predictions/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPrediction(response.data);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error('Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getCancerTypeColor = (type) => {
    const colors = {
      melanoma: 'text-danger-600',
      basal_cell_carcinoma: 'text-warning-600',
      squamous_cell_carcinoma: 'text-warning-600',
      benign: 'text-success-600',
      actinic_keratosis: 'text-warning-600',
      dermatofibroma: 'text-success-600',
      vascular_lesion: 'text-primary-600'
    };
    return colors[type] || 'text-gray-600';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-success-600';
    if (confidence >= 60) return 'text-warning-600';
    return 'text-danger-600';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Cancer Detection Analysis
          </h1>
          <p className="text-gray-600">
            Upload an image of a skin condition for AI-powered analysis and recommendations.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Upload Image
              </h2>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragActive
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-400'
                }`}
              >
                <input {...getInputProps()} />
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-w-full h-64 object-cover rounded-lg mx-auto"
                    />
                    <p className="text-sm text-gray-600">
                      Click to change image or drag and drop
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto" />
                    <div>
                      <p className="text-lg font-medium text-gray-900">
                        {isDragActive ? 'Drop the image here' : 'Upload an image'}
                      </p>
                      <p className="text-sm text-gray-600">
                        PNG, JPG, JPEG up to 10MB
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {file && (
                <div className="mt-4">
                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full btn-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="spinner"></div>
                        <span>Analyzing...</span>
                      </div>
                    ) : (
                      <div className="flex items-center justify-center space-x-2">
                        <Activity size={20} />
                        <span>Analyze Image</span>
                      </div>
                    )}
                  </button>
                </div>
              )}
            </div>

            {/* Instructions */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Instructions
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-success-500 mt-0.5 flex-shrink-0" />
                  <span>Ensure good lighting and clear image quality</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-success-500 mt-0.5 flex-shrink-0" />
                  <span>Focus on the area of concern</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-success-500 mt-0.5 flex-shrink-0" />
                  <span>Include surrounding skin for context</span>
                </li>
                <li className="flex items-start space-x-2">
                  <AlertCircle className="w-4 h-4 text-warning-500 mt-0.5 flex-shrink-0" />
                  <span>This is for educational purposes only. Consult a healthcare professional for medical advice.</span>
                </li>
              </ul>
            </div>
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {prediction ? (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Analysis Results
                </h2>
                
                <div className="space-y-6">
                  {/* Prediction */}
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      Predicted Condition
                    </h3>
                    <div className="flex items-center space-x-3">
                      <span className={`text-xl font-bold ${getCancerTypeColor(prediction.predicted_cancer_type)}`}>
                        {prediction.predicted_cancer_type.replace(/_/g, ' ').toUpperCase()}
                      </span>
                      <span className={`text-sm font-medium ${getConfidenceColor(prediction.confidence_score)}`}>
                        {prediction.confidence_score.toFixed(1)}% confidence
                      </span>
                    </div>
                  </div>

                  {/* Symptoms */}
                  {prediction.symptoms && (
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Common Symptoms
                      </h3>
                      <p className="text-gray-600 text-sm">
                        {prediction.symptoms}
                      </p>
                    </div>
                  )}

                  {/* Recommendations */}
                  {prediction.recommendations && (
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Recommendations
                      </h3>
                      <p className="text-gray-600 text-sm">
                        {prediction.recommendations}
                      </p>
                    </div>
                  )}

                  {/* Medicines */}
                  {prediction.medicines && prediction.medicines.length > 0 && (
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        Suggested Medicines
                      </h3>
                      <div className="space-y-3">
                        {prediction.medicines.slice(0, 3).map((medicine, index) => (
                          <div key={index} className="border border-gray-200 rounded-lg p-3">
                            <h4 className="font-medium text-gray-900">{medicine.name}</h4>
                            {medicine.generic_name && (
                              <p className="text-sm text-gray-600">Generic: {medicine.generic_name}</p>
                            )}
                            {medicine.description && (
                              <p className="text-sm text-gray-600 mt-1">
                                {medicine.description.substring(0, 100)}...
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="card">
                <div className="text-center py-12">
                  <Image className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    No Analysis Yet
                  </h3>
                  <p className="text-gray-600">
                    Upload an image and click "Analyze Image" to get started.
                  </p>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Prediction;

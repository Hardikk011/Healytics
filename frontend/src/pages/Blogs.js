import React, { useEffect, useState } from 'react'; // Removed useContext
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Blog = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAuthenticated } = useAuth(); // Removed user from destructuring
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:8000/api/blogs/') // Adjust API URL if different
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setBlogs(data); // Plain array
        } else if (data.results) {
          setBlogs(data.results); // Paginated response
        } else {
          setBlogs([]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching blogs:', err);
        setLoading(false);
        setBlogs([]);
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
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Cancer Awareness Blog</h1>
          <p className="text-gray-600">
            Educational articles about cancer prevention, treatment, and awareness.
          </p>
        </motion.div>

        {/* Show Create Blog button if user is authenticated */}
        {isAuthenticated && (
          <div className="mb-6 text-right">
            <button
              onClick={() => navigate('/blogs/create')} // Adjust route if needed
              className="inline-block px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 transition"
            >
              Create Blog
            </button>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">Loading blogs...</div>
        ) : blogs.length === 0 ? (
          <div className="card text-center py-12">
            <h3 className="text-lg font-medium text-gray-900 mb-2">No blogs available</h3>
            <p className="text-gray-600">Please check back later for educational content.</p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {blogs.map(blog => (
              <motion.div
                key={blog.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white shadow-md rounded-lg p-5 hover:shadow-lg transition"
              >
                {blog.image && (
                  <img
                    src={
                      blog.image.startsWith('http')
                        ? blog.image
                        : `http://localhost:8000${blog.image}`
                    }
                    alt={blog.title}
                    className="w-full h-48 object-cover rounded-md mb-4"
                  />
                )}
                <h2 className="text-xl font-bold mb-2">{blog.title}</h2>
                <p className="text-gray-600 mb-4 line-clamp-3">{blog.content}</p>
                <div className="text-sm text-gray-500">
                  By {blog.author?.username} • {new Date(blog.created_at).toLocaleDateString()}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Blog;

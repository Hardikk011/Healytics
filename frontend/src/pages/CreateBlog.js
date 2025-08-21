import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const CreateBlog = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isAuthenticated) {
    return <p>Please log in to create a blog.</p>;
  }

  const handleImageChange = e => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async e => {
    e.preventDefault();

    if (!title || !content) {
      setError('Title and content are required.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('content', content);
      formData.append('tags', tags);
      if (image) formData.append('image', image);

      // Adjust URL if needed
      const res = await fetch('http://localhost:8000/api/blogs/create/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Failed to create blog');
        setLoading(false);
        return;
      }

      // On success, redirect to blog list or new blog detail page
      navigate('/blogs');
    } catch (err) {
      setError('Error creating blog');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Create Blog Article</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Title *</label>
          <input
            type="text"
            className="w-full border rounded p-2"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Content *</label>
          <textarea
            className="w-full border rounded p-2 h-40"
            value={content}
            onChange={e => setContent(e.target.value)}
            required
          ></textarea>
        </div>

        <div>
          <label className="block mb-1 font-medium">Tags (comma separated)</label>
          <input
            type="text"
            className="w-full border rounded p-2"
            value={tags}
            onChange={e => setTags(e.target.value)}
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Image</label>
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
        >
          {loading ? 'Creating...' : 'Create Blog'}
        </button>
      </form>
    </div>
  );
};

export default CreateBlog;

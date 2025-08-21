# Healytics - Cancer Health Prediction System

A comprehensive cancer health prediction system with AI-powered diagnosis, chatbot support, and modern web interface.

## 🚀 Features

### Core Functionality
- **AI-Powered Cancer Detection**: Upload images for instant skin cancer prediction
- **Medicine Recommendations**: Get relevant medicine suggestions based on predictions
- **JWT Authentication**: Secure user authentication with persistent sessions
- **Health History**: Track all your predictions and medical history
- **AI Chatbot**: 24/7 cancer-related health assistance
- **Blog System**: Educational content about cancer prevention and treatment
- **Contact System**: Direct communication with healthcare providers

### Technical Features
- **Modern UI/UX**: Responsive design with animations and smooth transitions
- **Real-time Chat**: Interactive chatbot with typing animations
- **Image Processing**: Advanced image preprocessing for accurate predictions
- **API Integration**: FDA medicine database integration
- **Secure Storage**: Encrypted user data and medical information

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7**: Python web framework
- **Django REST Framework**: API development
- **JWT Authentication**: Secure token-based authentication
- **TensorFlow**: Machine learning model integration
- **OpenCV**: Image processing
- **SQLite**: Database (can be upgraded to PostgreSQL)

### Frontend
- **React 18**: Modern JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Axios**: HTTP client
- **React Router**: Client-side routing
- **React Hot Toast**: Notification system

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Your `skin_disease_model_best.h5` file

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Healytics
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Place Your Model File
```bash
# Create models directory if it doesn't exist
mkdir models
# Place your skin_disease_model_best.h5 file in the models/ directory
```

#### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### Run Django Server
```bash
python manage.py runserver
```

The Django backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Start Development Server
```bash
npm start
```

The React frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
Healytics/
├── api/                    # Django API app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # Data serializers
│   ├── utils.py           # Utility functions
│   └── urls.py            # API URLs
├── chatbot/               # Chatbot app
│   ├── models.py          # Chat models
│   ├── views.py           # Chatbot views
│   ├── chatbot_logic.py   # AI chatbot logic
│   └── urls.py            # Chatbot URLs
├── healytics/             # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URLs
│   └── wsgi.py            # WSGI configuration
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── contexts/      # React contexts
│   │   └── App.js         # Main app component
│   ├── public/            # Static files
│   └── package.json       # Frontend dependencies
├── models/                # ML model directory
│   └── skin_disease_model_best.h5  # Your model file
├── media/                 # Uploaded files
├── static/                # Static files
├── requirements.txt       # Python dependencies
└── manage.py             # Django management
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Model Configuration
Ensure your model file is placed in the `models/` directory and follows the expected format:
- Input: 224x224 RGB images
- Output: 7-class probabilities
- Format: HDF5 (.h5)

## 🚀 Usage

### 1. User Registration
- Visit `http://localhost:3000/register`
- Create a new account with your details

### 2. Cancer Prediction
- Login to your account
- Navigate to "Prediction" page
- Upload an image of suspected skin condition
- Get instant AI-powered analysis and recommendations

### 3. Chatbot Assistance
- Click the floating chat button
- Ask cancer-related questions
- Get instant AI-powered responses

### 4. Health History
- View all your previous predictions
- Track your health journey
- Access medicine recommendations

### 5. Educational Content
- Browse cancer awareness blogs
- Bookmark important articles
- Stay informed about prevention

## 🔒 Security Features

- JWT token-based authentication
- Secure password hashing
- CORS protection
- Input validation and sanitization
- File upload security
- HTTPS ready (for production)

## 🧪 Testing

### Backend Testing
```bash
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Configure environment variables

### Frontend Deployment
```bash
cd frontend
npm run build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Multi-language support
- Mobile app development
- Advanced analytics dashboard
- Integration with medical databases
- Telemedicine features
- Advanced AI models

## ⚠️ Disclaimer

This system is for educational and research purposes. Always consult with healthcare professionals for medical advice and diagnosis.

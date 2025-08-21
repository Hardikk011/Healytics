from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile, Prediction, Medicine, Blog, BlogBookmark, Contact
from .serializers import (
    UserSerializer, UserProfileSerializer, RegisterSerializer,
    PredictionSerializer, PredictionCreateSerializer, MedicineSerializer,
    BlogSerializer, BlogCreateSerializer, BlogBookmarkSerializer, ContactSerializer
)
from .utils import predict_cancer_type, get_medicine_suggestions, get_cancer_info
import os
import google.generativeai as genai

genai.configure(GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY', 'your-google-api-key'))
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        # Debug line
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, 
                          status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PredictionCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        validated_data = serializer.validated_data
        image = validated_data.get('image')

        if not image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Create prediction with only required fields that exist
        prediction = Prediction(user=request.user, image=image, predicted_cancer_type='unknown', confidence_score=0.0)
        prediction.save()  # Save first so file is written to MEDIA_ROOT

        # Step 2: Get correct path to image
        image_path = prediction.image.path

        # Step 3: Check if OpenCV can read the image
        import cv2
        img = cv2.imread(image_path)
        if img is None:
            prediction.delete()  # Remove invalid prediction
            return Response({'error': f'Cannot read uploaded image: {image_path}'}, status=400)

        # Step 4: Predict cancer type & confidence
        cancer_type, confidence = predict_cancer_type(image_path)
        if not cancer_type or confidence is None:
            prediction.delete()
            return Response({'error': 'Failed to process image or get confidence score'}, status=400)

        # Step 5: Update prediction with actual values
        prediction.predicted_cancer_type = cancer_type
        prediction.confidence_score = confidence

        # Fill optional fields safely
        cancer_info = get_cancer_info(cancer_type)
        prediction.symptoms = cancer_info.get('symptoms', '')
        prediction.recommendations = cancer_info.get('recommendations', '')

        prediction.save()  # Save updates

        # Step 6: Create associated Medicine objects
        medicines_data = get_medicine_suggestions(cancer_type) or []
        for medicine_data in medicines_data:
            Medicine.objects.create(prediction=prediction, **medicine_data)

        # Step 7: Serialize and return
        prediction_serializer = PredictionSerializer(prediction)
        return Response(prediction_serializer.data, status=201)





class PredictionListView(generics.ListAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class PredictionDetailView(generics.RetrieveAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) | 
                Q(tags__icontains=search)
            )
        
        return queryset

class BlogDetailView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.filter(is_published=True)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BlogCreateView(generics.CreateAPIView):
    serializer_class = BlogCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogBookmarkView(APIView):
    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id, is_published=True)
        
        # Check if already bookmarked
        bookmark, created = BlogBookmark.objects.get_or_create(
            user=request.user,
            blog=blog
        )
        
        if created:
            return Response({'message': 'Blog bookmarked successfully'}, 
                          status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Blog already bookmarked'}, 
                          status=status.HTTP_200_OK)
    
    def delete(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        try:
            bookmark = BlogBookmark.objects.get(user=request.user, blog=blog)
            bookmark.delete()
            return Response({'message': 'Bookmark removed successfully'}, 
                          status=status.HTTP_200_OK)
        except BlogBookmark.DoesNotExist:
            return Response({'error': 'Bookmark not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

class UserBookmarksView(generics.ListAPIView):
    serializer_class = BlogBookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BlogBookmark.objects.filter(user=self.request.user)

class ContactView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent successfully'}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------- HEALTH + STATS --------------------
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy', 'message': 'Healytics API is running'})


class StatsView(APIView):
    authentication_classes = [] 
    permission_classes = [permissions.AllowAny]  # Allow both guests & logged-in users

    def get(self, request):
        user = request.user if request.user.is_authenticated else None

        # Global stats (always returned)
        global_stats = {
            "total_users": User.objects.count(),
            "total_blogs": Blog.objects.filter(is_published=True).count(),
            "total_predictions": Prediction.objects.count(),
            "total_contacts": Contact.objects.count(),
        }

        # User-specific stats (only if logged in)
        if user:
            user_stats = {
                "total_predictions": Prediction.objects.filter(user=user).count(),
                "total_bookmarks": BlogBookmark.objects.filter(user=user).count(),
                "recent_predictions": list(
                    Prediction.objects.filter(user=user)
                    .order_by('-created_at')
                    .values('id', 'predicted_cancer_type', 'confidence_score', 'created_at')[:5]
                )
            }
        else:
            user_stats = None  # or {} if you want empty dict

        return Response({
            "user_stats": user_stats,
            "global_stats": global_stats
        })

class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'No message provided.'}, status=400)

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_message)
            ai_reply = response.text
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        return Response({'reply': ai_reply})


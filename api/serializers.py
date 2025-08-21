from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import UserProfile, Prediction, Medicine, Blog, BlogBookmark, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check for existing username or email
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create UserProfile with default values if needed
        UserProfile.objects.create(user=user)
        
        return user

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    medicines = MedicineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Prediction
        fields = '__all__'

class PredictionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['image']

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BlogBookmark.objects.filter(user=request.user, blog=obj).exists()
        return False

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'tags']

class BlogBookmarkSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only=True)
    
    class Meta:
        model = BlogBookmark
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
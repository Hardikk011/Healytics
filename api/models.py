from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Prediction(models.Model):
    CANCER_TYPES = [
        ('melanoma', 'Melanoma'),
        ('basal_cell_carcinoma', 'Basal Cell Carcinoma'),
        ('squamous_cell_carcinoma', 'Squamous Cell Carcinoma'),
        ('benign', 'Benign'),
        ('actinic_keratosis', 'Actinic Keratosis'),
        ('dermatofibroma', 'Dermatofibroma'),
        ('vascular_lesion', 'Vascular Lesion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    image = models.ImageField(upload_to='predictions/')
    predicted_cancer_type = models.CharField(max_length=50, choices=CANCER_TYPES)
    confidence_score = models.FloatField()
    symptoms = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.predicted_cancer_type} ({self.confidence_score:.2f}%)"

class Medicine(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    dosage_form = models.CharField(max_length=100, blank=True, null=True)
    strength = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class BlogBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'blog']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.blog.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

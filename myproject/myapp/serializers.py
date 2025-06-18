from rest_framework import serializers
from .models import Book, BookImage
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BookImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = BookImage
        fields = ['id', 'image']

class BookSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    uploaded_images = BookImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'published_at', 'images', 'uploaded_images', 'author']

    def create(self, validated_data):
        image_files = validated_data.pop('images', [])
        book = Book.objects.create(**validated_data)
        for image in image_files:
            BookImage.objects.create(book=book, image=image)
        return book

    def update(self, instance, validated_data):
        image_files = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if image_files is not None:
            # Delete existing images and add new ones
            instance.images.all().delete()
            for image in image_files:
                BookImage.objects.create(book=instance, image=image)
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, valided_data):
        user = User.objects.create_user(
            username = valided_data['username'],
            email = valided_data['email'],
            password = valided_data['password']
        )
        return user
    
    def validate_password(self, value):
        if value.lower() in ['password', '12345678']:
            raise ValidationError("Password is too common.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user woth this email already exists.")
        return value
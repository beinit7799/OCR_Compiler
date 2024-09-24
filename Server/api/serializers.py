from rest_framework import serializers  
from .models import *
from .services.code_formatter import format_code
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['id','formatted_code', 'language', 'created_at', 'user', 'guest']

class OCRProcessSerializer(serializers.ModelSerializer):
    snippet = CodeSnippetSerializer(read_only=True)
    original_image = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True ,allow_null=True)
    guest = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), write_only=True, allow_null=True)
    class Meta:
        model = OCRProcess
        fields = ['id', 'snippet', 'original_image', 'ocr_text', 'created_at', 'user', 'guest']

    def create(self, validated_data):
        original_image_path = validated_data.pop('original_image')
        ocr_text = validated_data.pop('ocr_text')
        user = validated_data.pop('user', None)
        guest = validated_data.pop('guest', None)

        formatted_code, language = format_code(ocr_text)

        if not formatted_code:
            formatted_code = ocr_text
        
        try:
            with transaction.atomic():
                snippet = CodeSnippet.objects.create(
                    formatted_code=formatted_code,
                    language=language,
                    user=user,
                    guest=guest
                )
                ocr_process = OCRProcess.objects.create(
                    snippet=snippet,
                    original_image=original_image_path,
                    ocr_text=ocr_text
                )
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return ocr_process

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'email', 'created_at','name','username','snippets')
    
    def get_snippets(self, obj):
        snippets = CodeSnippet.objects.filter(user=obj)
        serializer = CodeSnippetSerializer(snippets, many=True)
        return serializer.data
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    class Meta:
        model = User
        fields = ["email", "password"]

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'username')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email is already in use'})

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

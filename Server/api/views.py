from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from werkzeug.utils import secure_filename
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .services.methods import allowed_file
from .services.ocr import run_ocr
from django.http import HttpResponse
from .services.compiler import compile_code
from .permissions import IsSnippetOwner


UPLOAD_FOLDER = "Images"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email= serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({'tokens':tokens,'msg':'Login Successful'}, status.HTTP_200_OK)
        return Response({'errors':{'non_field_errors':['Email of password is not valid']}}, status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'msg': 'User registration success'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_image(request):
    if 'image' not in request.data:
        return Response({'msg': 'No image in the request'}, status=status.HTTP_400_BAD_REQUEST)

    image = request.data['image']
    
    if image.name == '':
        return Response({'msg': 'No selected file'}, status=status.HTTP_400_BAD_REQUEST)
    
    if image and allowed_file(image.name):
        filename = secure_filename(image.name)
        file_path = os.path.join(settings.MEDIA_ROOT,'uploads', filename)
        path = default_storage.save(file_path, ContentFile(image.read()))
        
        ocr_text = run_ocr(path)
        data = {
            'original_image': path,
            'ocr_text': ocr_text
        }
        
        if request.user.is_authenticated:
            user = request.user
            data['user'] = user.id
            data['guest'] = None
        else:
            if not request.session.session_key:
                request.session.create()
            guest, created = Guest.objects.get_or_create(session_id=request.session.session_key)
            data['guest'] = guest.id
            data['user'] = None

        serializer = OCRProcessSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'msg': 'Image upload failed. Invalid file format.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_snippet(request, snippet_id):
    snippet = CodeSnippet.objects.get(id=snippet_id, user=request.user)
    file_extension = {
        'python': 'py',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c'
    }.get(snippet.language, 'txt')
    
    response = HttpResponse(snippet.formatted_code, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=snippet_{snippet.id}.{file_extension}'
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def compiler_service(request):
    output = compile_code(request)
    return output

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsSnippetOwner])
def delete_code_snippet(request, pk):
    try:
        snippet = CodeSnippet.objects.get(pk=pk)
    except CodeSnippet.DoesNotExist:
        return Response({'msg': 'Code snippet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    permission = IsSnippetOwner()
    if not permission.has_object_permission(request, None, snippet):
        return Response({'msg': 'You do not have permission to delete this snippet'}, status=status.HTTP_403_FORBIDDEN)
    
    snippet.delete()
    return Response({'msg':'Successfully deleted '},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'msg': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'msg': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
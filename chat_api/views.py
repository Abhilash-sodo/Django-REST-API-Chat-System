from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Chat
from .serializers import UserSerializer, UserDetailSerializer, ChatSerializer
import uuid

@api_view(['POST'])
def register(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create(
            username=username,
            password=make_password(password),
            tokens=4000
        )
        
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not check_password(password, user.password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate new token
        user.auth_token = uuid.uuid4()
        user.save()
        
        return Response({
            'token': user.auth_token,
            'user_id': user.id
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def chat(request):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return Response(
                {'error': 'Authorization token required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.tokens < 100:
            return Response(
                {'error': 'Insufficient tokens'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message = request.data.get('message')
        # Dummy AI response for demonstration
        ai_response = f"This is a dummy response to: {message}"
        
        # Create chat entry
        chat = Chat.objects.create(
            user=user,
            message=message,
            response=ai_response
        )
        
        # Deduct tokens
        user.tokens -= 100
        user.save()
        
        return Response({
            'response': ai_response,
            'tokens_remaining': user.tokens
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def token_balance(request):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return Response(
                {'error': 'Authorization token required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response({
            'username': user.username,
            'tokens_remaining': user.tokens
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
# Bonus - User Detail API
@api_view(['GET'])
def get_all_users(request):
    """
    Get list of all users (admin endpoint)
    """
    try:
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# @api_view(['GET'])
# def get_user_detail(request, user_id):
#     """
#     Get details of a specific user
#     """
#     try:
#         token = request.headers.get('Authorization')
#         if not token:
#             return Response(
#                 {'error': 'Authorization token required'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         # Verify the requesting user
#         try:
#             requesting_user = User.objects.get(auth_token=token)
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'Invalid token'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         # Get the requested user
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'User not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Only allow users to view their own details
#         if requesting_user.id != user.id:
#             return Response(
#                 {'error': 'Unauthorized to view this user\'s details'},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         serializer = UserDetailSerializer(user)
#         return Response(serializer.data)
    
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

# @api_view(['GET'])
# def get_user_chat_history(request, user_id):
#     """
#     Get chat history of a specific user
#     """
#     try:
#         token = request.headers.get('Authorization')
#         if not token:
#             return Response(
#                 {'error': 'Authorization token required'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         # Verify the requesting user
#         try:
#             requesting_user = User.objects.get(auth_token=token)
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'Invalid token'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         # Get the requested user
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'User not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Only allow users to view their own chat history
#         if requesting_user.id != user.id:
#             return Response(
#                 {'error': 'Unauthorized to view this user\'s chat history'},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         chats = Chat.objects.filter(user=user).order_by('-timestamp')
#         serializer = ChatSerializer(chats, many=True)
#         return Response(serializer.data)
    
#     except Exception as e:
#         return Response(
#             {'error': str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )
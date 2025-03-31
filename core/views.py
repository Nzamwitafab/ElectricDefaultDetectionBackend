# core/views.py
import logging
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from core.services.profile_service import ProfileService
from core.services.user_service import delete_user, get_all_users, get_user_by_id, register_user, update_user
from core.serializers import UserRegisterSerializer,UserLoginSerializer,UserSerializer,UserUpdateSerializer
from core.services.user_service import login_user
from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from core.services.user_service import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated # type: ignore

logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def register_user_view(request):
    logger.info("Received user registration request.")

    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                result = register_user(serializer.validated_data)
                logger.info(f"User registered: {serializer.validated_data['email']}")
                return Response({"message": result["message"]}, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                logger.warning(f"Validation error during registration: {str(e)}")
                
                # Extracting the first error detail (it may have multiple errors)
                error_messages = e.detail if isinstance(e.detail, list) else [e.detail]
                formatted_error_message = str(error_messages[0])  # Get the first message in the list
                
                return Response({"error": formatted_error_message}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
                return Response({"error": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning("Invalid registration data received.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_user_view(request):
    permission_classes = []  # Empty list means no permissions required
    
    print("\n==== LOGIN VIEW REACHED ====")
    print(f"Request headers: {request.headers}")
    print("\n==== LOGIN VIEW REACHED ====")
    print(f"Request data: {request.data}")  # Debug input
    
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        print("Data validated successfully")
        print("==== CREDENTIALS VALIDATED ====")  # Debug 5
        
        try:
            tokens = login_user(serializer.validated_data)
            
            if tokens:
                print("==== TOKENS GENERATED SUCCESSFULLY ====")  # Debug 6
                return Response({
                    'access': tokens['access'],
                    'refresh': tokens['refresh']
                }, status=status.HTTP_200_OK)
            else:
                print("==== INVALID CREDENTIALS ====")  # Debug 7
                return Response(
                    {"detail": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Exception as e:
            print(f"!!!! LOGIN ERROR: {str(e)}")  # Debug 8
            return Response(
                {"detail": "Login processing error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # This return should theoretically never be reached for POST-only @api_view
    return Response(
        {"detail": "Method not allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id_view(request, user_id):  # Ensure 'user_id' is used here
    print("==== GET USER BY ID ====")
    user = get_user_by_id(user_id)
    if user:
        serializer = UserSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_users_view(request):
    print("==== GET ALL USERS ====")
    users = get_all_users()
    if users:
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
    return Response({"detail": "No users found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT','GET','POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_view(request, user_id):
    print("==== UPDATE USER ====")
    user = get_user_by_id(user_id)
    if user:
        updated_user = update_user(user.id, request.data)
        return Response({"user": UserSerializer(updated_user).data}, status=status.HTTP_200_OK)
    return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE','GET','POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_view(request,user_id):
    print("==== DELETE USER ====")
    user = get_user_by_id(user_id)
    if user:
        delete_user(user.id)
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_profile_view(request, user_id):
    logger.info(f"Request received for retrieving profile of user with ID: {user_id}")
    
    profile = ProfileService.get_profile(user_id)
    if profile:
        return Response({"profile": profile}, status=status.HTTP_200_OK)
    
    return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PATCH'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_view(request, user_id):
    logger.info(f"Request received for updating profile of user with ID: {user_id}")
    
    updated_profile = ProfileService.update_profile(user_id, request.data)
    
    if isinstance(updated_profile, dict) and "error" in updated_profile:
        # Handle the case where an error is returned from the service layer
        return Response(updated_profile, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_profile_view(request, user_id):
    logger.info(f"Request received for deleting profile of user with ID: {user_id}")
    
    success = ProfileService.delete_profile(user_id)
    if success:
        return Response({"message": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    return Response({"error": "Profile deletion failed."}, status=status.HTTP_400_BAD_REQUEST)

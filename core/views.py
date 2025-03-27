# core/views.py
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from core.services.user_service import delete_user, get_all_users, get_user_by_id, register_user, update_user
from core.serializers import UserRegisterSerializer,UserLoginSerializer,UserSerializer,UserUpdateSerializer
from core.services.user_service import login_user
from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from core.services.user_service import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated # type: ignore

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])  # Requires valid JWT
@permission_classes([IsAuthenticated])    # Custom permission
def register_user_view(request):
    if request.method == 'POST':
        # Validate incoming data with a serializer
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Pass the validated data to the service layer
            user = register_user(serializer.validated_data)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
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
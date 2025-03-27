# core/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.services.user_service import register_user
from core.serializers import UserRegisterSerializer,UserLoginSerializer
from core.services.user_service import login_user
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from core.services.user_service import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated

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
def test_view(request):
    print("==== TEST VIEW HIT ====")
    return Response({"status": "ok"})
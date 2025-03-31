from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from project.services.problem_service import ProblemService
from core.services.user_service import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from project.serializers import ProblemSerializer  # Import the serializer
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_problem_view(request, problem_id):
    logger.info(f"Request received for retrieving problem with ID: {problem_id}")
    
    problem = ProblemService.get_problem(problem_id)
    if problem:
        # Use serializer to format the problem object
        serializer = ProblemSerializer(problem)
        return Response({"problem": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"error": "Problem not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_problem_view(request):
    logger.info(f"Request received for creating problem by user with ID: {request.user.id}")
    
    problem_data = request.data
    problem = ProblemService.create_problem(request.user, problem_data)
    
    if isinstance(problem, dict) and "error" in problem:
        return Response(problem, status=status.HTTP_400_BAD_REQUEST)
    
    # After creating, serialize and return the problem data
    serializer = ProblemSerializer(problem)
    return Response({"problem": serializer.data, "message": "Problem created successfully."}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_problem_view(request, problem_id):
    logger.info(f"Request received for updating problem with ID: {problem_id}")
    
    updated_problem = ProblemService.update_problem(problem_id, request.data)
    
    if isinstance(updated_problem, dict) and "error" in updated_problem:
        return Response(updated_problem, status=status.HTTP_400_BAD_REQUEST)
    
    # After updating, serialize and return the updated problem data
    serializer = ProblemSerializer(updated_problem)
    return Response({"problem": serializer.data, "message": "Problem updated successfully."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_problem_view(request, problem_id):
    logger.info(f"Request received for deleting problem with ID: {problem_id}")
    
    try:
        success = ProblemService.delete_problem(problem_id)
        if success:
            return Response({"message": "Problem deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    except ValidationError as e:
        # Extract and join the error messages into a single string if they are in a list
        error_messages = ' '.join(e.detail) if isinstance(e.detail, list) else str(e.detail)
        logger.error(f"Validation error occurred: {error_messages}")
        return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_problems_view(request):
    logger.info("Request received for retrieving all problems.")
    
    problems = ProblemService.get_all_problems()
    if problems:
        # Use serializer to format the problem list
        serializer = ProblemSerializer(problems, many=True)
        return Response({"problems": serializer.data}, status=status.HTTP_200_OK)
    
    return Response({"error": "No problems found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from core.models import Grid
from project.services.grid_service import GridService
from core.services.user_service import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated # type: ignore
from project.serializers import GridSerializer
from rest_framework.exceptions import ValidationError # type: ignore
import logging

logger = logging.getLogger(__name__)

# Custom function to simplify the error format
def format_error(error):
    if isinstance(error, ValidationError):
        # Extract the error message from ValidationError
        return error.detail[0] if isinstance(error.detail, list) else str(error.detail)
    return str(error)  # Default to string conversion if it's not a ValidationError

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_grid_view(request, grid_id):
    logger.info(f"Request received for retrieving grid with ID: {grid_id}")
    
    try:
        grid = GridService.get_grid_by_id(grid_id)
        if not grid:
            logger.error(f"Grid with ID {grid_id} not found.")
            return Response({"error": f"Grid with ID {grid_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Use serializer to format the grid object
        serializer = GridSerializer(grid)
        return Response({"grid": serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Unexpected error while retrieving grid with ID {grid_id}: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_grid_view(request):
    logger.info(f"Request received for creating grid by user with ID: {request.user.id}")
    
    grid_data = request.data
    try:
        grid = GridService.create_grid(grid_data)
        # After creating, serialize and return the grid data
        serializer = GridSerializer(grid)
        return Response({"grid": serializer.data, "message": "Grid created successfully."}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Validation error while creating grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Unexpected error occurred while creating grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_grid_view(request, grid_id):
    logger.info(f"Request received for updating grid with ID: {grid_id}")
    
    try:
        updated_grid = GridService.update_grid(grid_id, request.data)
        if not updated_grid:
            logger.error(f"Grid with ID {grid_id} not found for update.")
            return Response({"error": f"Grid with ID {grid_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # After updating, serialize and return the updated grid data
        serializer = GridSerializer(updated_grid)
        return Response({"grid": serializer.data, "message": "Grid updated successfully."}, status=status.HTTP_200_OK)
    except ValidationError as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Validation error while updating grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Unexpected error occurred while updating grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_grid_view(request, grid_id):
    logger.info(f"Request received for deleting grid with ID: {grid_id}")
    
    try:
        success = GridService.delete_grid(grid_id)
        if success:
            return Response({"message": "Grid deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        logger.error(f"Grid with ID {grid_id} not found for deletion.")
        return Response({"error": f"Grid with ID {grid_id} not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except ValidationError as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Validation error while deleting grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Unexpected error occurred while deleting grid: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_grids_view(request):
    logger.info("Request received for retrieving all grids.")
    
    try:
        grids = Grid.objects.all()
        if not grids:
            logger.warning("No grids found.")
            return Response({"error": "No grids found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GridSerializer(grids, many=True)
        return Response({"grids": serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        error_message = format_error(e)  # Format the error message
        logger.error(f"Unexpected error while retrieving grids: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

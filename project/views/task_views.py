# views.py
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from project.services.task_service import TaskService
from project.serializers import TaskSerializer
from rest_framework.exceptions import ValidationError # type: ignore

@api_view(['GET'])
def get_task(request, task_id):
    task = TaskService.get_task_by_id(task_id)
    if task:
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    raise ValidationError(f"Task with ID {task_id} not found.")

@api_view(['GET'])
def get_all_tasks(request):
    tasks = TaskService.get_all_tasks()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = TaskService.create_task(serializer.validated_data)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_task(request, task_id):
    task = TaskService.update_task(task_id, request.data)
    if task:
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
    raise ValidationError(f"Task with ID {task_id} not found.")

@api_view(['DELETE'])
def delete_task(request, task_id):
    success = TaskService.delete_task(task_id)
    if success:
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    raise ValidationError(f"Task with ID {task_id} not found.")

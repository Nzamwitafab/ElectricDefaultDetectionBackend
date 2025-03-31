from rest_framework import serializers # type: ignore
from core.models import Grid, Problem, Task, User

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'  # You can specify individual fields if needed, e.g., ['id', 'user', 'location', 'description']

class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid
        fields = '__all__'  # You can specify individual fields if needed, e.g., ['id', 'total_clients', 'total_networks', 'energy_allocated', 'status']

from core.serializers import UserSerializer  # Assuming User model has a serializer
from project.serializers import ProblemSerializer  # Assuming Problem model has a serializer
from project.serializers import GridSerializer  # Assuming Grid model has a serializer

class TaskSerializer(serializers.ModelSerializer):
    technician_assigned = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.filter(role='Technician')
    )
    problem = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.all()
    )
    grid = serializers.PrimaryKeyRelatedField(
        queryset=Grid.objects.all()
    )

    class Meta:
        model = Task
        fields = '__all__'

    def update(self, instance, validated_data):
        # The serializer will automatically handle ID to instance conversion
        return super().update(instance, validated_data)
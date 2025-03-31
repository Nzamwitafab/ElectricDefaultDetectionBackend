# repositories.py
from core.models import Task

class TaskRepository:
    
    @staticmethod
    def get_task_by_id(task_id):
        return Task.objects.filter(id=task_id).first()
    
    @staticmethod
    def get_all_tasks():
        return Task.objects.all()

    @staticmethod
    def create_task(data):
        task = Task.objects.create(**data)
        return task

    @staticmethod
    def update_task(task, data):
        task.title = data.get('title', task.title)
        task.date = data.get('date', task.date)
        task.time = data.get('time', task.time)
        task.status = data.get('status', task.status)
        task.technician_assigned = data.get('technician_assigned', task.technician_assigned)
        task.ai_predicted_fault = data.get('ai_predicted_fault', task.ai_predicted_fault)
        task.problem = data.get('problem', task.problem)
        task.grid = data.get('grid', task.grid)
        task.save()
        return task

    @staticmethod
    def delete_task(task):
        task.delete()

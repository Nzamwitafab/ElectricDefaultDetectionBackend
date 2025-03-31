# services.py
from project.repositories.task_repository import TaskRepository

class TaskService:

    @staticmethod
    def get_task_by_id(task_id):
        return TaskRepository.get_task_by_id(task_id)

    @staticmethod
    def get_all_tasks():
        return TaskRepository.get_all_tasks()

    @staticmethod
    def create_task(data):
        return TaskRepository.create_task(data)

    @staticmethod
    def update_task(task_id, data):
        task = TaskRepository.get_task_by_id(task_id)
        if task:
            return TaskRepository.update_task(task, data)
        return None

    @staticmethod
    def delete_task(task_id):
        task = TaskRepository.get_task_by_id(task_id)
        if task:
            TaskRepository.delete_task(task)
            return True
        return False

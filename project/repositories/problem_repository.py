# core/repositories/problem_repository.py

from core.models import Problem

class ProblemRepository:
    @staticmethod
    def create_problem(user, problem_data):
        problem, created = Problem.objects.get_or_create(user=user, **problem_data)
        return problem

    @staticmethod
    def get_problem_by_id(problem_id):
        try:
            return Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return None

    @staticmethod
    def get_all_problems():
        return Problem.objects.all()

    @staticmethod
    def update_problem(problem_id, data):
        problem = ProblemRepository.get_problem_by_id(problem_id)
        if problem:
            for field, value in data.items():
                setattr(problem, field, value)
            problem.save()
            return problem
        return None

    @staticmethod
    def delete_problem(problem_id):
        problem = ProblemRepository.get_problem_by_id(problem_id)
        if problem:
            problem.delete()
            return True
        return False

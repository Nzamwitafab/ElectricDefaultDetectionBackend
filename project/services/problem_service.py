# core/services/problem_service.py

from project.repositories.problem_repository import ProblemRepository
import logging
from rest_framework.exceptions import ValidationError
logger = logging.getLogger(__name__)

class ProblemService:
    @staticmethod
    def get_problem(problem_id):
        logger.info(f"Retrieving problem with ID: {problem_id}")
        problem = ProblemRepository.get_problem_by_id(problem_id)
        if problem:
            logger.info(f"Problem found with ID: {problem_id}")
            return problem
        logger.warning(f"Problem with ID {problem_id} not found.")
        return None

    @staticmethod
    def create_problem(user, problem_data):
        logger.info(f"Creating problem for user with ID: {user.id}")
        problem = ProblemRepository.create_problem(user, problem_data)
        if problem:
            logger.info(f"Problem created for user with ID: {user.id}")
            return problem
        logger.warning(f"Problem creation failed for user with ID: {user.id}")
        return {"error": "Problem creation failed."}

    @staticmethod
    def update_problem(problem_id, data):
        logger.info(f"Updating problem with ID: {problem_id}")
        problem = ProblemRepository.update_problem(problem_id, data)
        if problem:
            logger.info(f"Problem updated for problem ID: {problem_id}")
            return problem
        logger.warning(f"Problem with ID {problem_id} not found for update.")
        return {"error": f"Problem with ID {problem_id} not found."}

    @staticmethod
    def delete_problem(problem_id):
        logger.info(f"Attempting to delete problem with ID: {problem_id}")
        
        # Try to delete the problem from the repository
        problem = ProblemRepository.get_problem_by_id(problem_id)
        
        if not problem:
            logger.warning(f"Problem with ID {problem_id} not found for deletion.")
            # Directly raise ValidationError with a clean message
            raise ValidationError(f"Problem with ID {problem_id} not found for deletion.")
        
        # If problem exists, proceed to delete
        success = ProblemRepository.delete_problem(problem_id)
        
        if success:
            logger.info(f"Problem deleted with ID: {problem_id}")
            return True
        
        # In case deletion fails
        logger.warning(f"Problem with ID {problem_id} could not be deleted.")
        # Directly raise ValidationError with a clean message
        raise ValidationError(f"Problem with ID {problem_id} could not be deleted.")
    
    @staticmethod
    def get_all_problems():
        logger.info("Retrieving all problems")
        problems = ProblemRepository.get_all_problems()
        if problems:
            logger.info(f"{len(problems)} problems found.")
            return problems
        logger.warning("No problems found.")
        return []
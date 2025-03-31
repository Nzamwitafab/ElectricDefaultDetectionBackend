import logging
from rest_framework.exceptions import ValidationError # type: ignore
from core.models import Grid

# Logger setup
logger = logging.getLogger(__name__)

class GridService:

    @staticmethod
    def create_grid(data):
        try:
            logger.info("Attempting to create a new grid.")
            grid = Grid.objects.create(
                total_clients=data.get('total_clients'),
                total_networks=data.get('total_networks'),
                energy_allocated=data.get('energy_allocated'),
                status=data.get('status')
            )
            logger.info(f"Grid created successfully with ID: {grid.id}")
            return grid
        except Exception as e:
            logger.error(f"Error creating grid: {e}")
            raise ValidationError(f"Failed to create grid: {e}")

    @staticmethod
    def get_grid_by_id(grid_id):
        try:
            logger.info(f"Attempting to retrieve grid with ID: {grid_id}")
            grid = Grid.objects.get(id=grid_id)
            logger.info(f"Grid with ID: {grid_id} retrieved successfully.")
            return grid
        except Grid.DoesNotExist:
            logger.warning(f"Grid with ID: {grid_id} not found.")
            raise ValidationError(f"Grid with ID {grid_id} not found.")
        except Exception as e:
            logger.error(f"Error retrieving grid: {e}")
            raise ValidationError(f"Failed to retrieve grid: {e}")

    @staticmethod
    def update_grid(grid_id, data):
        try:
            logger.info(f"Attempting to update grid with ID: {grid_id}")
            grid = Grid.objects.get(id=grid_id)
            grid.total_clients = data.get('total_clients', grid.total_clients)
            grid.total_networks = data.get('total_networks', grid.total_networks)
            grid.energy_allocated = data.get('energy_allocated', grid.energy_allocated)
            grid.status = data.get('status', grid.status)
            grid.save()
            logger.info(f"Grid with ID: {grid_id} updated successfully.")
            return grid
        except Grid.DoesNotExist:
            logger.warning(f"Grid with ID: {grid_id} not found.")
            raise ValidationError(f"Grid with ID {grid_id} not found.")
        except Exception as e:
            logger.error(f"Error updating grid: {e}")
            raise ValidationError(f"Failed to update grid: {e}")

    @staticmethod
    def delete_grid(grid_id):
        try:
            logger.info(f"Attempting to delete grid with ID: {grid_id}")
            grid = Grid.objects.get(id=grid_id)
            grid.delete()
            logger.info(f"Grid with ID: {grid_id} deleted successfully.")
            return True
        except Grid.DoesNotExist:
            logger.warning(f"Grid with ID: {grid_id} not found.")
            raise ValidationError(f"Grid with ID {grid_id} not found.")
        except Exception as e:
            logger.error(f"Error deleting grid: {e}")
            raise ValidationError(f"Failed to delete grid: {e}")

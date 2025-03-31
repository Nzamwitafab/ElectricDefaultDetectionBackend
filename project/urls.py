# project/urls.py
from django.urls import path # type: ignore
from project.views import problem_views
from project.views.grid_views import create_grid_view, delete_grid_view, get_all_grids_view, get_grid_view, update_grid_view
from project.views.task_views import create_task, delete_task, get_all_tasks, get_task, update_task

urlpatterns = [
    path('problems/create/', problem_views.create_problem_view, name='create_problem'),
    path('problems/', problem_views.get_all_problems_view, name='get_all_problems'), 
    path('problems/<int:problem_id>/', problem_views.get_problem_view, name='get_problem'),
    path('problems/<int:problem_id>/update/', problem_views.update_problem_view, name='update_problem'),
    path('problems/<int:problem_id>/delete/', problem_views.delete_problem_view, name='delete_problem'),
        path('grids/', get_all_grids_view, name='get_all_grids'),
    path('grids/create/', create_grid_view, name='create_grid'),
    path('grids/<int:grid_id>/', get_grid_view, name='get_grid'),
    path('grids/<int:grid_id>/update/', update_grid_view, name='update_grid'),
    path('grids/<int:grid_id>/delete/', delete_grid_view, name='delete_grid'),
        path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<int:task_id>/', get_task, name='get_task'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]

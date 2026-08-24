from django.urls import path, include

from . import views

urlpatterns=[
    path("", views.project_list, name="project-list"),
    path("create/", views.project_create, name="project-create"),
    path("<int:project_id>/", views.project_detail, name="project-detail"),
    path("<int:project_id>/tasks/", include("tasks.urls")),
    path("<int:project_id>/members/", views.project_members, name="project-members"),
    path("<int:project_id>/members/<int:user_id>/", views.project_members_delete, name="project-members-delete"),
    path("project-list/", views.render_project_list, name="render-project-list"),
    path("<int:project_id>/project-detail/", views.render_project_detail, name="render-project-detail"),
]
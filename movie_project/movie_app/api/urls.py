from django.urls import path
from rest_framework.routers import SimpleRouter
from .viewsets import ViewSets

router = SimpleRouter()
router.register('movies', ViewSets)
# urlpatterns = [
#
#     path('movies/<int:pk>/',
#          ViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}),
#          name='first'),
#     path('movies/', ViewSets.as_view({'get': 'list', 'post': 'create'}), name='second'),
# ]

urlpatterns = router.urls


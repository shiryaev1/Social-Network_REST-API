from api.viewsetc import PostViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('posts', PostViewSet, base_name='post')
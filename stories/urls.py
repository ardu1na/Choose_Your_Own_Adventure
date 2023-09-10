from rest_framework.routers import DefaultRouter

from stories.views import StoryViewSet, \
    SavedViewSet, LikeViewSet
    
    
router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'saved', SavedViewSet, basename="saved")
router.register(r'likes', LikeViewSet, basename="like")

urlpatterns = router.urls
from rest_framework.routers import DefaultRouter

from stories.views import StoryViewSet, \
    SavedViewSet, LikeViewSet, TextViewSet, ChoiceViewSet    
    
router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'saved', SavedViewSet, basename="saved")
router.register(r'likes', LikeViewSet, basename="like")
router.register(r'texts', TextViewSet, basename="texts")
router.register(r'choices', ChoiceViewSet, basename="choices")

urlpatterns = router.urls
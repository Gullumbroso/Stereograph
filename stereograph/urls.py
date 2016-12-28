from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from algorithm import views

router = routers.DefaultRouter()
router.register(r'characteristics', views.CharacteristicViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'edges', views.EdgeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^shortest_path/$', views.ShortestPath.as_view())
]
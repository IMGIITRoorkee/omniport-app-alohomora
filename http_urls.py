from django.urls import path

from alohomora.views.cast import CastAlohomoraView

app_name = 'alohomora'

urlpatterns = [
    path('', CastAlohomoraView.as_view(), name='cast')
]

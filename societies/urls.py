from django.urls import path
from societies.views import (
    SocietyCreateView,
    PartnerCreateView,
    AdministratorCreateView,
    SocietyRetrieveDeleteView,
    SocietyByPartnerView,
    PartnersAdministratorsBySocietyView
)


urlpatterns = [
    path('societies/', SocietyCreateView.as_view(), name='create-society'),
    path('partners/', PartnerCreateView.as_view(), name='create-partner'),
    path('administrators/', AdministratorCreateView.as_view(), name='create-administrator'),
    path('societies/delete/<str:rut>/', SocietyRetrieveDeleteView.as_view(), name='society-delete'),
    path('societies/partner/<str:rut>/', SocietyByPartnerView.as_view(), name='society-by-partner'),
    path('societies/partners-administrators/<str:rut>/', PartnersAdministratorsBySocietyView.as_view(), name='partners-administrators-by-society'),
]

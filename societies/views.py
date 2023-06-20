from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from societies.models import Society, Partner, Administrator
from societies.serializers import (
    SocietySerializer,
    PartnerSerializer,
    AdministratorSerializer,
    FacultySerializer,
    PartnerAdministratorSerializer
)
from django.db.models import Q


class SocietyCreateView(generics.CreateAPIView):
    def post(self, request, format=None):
        serializer = SocietySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerCreateView(generics.CreateAPIView):
    serializer_class = PartnerSerializer
    def post(self, request, *args, **kwargs):
        society_id = request.data.get('society')
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({'error': 'Society does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(society=society)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdministratorCreateView(generics.CreateAPIView):
    serializer_class = AdministratorSerializer

    def post(self, request, *args, **kwargs):
        society_id = request.data.get('society')
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({'error': 'Society does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        faculties_data = request.data.pop('faculties', [])

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            administrator = serializer.save(society=society)

            for faculty_data in faculties_data:
                faculty_data['administrator'] = administrator.id
                faculty_serializer = FacultySerializer(data=faculty_data)
                if faculty_serializer.is_valid():
                    faculty_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocietyRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Society.objects.all()
    serializer_class = SocietySerializer
    lookup_field = 'rut'


class SocietyByPartnerView(generics.ListAPIView):
    serializer_class = SocietySerializer

    def get_queryset(self):
        partner_rut = self.kwargs['rut']
        societies = Society.objects.filter(Q(partner__rut=partner_rut) | Q(administrator__rut=partner_rut))
        return societies


class PartnersAdministratorsBySocietyView(generics.ListAPIView):
    serializer_class = PartnerAdministratorSerializer

    def get_queryset(self):
        society_rut = self.kwargs['rut']
        try:
            society = Society.objects.get(rut=society_rut)
        except Society.DoesNotExist:
            return []

        partners = society.partner_set.all()
        administrators = society.administrator_set.all()

        queryset = {
            'partners': partners,
            'administrators': administrators,
        }
        return [queryset]

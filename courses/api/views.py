from rest_framework import generics, viewsets
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route

from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, \
                        CourseWithContentSerializer
from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    """for getting subjects list"""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """for getting subject details"""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollView(APIView):

#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)

#         return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
        for getting all courses, enroll course
        and getting enrolled course contents
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['get'],
                  serializer_class=CourseWithContentSerializer,
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @detail_route(methods=['post'],
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)

        return Response({'enrolled': True})

from django.shortcuts import render
from rest_framework import generics


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = UniversityPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moder').exists():
            return Lesson.objects.all()
        else:
            lesson = Lesson.objects.filter(owner=self.request.user)
            return lesson

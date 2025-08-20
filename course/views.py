from django.shortcuts import render
from django.views import View
from django.utils import timezone
from datetime import timedelta

from course.models import Lesson

class VideoRoomView(View):
    def get(self, request, lesson_id):
        lesson = Lesson.objects.filter(id=lesson_id, created__gte=timezone.now() - timedelta(hours=2)).first()
        if lesson:
            return render(request, 'video_room.html', {
                'room_id': lesson_id,
                'role': 'Host',
                'teacher_id': lesson.course.teacher.id,
                'teacher_full_name': lesson.course.teacher.get_full_name(),
            })
        else:
            return render(request, 'lesson_expire.html')

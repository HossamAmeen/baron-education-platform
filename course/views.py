from django.shortcuts import render
from django.views import View

from course.models import Lesson

class VideoRoomView(View):
    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        return render(request, 'video_room.html', {
            'room_id': lesson_id,
            'role': 'Host',
            'teacher_id': lesson.course.teacher.id,
            'teacher_full_name': lesson.course.teacher.get_full_name(),
        })

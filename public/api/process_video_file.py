from django.views import View
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from di.use_cases import UseCases
from domain.model import VideoFile
import os
import uuid

class ProcessVideoFile(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_cases = UseCases.get_instance()

    def post(self, request):
        uploaded_file = self.use_cases.download_video_file_use_case.invoke(request, 'videoFile')

        if not uploaded_file:
            null_file = VideoFile(success=False)
            null_file.errors.append('No file uploaded')
            return null_file.toJSON()
        
        full_file_path = self.use_cases.make_path_use_case.invoke(uploaded_file, 'videos')
        video_file = self.use_cases.save_file_use_case.invoke(full_file_path, uploaded_file)
        video_file.success, video_file.processed_filepath, video_file.counter = self.use_cases.process_video_file_use_case.invoke('/media/rupak/Ddrive/Projects/vehicle-counter-api/best_v.pt', video_file.saved_path, 'processed', video_file.file_name)
        video_file.processed_url = self.use_cases.make_url_use_case.invoke(request.scheme, request.get_host(), video_file.processed_filepath)

        return video_file.toJSON()
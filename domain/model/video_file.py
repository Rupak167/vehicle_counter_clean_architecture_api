from django.http import JsonResponse

class VideoFile:
    def __init__(self, file_name=None, saved_path=None, processed_filepath=None, processed_url=None, counter=None, success=False):
        self.file_name = file_name
        self.saved_path = saved_path
        self.processed_filepath = processed_filepath
        self.processed_url = processed_url
        self.counter = counter
        self.success = success
        self.errors = []

    def toJSON(self):
        return JsonResponse({
            'success': self.success,
            'processed_url': self.processed_url,
            'stat': self.counter,
            'errors': self.errors
        })
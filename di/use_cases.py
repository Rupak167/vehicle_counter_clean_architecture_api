from domain.use_case import DownloadVideoFile, MakePath, SaveFile, ProcessVideoFile, MakeUrl
from django.conf import settings

class UseCases:
    instance = None

    def __init__(self):
        if UseCases.instance is not None:
            raise RuntimeError("An instance of use case class already exist.")
        
        UseCases.instance = self
        self.media_root = settings.MEDIA_ROOT


    @staticmethod
    def get_instance():
        if UseCases.instance is None:
            UseCases.instance = UseCases()
        
        return UseCases.instance
    
    @property
    def download_video_file_use_case(self):
        return DownloadVideoFile()
    
    @property
    def make_path_use_case(self):
        return MakePath(self.media_root)
    
    @property
    def save_file_use_case(self):
        return SaveFile()
    
    @property
    def process_video_file_use_case(self):
        return ProcessVideoFile(self.media_root)
    
    @property
    def make_url_use_case(self):
        return MakeUrl()
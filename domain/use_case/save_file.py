from domain.model import VideoFile

class SaveFile:
    def invoke(self, file_path, file):
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return VideoFile(
            file_name=file.name,
            saved_path=file_path,
            processed_filepath=None,
            processed_url=None,
            counter=None,
            success=False
        )
        

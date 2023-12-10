import os

class MakePath:
    def __init__(self, media_root):
        self.media_root = media_root

    def invoke(self, uploaded_file, parent):
        upload_path = os.path.join(self.media_root, parent)
        os.makedirs(upload_path, exist_ok=True)
        return os.path.join(upload_path, uploaded_file.name)
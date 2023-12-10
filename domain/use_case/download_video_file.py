class DownloadVideoFile:
    def invoke(self, request, attribute_name):
        return request.FILES.get(attribute_name)
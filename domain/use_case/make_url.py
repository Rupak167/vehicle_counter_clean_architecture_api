class MakeUrl:
    def invoke(self, protocol, host, path):
        print("path:", path)
        relative_path = '/media/' + path.split('\\')[-2]+ '/' + path.split('\\')[-1]
        return f"{protocol}://{host}{relative_path}"
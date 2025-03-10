from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


# 🔹 Google Drive Connector
class GoogleDriveConnector:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def read_files(self):
        file_list = self.drive.ListFile({"q": "trashed=false"}).GetList()
        return [f for f in file_list if f["mimeType"] == "text/plain"]

    def write_file(self, filename, content):
        file = self.drive.CreateFile({"title": filename})
        file.SetContentString(content)
        file.Upload()


# 🔹 Local Folder Connector
class LocalConnector:
    def __init__(self, folder_path="./data"):
        self.folder_path = folder_path

    def read_files(self):
        return [
            os.path.join(self.folder_path, f)
            for f in os.listdir(self.folder_path)
            if f.endswith(".txt")
        ]

    def write_file(self, filename, content):
        with open(os.path.join(self.folder_path, filename), "w") as f:
            f.write(content)

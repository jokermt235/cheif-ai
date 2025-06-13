from django.core.files.storage import FileSystemStorage
from injector import inject
import logging

class UploadService:
  def upload(self, file)->bool:
    pass

class FileUploadService(UploadService):
  logger = logging.getLogger(__name__)
  
  @inject
  def __init__(self, file_storage : FileSystemStorage):
    self.file_storage = file_storage

  def upload(self, file)->bool:
    filename = None
    result = False

    try:
      filename = self.file_storage.save(file.name, file)
      result = True
    except:
      self.logger.debug('Error uploading file')

    return result

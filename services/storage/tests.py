from django.test import TestCase
from storage.services import UploadService
from injector import inject

class MockFileUploadService(UploadService):
  def upload(self, file):
    return True

@inject
def test_upload_file_service(service : MockFileUploadService):
  result = service.upload(None)
  assert result


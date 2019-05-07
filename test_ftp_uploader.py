from ftp_uploader import *
import unittest
import ftplib
from mock import patch, mock_open, MagicMock


def test_local_list_empty_folder():
    os.mkdir('dir_test')
    assert list_local_files('dir_test/') == []
    
    
def test_local_list_txt_file():
    f= open("dir_test/test.txt","w+")
    assert list_local_files('dir_test/') == []
    
def test_local_list_jpg_file():
    f= open("dir_test/test.jpg","w+")
    assert list_local_files('dir_test/') == ['test.jpg']
    
def test_delete_function():
    data = ['dir_test/test.txt','dir_test/test.jpg']
    delete_files(data)
    list = os.listdir('dir_test')
    assert list == []
    os.rmdir('dir_test')

def test_diff_fct():
    list = Diff(['1','2'], ['3','2'])
    assert list == ['1']
    
#class TestUploader(unittest.TestCase):

    #@patch('ftplib.FTP', autospec=True)
    #def test_download_file(self, mock_ftp_constructor):
        #mock_ftp = mock_ftp_constructor.return_value
        #mocked_file = MagicMock()
        
        #ftp = ftplib.FTP('ftp.server.local')
        #ftp.login()

        #data = ['test.txt','test.jpg']
        #upload_files(ftp, data)

        #mock_ftp_constructor.assert_called_with('ftp.server.local')
        #self.assertTrue(mock_ftp.login.called)
        #mock_ftp_constructor.return_value.storbinary.assert_called_with(
            #'STOR test.jpg', "test.jpg")
    

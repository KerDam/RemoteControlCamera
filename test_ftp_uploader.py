from ftp_uploader import *


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
    
def test_list_remote_files():
    ftp = ftplib.FTP("files.000webhost.com")
    ftp.login("axc-agile", "axc-agile")
    ftp.cwd("/ftp_tests") 
    list = list_remote_files(ftp)
    assert list == ['1.jpg', '2.jpg']
    

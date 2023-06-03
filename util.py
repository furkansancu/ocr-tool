from subprocess import Popen, PIPE

def TestTesseractPath (path):
    try:
        process = Popen(f'"{path}" --version', stdout=PIPE)
        stdout = process.communicate()
        print(stdout)
        return stdout != b''
    except:
        return False

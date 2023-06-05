import ctypes
import sys
import psutil
import tkinter as tk
from tkinter import filedialog
import win32gui
import win32process
from prettytable import PrettyTable


windows = []


def callback(hwnd, pid):
    global windows
    thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    if process_id == pid:
        if win32gui.IsWindowVisible(hwnd): # check if the window is visible
            windows.append(win32gui.GetWindowText(hwnd))

def run():
    global windows
    print("List of running processes with visible windows:")
    process_dict = {}
    table = PrettyTable(['PID', 'Process Name', 'Window Title'])
    for proc in psutil.process_iter(['pid', 'name']):
        windows = []
        win32gui.EnumWindows(callback, proc.info['pid'])
        if windows:  # if the process has a visible window
            for window in windows:
                table.add_row([proc.info['pid'], proc.info['name'], window])
            process_dict[proc.info['pid']] = proc.info['name']

    print(table)
    
    pid = int(input('Enter the PID of the process to inject into: '))
    if pid not in process_dict:
        print("Invalid PID. Returning to main menu.")
        return

    root = tk.Tk()
    root.withdraw()
    root.iconify()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')

    dll_path = filedialog.askopenfilename(filetypes=[('Dynamic Link Libraries', '*.dll')])  
    root.destroy()

    if not dll_path:
        print("No DLL file selected. Returning to main menu.")
        return

    print("Please choose an injection method:")
    print("1. LoadLibrary")
    print("2. Manual Mapping")
    injection_method = int(input("Enter your choice: "))

    if injection_method == 1:
        try:
            inject_dll(pid, dll_path)
        except Exception as e:
            print(f"An error occurred: {e}. Returning to main menu.")
    elif injection_method == 2:
        print("Manual Mapping is selected. This method is not implemented yet.")
    else:
        print("Invalid choice. Returning to main menu.")


def inject_dll(pid, dll_path):
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    kernel32 = ctypes.windll.kernel32
    dll_len = len(dll_path)

    # Get handle to process
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print("Couldn't acquire a handle to PID: %s" % pid)
        sys.exit(0)

    # Allocate space for DLL path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

    # Write DLL path into memory
    written = ctypes.c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, ctypes.byref(written))

    # Resolve LoadLibraryA address
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

    # Now we create a remote thread that starts begins at LoadLibraryA and is passed our DLL path as an argument
    thread_id = ctypes.c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id)):
        print("Failed to inject the DLL. Exiting.")
        sys.exit(0)

    print("Remote Thread with ID 0x%08x created." % thread_id.value)

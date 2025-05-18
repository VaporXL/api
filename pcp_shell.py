#!/usr/bin/env python3
import os
import sys
import shutil
import time
import platform
import subprocess
import datetime

# Logitech blue RGB (0,174,239)
BLUE = "\033[38;2;0;174;239m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

# BASIC program storage
basic_program = {}

def splash_screen():
    print(CLEAR)
    print(f"{BLUE}╔════════════════════════════════╗")
    print("║        PC P - POPLISTIC        ║")
    print("║      COMMAND PROCESSOR v1.5    ║")
    print("╚════════════════════════════════╝")
    print("© 2025 Poplistic Systems")
    print("Type HELP for commands\n" + RESET)

def help_text():
    print(f"""{BLUE}
Available commands:

CAT                       - List files
TYPE <file>               - Show file contents
RUN <file>                - Run a python script
DELETE <file>             - Delete a file
RENAME <old> <new>        - Rename a file
COPY <src> <dest>         - Copy a file
MKDIR <name>              - Create directory
RMDIR <name>              - Remove directory
CLS                       - Clear screen
TIME                      - Show current time
SYSINFO                   - Show system info
REBOOT                    - Reboot Raspberry Pi
SHUTDOWN                  - Shutdown Raspberry Pi
HELP                      - Show this help
EXIT / QUIT               - Exit shell
ECHO <text>               - Print text
COLOR <r> <g> <b>         - Set text color (RGB)
BEEP                      - Beep sound (if possible)

BASIC                     - Enter BASIC mode
NEW                       - Clear BASIC program
LIST                      - List BASIC program
SAVE <file>               - Save BASIC program to file
LOAD <file>               - Load BASIC program from file
RUN                       - Run BASIC program

{RESET}""")

def list_files():
    files = os.listdir('.')
    for f in files:
        print(f)

def type_file(filename):
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        return
    with open(filename, 'r') as file:
        print(file.read())

def run_python(filename):
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        return
    try:
        subprocess.run(['python3', filename])
    except Exception as e:
        print(f"Error running file: {e}")

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted '{filename}'")
    except Exception as e:
        print(f"Error deleting file: {e}")

def rename_file(old, new):
    try:
        os.rename(old, new)
        print(f"Renamed '{old}' to '{new}'")
    except Exception as e:
        print(f"Error renaming file: {e}")

def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"Copied '{src}' to '{dest}'")
    except Exception as e:
        print(f"Error copying file: {e}")

def mkdir_dir(name):
    try:
        os.mkdir(name)
        print(f"Directory '{name}' created.")
    except Exception as e:
        print(f"Error creating directory: {e}")

def rmdir_dir(name):
    try:
        os.rmdir(name)
        print(f"Directory '{name}' removed.")
    except Exception as e:
        print(f"Error removing directory: {e}")

def cls_screen():
    print(CLEAR)

def show_time():
    now = datetime.datetime.now()
    print(now.strftime("%H:%M:%S"))

def sys_info():
    print(f"PC P SYSTEM - {platform.platform()} | {platform.machine()} | Python {platform.python_version()}")

def reboot_pi():
    print("Rebooting Raspberry Pi...")
    os.system("sudo reboot")

def shutdown_pi():
    print("Shutting down Raspberry Pi...")
    os.system("sudo shutdown now")

def echo_text(text):
    print(text)

def set_color(r, g, b):
    global BLUE
    try:
        r = int(r)
        g = int(g)
        b = int(b)
        BLUE = f"\033[38;2;{r};{g};{b}m"
        print(f"Text color set to RGB({r},{g},{b})")
    except:
        print("Invalid color values. Usage: COLOR <r> <g> <b>")

def beep_sound():
    try:
        # Try system bell
        print('\a')
    except:
        print("Beep not supported.")

# BASIC interpreter core

def basic_new():
    global basic_program
    basic_program = {}
    print("BASIC program cleared.")

def basic_list():
    if not basic_program:
        print("No BASIC program loaded.")
        return
    for line in sorted(basic_program.keys()):
        print(f"{line} {basic_program[line]}")

def basic_save(filename):
    try:
        with open(filename, 'w') as f:
            for line in sorted(basic_program.keys()):
                f.write(f"{line} {basic_program[line]}\n")
        print(f"BASIC program saved to '{filename}'")
    except Exception as e:
        print(f"Error saving BASIC program: {e}")

def basic_load(filename):
    global basic_program
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        return
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        basic_program = {}
        for l in lines:
            parts = l.strip().split(' ', 1)
            if len(parts) == 2 and parts[0].isdigit():
                basic_program[int(parts[0])] = parts[1]
        print(f"BASIC program loaded from '{filename}'")
    except Exception as e:
        print(f"Error loading BASIC program: {e}")

def basic_run():
    if not basic_program:
        print("No BASIC program loaded.")
        return
    lines = sorted(basic_program.keys())
    line_index = 0
    while line_index < len(lines):
        line_num = lines[line_index]
        statement = basic_program[line_num].strip()
        # Simple parse: support PRINT and GOTO only
        if statement.upper().startswith("PRINT"):
            # Extract text after PRINT
            arg = statement[5:].strip()
            if arg.startswith('"') and arg.endswith('"'):
                # Remove quotes
                text = arg[1:-1]
                print(text, end='')
            elif arg.endswith(';'):
                # e.g. PRINT "EXAMPLE! ";
                if arg.startswith('"'):
                    text = arg[1:-2]
                    print(text, end='')
                else:
                    print(arg, end='')
            else:
                print(arg)
        elif statement.upper().startswith("GOTO"):
            target_line_str = statement[4:].strip()
            if target_line_str.isdigit():
                target_line = int(target_line_str)
                if target_line in basic_program:
                    line_index = lines.index(target_line)
                    continue
                else:
                    print(f"Line {target_line} not found.")
                    break
            else:
                print("Invalid GOTO target.")
                break
        elif statement.upper() == "END":
            break
        else:
            print(f"Unknown BASIC command at line {line_num}: {statement}")
        line_index += 1
    print()  # newline after program run

def basic_interpreter():
    print(f"{BLUE}Entering BASIC mode. Type NEW to clear program, RUN to execute, LIST to view, SAVE/LOAD <file>, or EXIT to quit BASIC mode.{RESET}")
    while True:
        line = input("BASIC> ").strip()
        if line.upper() == "EXIT":
            break
        elif line.upper() == "NEW":
            basic_new()
        elif line.upper() == "LIST":
            basic_list()
        elif line.upper().startswith("SAVE "):
            _, filename = line.split(" ", 1)
            basic_save(filename.strip())
        elif line.upper().startswith("LOAD "):
            _, filename = line.split(" ", 1)
            basic_load(filename.strip())
        elif line.upper() == "RUN":
            basic_run()
        elif line == "":
            continue
        else:
            # Expect line starting with a number for BASIC code
            parts = line.split(' ', 1)
            if parts[0].isdigit() and len(parts) == 2:
                line_num = int(parts[0])
                basic_program[line_num] = parts[1]
            else:
                print("Invalid BASIC line. Must start with line number and code.")

def main():
    splash_screen()
    current_color = BLUE

    while True:
        try:
            cmd = input(f"{current_color}] {RESET}").strip()
            if not cmd:
                continue

            parts = cmd.split()
            command = parts[0].upper()
            args = parts[1:]

            if command == "HELP":
                help_text()
            elif command == "CAT":
                list_files()
            elif command == "TYPE":
                if args:
                    type_file(args[0])
                else:
                    print("Usage: TYPE <file>")
            elif command == "RUN":
                if args:
                    run_python(args[0])
                else:
                    # Run BASIC program
                    basic_run()
            elif command == "DELETE":
                if args:
                    delete_file(args[0])
                else:
                    print("Usage: DELETE <file>")
            elif command == "RENAME":
                if len(args) == 2:
                    rename_file(args[0], args[1])
                else:
                    print("Usage: RENAME <old> <new>")
            elif command == "COPY":
                if len(args) == 2:
                    copy_file(args[0], args[1])
                else:
                    print("Usage: COPY <src> <dest>")
            elif command == "MKDIR":
                if args:
                    mkdir_dir(args[0])
                else:
                    print("Usage: MKDIR <name>")
            elif command == "RMDIR":
                if args:
                    rmdir_dir(args[0])
                else:
                    print("Usage: RMDIR <name>")
            elif command == "CLS":
                cls_screen()
            elif command == "TIME":
                show_time()
            elif command == "SYSINFO":
                sys_info()
            elif command == "REBOOT":
                reboot_pi()
            elif command == "SHUTDOWN":
                shutdown_pi()
            elif command == "ECHO":
                echo_text(' '.join(args))
            elif command == "COLOR":
                if len(args) == 3:
                    set_color(args[0], args[1], args[2])
                else:
                    print("Usage: COLOR <r> <g> <b>")
            elif command == "BEEP":
                beep_sound()
            elif command == "BASIC":
                basic_interpreter()
            elif command == "NEW":
                basic_new()
            elif command == "LIST":
                basic_list()
            elif command == "SAVE":
                if args:
                    basic_save(args[0])
                else:
                    print("Usage: SAVE <file>")
            elif command == "LOAD":
                if args:
                    basic_load(args[0])
                else:
                    print("Usage: LOAD <file>")
            elif command in ["EXIT", "QUIT"]:
                print("Goodbye!")
                break
            else:
                print(f"Unknown command '{command}'. Type HELP for list.")
        except KeyboardInterrupt:
            print("\nUse EXIT to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

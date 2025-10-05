import os, sys, time

# Warna dasar (pakai ANSI escape code)
class Color:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    WHITE = "\033[97m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03, color=Color.WHITE):
    for c in text:
        sys.stdout.write(color + c + Color.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(text="Loading", dots=5, delay=0.3, color=Color.YELLOW):
    for i in range(dots):
        sys.stdout.write(f"\r{color}{text}{'.' * (i+1)}{' ' * (dots-i)}{Color.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

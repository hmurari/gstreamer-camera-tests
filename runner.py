import subprocess
import time

def main():
    for method in range(8):
        args = ['python3', 'camera-test.py', '--method', str(method), '--device', '0']
        subprocess.run(args)
        time.sleep(1)

if __name__ == '__main__':
    main()

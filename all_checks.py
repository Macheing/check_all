import shutil
import os,sys
import socket

def check_reboot():
    '''Return true if the computer has a pending reboot.'''
    return os.path.exists('/run/reboot-required')

def check_disk_full(disk, min_gb,min_percent):
    '''Return true if there isn't enough disk space, or false otherwise.'''
    du = shutil.disk_usage(disk)
    # calculate the percent of of free space.
    percet_free = 100 * du.free/du.total
    # calculates number of free gigabytes
    gigabytes_free = du.free/2**30

    if gigabytes_free < min_percent or gigabytes_free < min_gb:
        return True

    return False

def check_root_full():
    '''Returns true if root partition is full, false otherwise.'''
    return check_disk_full(disk='/', min_gb= 2, min_percent= 10)
    
def check_no_network():
    '''Return true if it fails to resolve google's url, otherwise false.'''
    try:
        socket.gethostbyname('www.google.com')
        return False
    except:
        return True

def main():
    checks = [
                (check_reboot, 'Pending Reboot'),
                (check_root_full, "Root partition full!"),
                (check_no_network, 'No working network.'),
              ]

    everything_ok = True

    for check, message in checks:
        if check():
            print(message)
            #sys.exit(1)
            everything_ok = False
    
    if not everything_ok:
        sys.exit(1)
    
    print('Everything ok!')
    sys.exit(0)

main()

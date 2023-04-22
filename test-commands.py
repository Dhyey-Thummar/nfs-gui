import sys
import subprocess
import shutil
import os

def mount_client(server_ip, mount_point_server, mount_point_client):
    try:
        subprocess.call(['sudo', 'mount', '-t', 'nfs', server_ip + ':' + mount_point_server, mount_point_client])
    except Exception as e:
        print(f'Error mounting NFS share: {e}')
    finally:
        print('mount_client() finished')

def umount_client(mount_point_client):
    try:
        subprocess.call(['sudo', 'umount', mount_point_client])
    except Exception as e:
        print(f'Error unmounting NFS share: {e}')
    finally:
        print('umount_client() finished')

def check_mount(mount_point_client):
    if os.path.ismount(mount_point_client):
        print('NFS share mounted')
        return True
    else:
        print('NFS share not mounted')
    return False

def main():
    server_ip = input('Enter server IP: ')
    mount_point_server = input('Enter server mount point: ')
    mount_point_client = input('Enter client mount point: ')

    while True:
        try:
            what = input('Enter what to do (mount/umount/check/exit): ')
            match what:
                case 'mount':
                    mount_client(server_ip, mount_point_server, mount_point_client)
                case 'umount':
                    umount_client(mount_point_client)
                case 'check':
                    check_mount(mount_point_client)
                case 'exit':
                    sys.exit(0)
                case _:
                    print('Invalid option')
        except KeyboardInterrupt:
            print('Exiting...')
            sys.exit(0)
    

if __name__ == '__main__':
    main()
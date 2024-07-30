import os
import hashlib
import time
import stat
import argparse
import logging
import subprocess

# Idea is to make the script close all the port with IP tables/ufw when the file integrity changes without disrupting normal network activity
# Also ellaborate on the parsing with logic rules
# Add tcp and tshark capabilities


# Define the directories to monitor
DEFAULT_DIRECTORIES_TO_MONITOR = ["/etc", "/var/log", "/bin", "/sbin", "/usr/bin", "/usr/sbin", "/root", "/home", "/var/www"]

# Define the hash function to use
DEFAULT_HASH_FUNC = hashlib.sha256

# Define Arguments
def get_args():
    parser = argparse.ArgumentParser(description='Monitor specified directories for file modifications')
    parser.add_argument('-d', '--directories', nargs='+', default=DEFAULT_DIRECTORIES_TO_MONITOR,
                        help='directories to monitor (default: %(default)s)')
    parser.add_argument('-f', '--hash-func', default='sha256',
                        help='hash function to use (default: %(default)s)')
    parser.add_argument('-i', '--interval', type=int, default=5,
                        help='time interval in seconds between checks (default: %(default)s)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose output')
    returnHunting parser.parse_args()
    parser.add_argument('-th', action='store_true', help='Networking and Monitoring logs')


def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')


def get_initial_metadata(directories, hash_func):
    metadata = {}
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                print(filepath)  # add this line
                with open(filepath, 'rb') as f:
                    metadata[filepath] = hash_func(f.read()).hexdigest()
    return metadata




def monitor_directories(directories, hash_func, interval):
    initial_metadata = get_initial_metadata(directories, hash_func)
    while True:
        for directory in directories:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if not os.path.exists(filepath):
                        # The file has been deleted
                        logging.info("File %s has been deleted!", filepath)
                        initial_metadata.pop(filepath, None)
                        continue

                    # Get the current hash value of the file contents
                    with open(filepath, 'rb') as f:
                        file_contents = f.read()
                    current_content_hash = hash_func(file_contents).hexdigest()

                    # Get the current metadata values of the file
                    current_metadata = os.stat(filepath)

                    # If the file is a symlink, get the metadata values of the link itself
                    if stat.S_ISLNK(current_metadata.st_mode):
                        link_target = os.readlink(filepath)
                        current_metadata = os.stat(link_target)

                    # If the hash or metadata values have changed, log the modification
                    if current_content_hash != initial_metadata[filepath]['content_hash']:
                        logging.info("File %s has been modified (content)!", filepath)
                        initial_metadata[filepath]['content_hash'] = current_content_hash
                    if current_metadata != initial_metadata[filepath]['metadata']:
                        logging.info("File %s has been modified (metadata)!", filepath)
                        initial_metadata[filepath]['metadata'] = current_metadata

        time.sleep(interval)

# Network/System Monitoring Funtion

def check_ports_and_processes():
    # CHECK PORTS
    print("Checking ports:")
    result_ports = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    ports_output = result_ports.stdout
    print(ports_output)

    # PROCESS
    print("Running processes:")
    result_processes = subprocess.run(['ps', '-auxwf'], capture_output=True, text=True)
    processes_output = result_processes.stdout
    print(processes_output)

    return ports_output, processes_output

# IP tables function
# NEED TO WORK ON
def setup_iptables(accept=False):
    # IPTABLES TO DROP
    subprocess.run(['sudo', 'iptables', '-F'])
    subprocess.run(['sudo', 'iptables', '-P', 'INPUT', 'DROP'])
    subprocess.run(['sudo', 'iptables', '-P', 'FORWARD', 'DROP'])
    subprocess.run(['sudo', 'iptables', '-P', 'OUTPUT', 'DROP'])

    if accept:
        print("Flow")
        subprocess.run(['sudo', 'iptables', '-P', 'INPUT', 'ACCEPT'])
        subprocess.run(['sudo', 'iptables', '-P', 'FORWARD', 'ACCEPT'])
        subprocess.run(['sudo', 'iptables', '-P', 'OUTPUT', 'ACCEPT'])


# Main Function

if __name__ == '__main__':
    args = get_args()

    if args.th:
        ports_output, processes_output = check_ports_and_processes()
    else:
        hash_func = args.hash_func
        setup_logging(args.verbose)
        monitor_directories(args.directories, getattr(hashlib, hash_func), args.interval)

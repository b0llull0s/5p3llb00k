#!/usr/bin/env python3

import argparse
import subprocess
import sys

def is_mounted(device):
    try:
        result = subprocess.run(['findmnt', '-n', '-o', 'TARGET', device], capture_output=True, text=True)
        return result.stdout.strip() != ""
    except subprocess.CalledProcessError:
        return False

def format_device(device, fs_type, label=None, quick=False):
    try:
        # Check if the device is mounted
        if is_mounted(device):
            print(f"Unmounting {device}...")
            subprocess.run(['sudo', 'umount', device], check=True)
        else:
            print(f"{device} is not mounted.")
        
        # Build the formatting command
        format_cmd = []
        if fs_type == 'ext4':
            format_cmd = ['sudo', 'mkfs.ext4']
            if quick:
                format_cmd.append('-F')
        elif fs_type == 'ntfs':
            format_cmd = ['sudo', 'mkfs.ntfs']
            if quick:
                format_cmd.append('-Q')
        elif fs_type == 'xfs':
            format_cmd = ['sudo', 'mkfs.xfs']
            # XFS does not have a quick format option
        elif fs_type == 'vfat':
            format_cmd = ['sudo', 'mkfs.vfat']
            if quick:
                format_cmd.append('-F')
        elif fs_type == 'btrfs':
            format_cmd = ['sudo', 'mkfs.btrfs']
            # BTRFS does not have a quick format option
        elif fs_type == 'exfat':
            format_cmd = ['sudo', 'mkfs.exfat']
            # exFAT does not have a quick format option

        # Add label if specified
        if label:
            if fs_type in ['ext4', 'ntfs', 'vfat', 'exfat']:
                format_cmd.extend(['-n', label])
            else:
                print(f"Labeling not supported for {fs_type} filesystem.")
        
        format_cmd.append(device)
        
        # Execute the formatting command
        print(f"Formatting {device} as {fs_type}...")
        subprocess.run(format_cmd, check=True)
        
        print(f"Formatting complete. {device} is now formatted as {fs_type}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Format a USB or SSD device.')
    parser.add_argument('device', type=str, help='The device to format (e.g., /dev/sdX1)')
    parser.add_argument('-f', '--filesystem', type=str, required=True, help='The filesystem type to use (e.g., ext4, ntfs, xfs, vfat, btrfs, exfat)')
    parser.add_argument('-l', '--label', type=str, help='Label for the filesystem')
    parser.add_argument('-q', '--quick', action='store_true', help='Perform a quick format')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate filesystem type
    valid_filesystems = ['ext4', 'ntfs', 'xfs', 'vfat', 'btrfs', 'exfat']
    if args.filesystem not in valid_filesystems:
        print(f"Invalid filesystem type: {args.filesystem}. Choose from {', '.join(valid_filesystems)}.")
        sys.exit(1)

    # Call the format function
    format_device(args.device, args.filesystem, label=args.label, quick=args.quick)

if __name__ == "__main__":
    main()

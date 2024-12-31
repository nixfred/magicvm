#!/usr/bin/env python3
import os
import random
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DEFAULT_RAM_GB = "8"  # Default RAM size in GB
DEFAULT_DISK_GB = "10"  # Default Disk size in GB
DEFAULT_ISO_PATH = "/var/lib/libvirt/images/magicvm.iso"

def print_ascii_art():
    ascii_art = r"""
 __   __  ___  ____    _    ____  __  __ ___ _   _ 
 \ \ / / |_ _|| __ )  / \  / ___||  \/  |_ _| \ | |
  \ V /   | | |  _ \ / _ \ \___ \| |\/| || ||  \| |
   | |    | | | |_) / ___ \ ___) | |  | || || |\  |
   |_|   |___||____/_/   \_\____/|_|  |_|___|_| \_|
    """
    print(ascii_art)

def get_input(prompt, default_value):
    user_input = input(f"{prompt} [{default_value}]: ").strip()
    return user_input or default_value

def validate_file_path(file_path):
    if not Path(file_path).exists():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File {file_path} does not exist.")
    return file_path

def check_storage_pool_space(required_size_gb):
    pool_info_cmd = ["virsh", "pool-info", "default"]
    try:
        output = subprocess.check_output(pool_info_cmd, text=True)
        for line in output.splitlines():
            if "Available" in line:
                available_space_gb = float(line.split(":")[1].strip().split()[0])  # Get available space in GB
                if required_size_gb > available_space_gb:
                    raise ValueError(
                        f"Requested disk size ({required_size_gb} GB) exceeds available space ({available_space_gb} GB)."
                    )
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to retrieve storage pool information.")

def run_command(command, description=""):
    logging.info(f"Executing: {description or ' '.join(command)}")
    try:
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.cmd}\nError: {e.output}")
        raise

def create_vm(vm_name, ram_size_gb, disk_size_gb, iso_file):
    check_storage_pool_space(int(disk_size_gb))
    cmd = [
        "virt-install",
        "--name", vm_name,
        "--ram", str(int(ram_size_gb) * 1024),  # Convert GB to MB for RAM
        "--disk", f"pool=default,size={disk_size_gb},format=qcow2",  # Explicit size in GB
        "--vcpus", "2",
        "--os-variant", "ubuntu20.04",
        "--network", "bridge=virbr0",
        "--graphics", "none",
        "--cdrom", iso_file,
    ]
    run_command(cmd, f"Creating VM '{vm_name}'")

if __name__ == "__main__":
    print_ascii_art()
    try:
        vm_name = get_input("Enter a name for the VM", f"{random.choice(['magic', 'wizard', 'sorcerer'])}-{random.choice(['cat', 'wand', 'spell'])}")
        ram_size_gb = get_input("Enter amount of RAM for the VM in GB", DEFAULT_RAM_GB)
        disk_size_gb = get_input("Enter the size of the virtual drive in GB", DEFAULT_DISK_GB)
        iso_file = validate_file_path(get_input("Enter the name or full path of the ISO file", DEFAULT_ISO_PATH))

        logging.info("Starting VM creation process...")
        create_vm(vm_name, ram_size_gb, disk_size_gb, iso_file)

        logging.info("VM creation completed successfully!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

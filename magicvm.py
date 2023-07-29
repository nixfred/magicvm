#!/usr/bin/env python3
import os
import random
import subprocess

def print_ascii_art():
    ascii_art = r"""
 __   __  ___  ____    _    ____  __  __ ___ _   _ 
 \ \ / / |_ _|| __ )  / \  / ___||  \/  |_ _| \ | |
  \ V /   | | |  _ \ / _ \ \___ \| |\/| || ||  \| |
   | |    | | | |_) / ___ \ ___) | |  | || || |\  |
   |_|   |___||____/_/   \_\____/|_|  |_|___|_| \_|
    """
    print(ascii_art)

def get_vm_name():
    vm_name = input("Enter a name for the VM: ")
    return vm_name.strip() or f"{random.choice(['magic', 'wizard', 'sorcerer'])}-{random.choice(['cat', 'wand', 'spell'])}"

def get_ram_size():
    default_ram = "8000"
    ram_size = input(f"Enter amount of RAM for the VM in MB [{default_ram}MB]: ")
    return ram_size.strip() or default_ram

def get_disk_size():
    default_disk = "10000"  # Lowered the default disk size to 10000 MB
    disk_size = input(f"Enter the size of the virtual drive in MB [{default_disk}MB]: ")
    return disk_size.strip() or default_disk

def get_iso_file():
    default_iso_path = "/home/pi/Downloads/magicvm.iso"
    iso_file = input(f"Enter the name or full path of the ISO file [{default_iso_path}]: ")
    return iso_file.strip() or default_iso_path

def create_vm(vm_name, ram_size, disk_size, iso_file):
    cmd_create_vm = [
        "virt-install",
        "--name", vm_name,
        "--ram", f"{ram_size}",
        "--disk", f"pool=default,size={disk_size}",
        "--vcpus", "2",
        "--os-variant", "ubuntu20.04",
        "--network", "bridge=virbr0",
        "--graphics", "none",
        "--import",
        "--cdrom", iso_file,
    ]
    subprocess.run(cmd_create_vm, check=True)  # Throw exception if command fails

def upgrade_vm(vm_name):
    cmd_shutdown = ["virsh", "shutdown", vm_name]
    subprocess.run(cmd_shutdown, check=True)  # Throw exception if command fails

    cmd_resize_disk = [
        "virt-resize",
        "--expand", "/dev/sda1",
        f"{vm_name}-disk", f"{vm_name}-disk-resized"
    ]
    subprocess.run(cmd_resize_disk, check=True)  # Throw exception if command fails

    cmd_replace_disk = [
        "virsh",
        "undefine",
        vm_name,
    ]
    subprocess.run(cmd_replace_disk, check=True)  # Throw exception if command fails

    cmd_define_vm = [
        "virsh",
        "define",
        f"{vm_name}-disk-resized",
    ]
    subprocess.run(cmd_define_vm, check=True)  # Throw exception if command fails

    cmd_start = ["virsh", "start", vm_name]
    subprocess.run(cmd_start, check=True)  # Throw exception if command fails

    os.remove(f"{vm_name}-disk-resized")

if __name__ == "__main__":
    print_ascii_art()
    vm_name = get_vm_name()
    ram_size = get_ram_size()
    disk_size = get_disk_size()
    iso_file = get_iso_file()

    try:
        print("Creating the VM...")
        create_vm(vm_name, ram_size, disk_size, iso_file)

        print("Upgrading the VM...")
        upgrade_vm(vm_name)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing a command: {e.cmd}\nError message: {e.output}")
    else:
        print("VM creation and upgrade completed successfully!")

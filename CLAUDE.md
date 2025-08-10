# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MagicVM is a Python-based virtual machine creation tool that provides a simple CLI interface for creating KVM/QEMU virtual machines using libvirt. The tool uses `virt-install` to create VMs with user-specified parameters including RAM, disk size, and ISO image.

## Prerequisites & Dependencies

- Python 3.12+ 
- libvirt 10.0.0+ with virsh
- virt-install
- KVM/QEMU virtualization support
- Default storage pool configured in libvirt

## Common Development Commands

### Running the Tool
```bash
# Make the script executable (if needed)
chmod +x magicvm.py

# Run the VM creation tool
./magicvm.py
# or
python3 magicvm.py
```

### Git Operations
```bash
# Automated update and push script
./update.sh

# Manual git operations
git add .
git commit -m "Update files - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin master
```

## Architecture & Key Components

### Main Script: magicvm.py
- **Entry point**: Interactive CLI that prompts for VM configuration
- **Key functions**:
  - `create_vm()`: Core VM creation using virt-install
  - `check_storage_pool_space()`: Validates available storage before VM creation
  - `validate_file_path()`: Ensures ISO file exists before proceeding
- **Default values**:
  - RAM: 8GB
  - Disk: 10GB  
  - ISO Path: `/var/lib/libvirt/images/magicvm.iso`
  - Network: virbr0 bridge
  - Graphics: none (headless)

### Automation: update.sh
- Handles git operations automatically
- Creates new GitHub repos if .git doesn't exist
- Uses SSH authentication for GitHub operations

## Important Considerations

- VMs are created in the "default" libvirt storage pool
- Disk format is qcow2 for efficient storage
- VMs are configured with serial console for headless access
- OS variant is set to "generic" for broad compatibility
- The tool checks available storage space before creating VMs to prevent failures

## Project Vision & Next Steps

### Current State (v0.9)
The script is functional but requires user interaction for each VM parameter. It successfully creates VMs but lacks the "magic" that would make it truly effortless.

### Vision for v1.0
Transform MagicVM into a tool where VM creation is as simple as:
```bash
magicvm ubuntu-test
```

### Key Questions Being Addressed
1. **Use Case Definition**: Determining if this is for quick testing, lab automation, or learning
2. **Interface Design**: Balancing simplicity with flexibility
3. **Automation Level**: How much should be automatic vs configurable
4. **Network & SSH**: Auto-configuration of networking and SSH access
5. **Template System**: Pre-configured VMs for common scenarios

### Development Approach
- Interview-driven design to understand real user needs
- Iterative development with user feedback
- Focus on removing friction from VM creation
- Keep advanced features optional

### Next Implementation Steps
1. Gather requirements through user interview
2. Design minimal command-line interface
3. Implement smart defaults and templates
4. Add automation for common tasks (SSH keys, networking)
5. Create preset configurations for common use cases

See ROADMAP.md for detailed development phases.
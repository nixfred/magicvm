# MagicVM

A simple, fast virtual machine creation tool for KVM/QEMU that removes the complexity from VM deployment.

## Current Status: v0.9
- Basic VM creation with user prompts
- Support for Ubuntu Server and Linux Mint ISOs
- Automatic network configuration
- Console access for headless installations

## Usage
```bash
./magicvm.py
```

Follow the prompts to:
1. Name your VM
2. Allocate RAM (GB)
3. Set disk size (GB)
4. Select ISO image

## Requirements
- KVM/QEMU with libvirt
- Python 3.12+
- virt-install
- Default storage pool configured

## Project Vision - Interview Questions

### Next Phase Development (v1.0)
We're redesigning MagicVM based on real user needs. Key questions to address:

1. **Primary Goal**: What's the main purpose? Quick testing? Lab automation? Learning?
2. **Use Cases**: One-off VMs? Multiple lab environments? Template deployments?
3. **Pain Points**: What's wrong with existing tools? Too complex? Too slow?
4. **The "Magic"**: What would ideal VM creation look like? One command? Auto-SSH?
5. **Target Users**: Personal tool? Team use? Public release?
6. **OS Focus**: Ubuntu Server? Mixed Linux? Windows support?
7. **Priority**: Speed? Simplicity? Flexibility?

These questions will shape v1.0 to be truly "magical" - removing friction from VM creation.

#!/bin/bash

# Function to update and push changes to GitHub
update_and_push() {
    local dir="$1"

    # Check if the directory contains a .git directory
    if [ -d "$dir/.git" ]; then
        # Change to the directory containing .git
        cd "$dir"

        # Check if there are changes in the local repository
        if [ -n "$(git status --porcelain)" ]; then
            # Stage all changes in the directory
            git add .

            # Commit the changes with a timestamp-based commit message
            git commit -m "Update files - $(date '+%Y-%m-%d %H:%M:%S')"

            # Push the changes to the remote repository on GitHub using SSH
            git push origin master

            echo "Update successful for directory: '$dir'."
        else
            echo "No changes detected for directory: '$dir'."
        fi
    else
        # Initialize a new Git repository in the current directory
        git -C "$dir" init

        # Add all files in the directory to the staging area
        git -C "$dir" add .

        # Commit the changes with a timestamp-based commit message
        git -C "$dir" commit -m "Initial commit - $(date '+%Y-%m-%d %H:%M:%S')"

        # Get the GitHub username from the SSH URL
        local github_username=$(git -C "$dir" config remote.origin.url | cut -d ':' -f 2 | cut -d '/' -f 1)

        # Create a new GitHub repository using the GitHub API
        curl -u "$github_username" -X POST https://api.github.com/user/repos -d '{"name":"'"$(basename "$dir")"'"}'

        # Set the remote origin using SSH
        git -C "$dir" remote add origin "git@github.com:$github_username/$(basename "$dir").git"

        # Push the changes to the remote repository on GitHub using SSH
        git -C "$dir" push -u origin master

        echo "New repository '$(basename "$dir")' created on GitHub from directory: '$dir'."
    fi
}

# Get the current directory where the script is executed
current_directory="$(pwd)"

# Set the SSH agent socket for this session to ensure proper SSH authentication
export SSH_AUTH_SOCK="$HOME/.ssh/ssh-agent"

# Call the function to update and push changes using the current directory
update_and_push "$current_directory"

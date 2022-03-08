#!/bin/bash
# Script to cd into each student's assignment directory to fix issues 

for directory in $(ls -d */)
do
  cd $directory
  echo "pulling updates to $directory"
  git pull || echo "Not a git repo"

  # Make fixes

  echo "pushing to github"
  git add .
  git commit -m "Assignment patch" # Add additional commit messages
  git push

  cd ..
done


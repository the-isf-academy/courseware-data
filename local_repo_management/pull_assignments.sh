#!/bin/bash
# Script to cd into each student's assignment directory and git pull to automate
# refreshing submissions before grading

for directory in $(ls -d */)
do
  cd $directory
  echo "pulling updates to $directory"
  git pull || echo "Not a git repo"
  cd ..
done

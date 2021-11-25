# Bilateral Assignment
This project is a demostration of how processes works in different stages

## File Structure
### Processing  - processing files
### Queue       - queue files
### Processed   - processed files
### process_main.py - Python Script to do following work simulatenously

- Initialise db and threads
- Thread 1 Create a file (processing files) every second and mention it as 0 in db
- Thread 2 Move from processing files to queue files every 5 seconds and when Queue directory is empty
- Thread 3 Move queue files to processed files and updating status on db as 1

## DataBase Information
- Works on MongoDB
- ProcessDB MongoDB database
- ProcessCollection MongoDB collection 

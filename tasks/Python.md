# Python task

In this task you'll implement a bunch of basic functions for manipulating data in Python. The only source file is located 
in `src/aggregate_pdf_reports.py`. Here you will find a couple of function signatures along with their description (what 
should they do). Your task is to implement all of these functions.

You can simply check your implementation by running the script (e.g. `python src/aggregate_pdf_reports.py`) or just look 
at the `if __name__ == '__main__':` block to get the idea how should it work.


## Scenario
Our main domain is finding different pathologies on X-Ray images. After each scan is processed, we generate a PDF report 
describing what our neural network has found.

Metadata about PDF reports are stored in our DB and the actual reports are stored in the Azure Blob Storage. 

These PDF reports are then often analysed to see if we are doing a good job or not. And it is very handy to have them 
all as a single PDF file.


## Task
Implement all functions inside `src/aggregate_pdf_reports.py` module to get it up and running. Result of running the 
script should be:
- Directory containing all PDF reports from the last 14 days.
- Directory containing a single PDF file – all reports joined together.

You can use any libraries you want. Use ChatGPT or any other LLM to assist you in any way you seem appropriate.

Credentials for connecting to the Azure Blob Storage were provided to you by e-mail.


## Requirements
- All functions in `src/aggregate_pdf_reports.py` are implemented and the script is runnable.
- The script produces results described above.
- Write a step-by-step guide on how run the script.
- Don't forget to provide packages you have used (ideally via `requirements.txt`).
- Document your code.
- Adhere to PEP 8 and make sure your code is nice and clean.
- _[Optional]_ Unittests are very nice to have. :-)

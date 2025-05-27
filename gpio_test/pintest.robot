*** Settings ***
Library           Process

*** Test Cases ***
Pump On Trigger
    Start Process     ./scripts/scriptzero.py
    Sleep            5s
    Terminate All Processes

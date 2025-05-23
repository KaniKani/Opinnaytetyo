*** Settings ***
Library     seriallib.py

*** Variables ***
${PORT}     /dev/ttyUSB0
${BAUDRATE}     115200

*** Test Cases ***

Check Moisture From Serial 
    ${value}=   Read Moisture
    Log     Moisture = ${value}
    Should Be True     ${value} > 200

Check Weight From Serial 
    ${value}=   Read Weight
    Log     Weight = ${value}
    Should Be True     ${value} > 1024

Send Manual Pump Command
    Write Line To Serial    on
    ${line}=    Read Serial Line
    Should Contain      ${line}     PUMP FORCED ON

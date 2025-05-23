*** Settings ***
Library    ../SerialKeywords.py

*** Variables ***
${PORT}         /dev/ttyUSB0
${BAUDRATE}     115200

*** Test Cases ***
Responds To Hello
    Open Serial Connection    ${PORT}    baudrate=${BAUDRATE}
    Sleep    5s
    Write To Serial    hi\r\n
    Sleep    2s
    ${response}=    Read From Serial    timeout=5
    Log    Actual Response: ${response}
    Should Contain    ${response}    Hello from ESP32
    Close Serial Connection

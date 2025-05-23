*** Settings ***
Library    ../libraries/SerialKeywords.py
Library    Process

*** Variables ***
${PORT}         /dev/ttyUSB0
${BAUDRATE}     115200

*** Test Cases ***
Boot Message
    Open Serial Connection    ${PORT}    baudrate=${BAUDRATE}
    Reset ESP32
    Sleep   3s
    ${output}=    Read From Serial
    Log    Actual Boot Message: ${output}
    Should Contain    ${output}    ESP-ROM:esp32s2-rc4-20191025
    Sleep   5s

Send Manual Test Message
    Write To Serial     Hello there\n
    Sleep   1s
    ${debug}=    Read From Serial    timeout=3
    Log    DEBUG RESPONSE: ${debug}

Responds To Manual Override On
    Open Serial Connection      ${PORT}     baudrate=${BAUDRATE}
    Sleep   5s
    Write To Serial    on\r\n
    Sleep    2s
    ${response}=    Read From Serial    timeout=5
    Log    Actual Response: ${response}
    Should Contain    ${response}    Manual override: PUMP FORCED ON
    Close Serial Connection

Responds To Manual Override Off
    Open Serial Connection      ${PORT}     baudrate=${BAUDRATE}
    Sleep   5s
    Write To Serial    off\r\n
    Sleep    2s
    ${response}=    Read From Serial    timeout=5
    Log    Actual Response: ${response}
    Should Contain    ${response}    Manual override: PUMP LOCKED OFF
    Close Serial Connection

Responds to Auto Mode
    Open Serial Connection      ${PORT}     baudrate=${BAUDRATE}
    Sleep   5s
    Write To Serial    active\r\n
    Sleep    2s
    ${response}=    Read From Serial    timeout=5
    Log    Actual Response: ${response}
    Should Contain    ${response}    Resuming automated action
    Close Serial Connection

Pump On From Pin
    Start Process   sudo    python3     ../scripts/pintest.py
    Sleep            5s
    Terminate All Processes

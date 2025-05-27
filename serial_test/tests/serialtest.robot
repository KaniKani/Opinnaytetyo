*** Settings ***
Library    ../SerialKeywords.py

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
    Write To Serial     h\n
    Sleep   1s
    ${debug}=    Read From Serial    timeout=3
    Log    DEBUG RESPONSE: ${debug}

Responds To Hello
    Open Serial Connection      ${PORT}     baudrate=${BAUDRATE}
    Sleep   5s
    Write To Serial    hi\r\n
    Sleep    2s
    ${response}=    Read From Serial    timeout=5
    Log    Actual Response: ${response}
    Should Contain    ${response}    Hello from ESP32
    Close Serial Connection

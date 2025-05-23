#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"

void main() {
    printf("ESP32 READY\n");
    while (1) {
        int c = getchar();
        if (c == 'h') {
            printf("Hello from ESP32\n");
        }
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

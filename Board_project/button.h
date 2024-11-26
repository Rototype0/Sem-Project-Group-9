#pragma once
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/timer.h"

struct gpio_and_type_t
{
    uint gpio;
    bool type;
};


static uint32_t button_mask;
static uint button_count = 0;
static gpio_and_type_t gpios_and_types[32];
static uint pressed_counter[32];
static uint32_t debounce_times[32];
static bool cleared_h[32];
static bool cleared_l[32];

class Button
{
private:
    uint gpio;
    bool type;
    uint pressed_since_last;
    static int64_t Timer_cb_h(alarm_id_t id, void *userdata)
{
    if (gpio_get(((gpio_and_type_t*)userdata)->gpio))
    {
        if (((gpio_and_type_t*)userdata)->type)
        {
            pressed_counter[((gpio_and_type_t*)userdata)->gpio] ++;
        }
        button_mask |= (1<<((gpio_and_type_t*)userdata)->gpio);
    }
    cleared_h[((gpio_and_type_t*)userdata)->gpio] = true;
    return 0;
}
static int64_t Timer_cb_l(alarm_id_t id, void *userdata)
{
    if (!gpio_get(((gpio_and_type_t*)userdata)->gpio))
    {
        if (!((gpio_and_type_t*)userdata)->type)
        {
            pressed_counter[((gpio_and_type_t*)userdata)->gpio] ++;
        }
        button_mask &= !(1<<((gpio_and_type_t*)userdata)->gpio);
    }
    cleared_l[((gpio_and_type_t*)userdata)->gpio] = true;
    return 0;
}
static void Button_press_cb(uint gpio_nr, uint32_t events)
{
    if ((events == GPIO_IRQ_EDGE_RISE) && cleared_h[gpio_nr])
    {
        cleared_h[gpio_nr] = false;
        add_alarm_in_ms(debounce_times[gpio_nr], Timer_cb_h, &(gpios_and_types[gpio_nr]), false);
    }
    if ((events == GPIO_IRQ_EDGE_FALL) && cleared_l[gpio_nr])
    {
        cleared_l[gpio_nr] = false;
        add_alarm_in_ms(debounce_times[gpio_nr], Timer_cb_l, &(gpios_and_types[gpio_nr]), false);
    }
}
public:
    Button(uint gpio_nr, uint32_t debounce_time=50, bool trigger_on_press=true, bool enable=true, bool pull_up=false);
    ~Button();
    void enable();
    void disable();
    bool is_pressed();
    uint pressed_total();
    uint pressed_since_last_check();
};
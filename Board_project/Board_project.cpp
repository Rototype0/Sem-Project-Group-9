#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/timer.h"
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "hardware/i2c.h"
#include "hardware/adc.h"
#include "hardware/pwm.h"
#include "button.h"
#include "display.h"
#include "wav_data.h"

#define deadzone 0x015                               // Deadzone constant potentiometer on adc
#define conversion_factor_V 3.3f / (1 << 12)         // conversion factor for voltage
#define conversion_factor_deg 270.0f / (1 << 12)     // conversion factor for degrees
#define conversion_factor_percent 100.0f / (1 << 12) // conversion factor for percent
#define BUZZER_PIN 20
#define SYS_CLOCK_FREQ 125000000 // 125 MHz

#define SAMPLE_RATE 8000 // 8 kHz sample rate
#define BIT_DEPTH 8      // 8-bit samples

unsigned short song_frequencies[] = {
    440, // A4
    466, // B4
    523, // C5
    440, // A4
    392, // G4
    440, // A4
    329, // E4
    349, // F4
    392, // G4
    440, // A4
    466, // B4
    523, // C5
    440, // A4
    392, // G4
    440, // A4
    329, // E4
    349, // F4
    392, // G4
    440, // A4
    466  // B4
};

// Duration of each note (in milliseconds)
unsigned short note_durations[] = {
    500, // A4
    500, // B4
    500, // C5
    500, // A4
    500, // G4
    500, // A4
    500, // E4
    500, // F4
    500, // G4
    500, // A4
    500, // B4
    500, // C5
    500, // A4
    500, // G4
    500, // A4
    500, // E4
    500, // F4
    500, // G4
    500, // A4
    500  // B4
};

// adc class
class Adc
{
protected:
    uint channel_m; // channel 0-3 for adc
public:
    // initializing adc
    Adc(uint channel, bool first) : channel_m(channel)
    {
        // checking if user input incorrect channel
        if (channel_m < 4)
        {
            // initialize adc first time
            if (first)
            {
                adc_init();
            }
            // switch on channel number to set correct GPIO for corresponding channel
            uint gpio_nr;
            switch (channel_m)
            {
            case 0:
                gpio_nr = 26;
                break;
            case 1:
                gpio_nr = 27;
                break;
            case 2:
                gpio_nr = 28;
                break;
            case 3:
                gpio_nr = 0;
                adc_set_temp_sensor_enabled(true);
                break;
            default:
                break;
            }
            if (gpio_nr)
            {
                gpio_set_dir(gpio_nr, false);
                gpio_disable_pulls(gpio_nr);
                gpio_set_input_enabled(gpio_nr, false);
            }
        }
        else
        {
            printf("Not a valid channel");
        }
    }
    ~Adc()
    {
        // disable temp sensor if it was enabled
        if (channel_m == 3)
        {
            adc_set_temp_sensor_enabled(false);
        }
    }
    // read data from adc
    uint16_t Read()
    {
        adc_select_input(channel_m);
        return adc_read();
    }
};

class Motor
{
protected:
    uint slice_num; // PWM slice for corresponding pin
    uint gpio_m;    // pin
public:
    Motor(uint gpio_nr, uint16_t freq, uint16_t clk_div, uint16_t init_val = 0, bool immidiate = true)
    {
        // your code goes here
    }
    ~Motor()
    {
        disable();
    }
    void enable()
    {
        pwm_set_enabled(slice_num, true);
    }
    void disable()
    {
        pwm_set_enabled(slice_num, false);
    }
};

class Servo_cont : public Motor
{
private:
    float a_m; // gain for conversion
    int b_m;   // bias for conversion
public:
    Servo_cont(uint gpio_nr, float init_speed = 0, uint16_t freq = 50, uint16_t clk_div = 50, float a = 12.5, int b = 3749, bool immidiate = true)
        : Motor(gpio_nr, freq, clk_div, (init_speed * a) + b, immidiate), // call base constructor with correct values
          a_m(a), b_m(b)                                                  // initialize member variables
    {
    }
    void Set_Speed(float speed)
    {
        // clip speed value between -100 and 100
        if (speed > 100)
        {
            speed = 100;
        }
        else if (speed < -100)
        {
            speed = -100;
        }
        // set pwm value
        pwm_set_gpio_level(gpio_m, speed * a_m + b_m);
    }
};

class Servo_angular : public Motor
{
private:
    float range_m; // rotational range for servo
    float a_m;     // gain for conversion
    int b_m;       // bias for conversion
public:
    Servo_angular(uint gpio_nr, float angle = 90, float range = 180, uint16_t freq = 50, uint16_t clk_div = 50, float a = 2500, int b = 2499, bool immidiate = true)
        : Motor(gpio_nr, freq, clk_div, ((angle / range) * a + b), immidiate), // call base constructor with correct values
          range_m(range), a_m(a), b_m(b)                                       // initialize member variables
    {
    }
    void Set_angle(float angle)
    {
        // clip angle between 0 and range
        if (angle < 0)
        {
            angle = 0;
        }
        else if (angle > range_m)
        {
            angle = range_m;
        }
        // set pwm value
        pwm_set_gpio_level(gpio_m, ((angle / range_m) * a_m + b_m));
    }
};

class DC_Motor : public Motor
{
private:
    float mult;

public:
    DC_Motor(uint gpio_nr, float init_speed = 0, uint16_t freq = 2000, uint16_t clk_div = 1, bool immidiate = true)
        : Motor(gpio_nr, freq, clk_div, (((float)init_speed) * ((125000000 / (clk_div * freq) - 1) / 100)), immidiate), // base contructor with correct values
          mult(((125000000 / (clk_div * freq) - 1) / 100))                                                              // initialize gain
    {
    }
    void Set_speed(float speed)
    {
        // clip speed
        if (speed > 100)
        {
            speed = 100;
        }
        else if (speed < -100)
        {
            speed = -100;
        }
        // set pwm
        pwm_set_gpio_level(gpio_m, speed * mult);
    }
};

class Buzzer
{
public:
    // Function to play a single tone
    // void play_tone(int frequency, int duration, int pin)
    // {
    //     // Set the PWM frequency based on the hardcoded system clock frequency
    //     pwm_set_wrap(pin, SYS_CLOCK_FREQ / frequency); // Set the PWM frequency (wrap)

    //     pwm_set_gpio_level(pin, 0x7FFF); // Set the buzzer volume (max value)

    //     sleep_ms(duration); // Play the tone for the specified duration

    //     pwm_set_gpio_level(pin, 0); // Turn off the buzzer after the tone is done
    // }
        void play_wav(uint8_t *data, size_t data_size, uint gpio)
        {
            gpio_set_function(gpio, GPIO_FUNC_PWM);
            uint slice = pwm_gpio_to_slice_num(gpio);

            // Set PWM frequency to match the sample rate
            pwm_set_clkdiv(slice, 1.0f);                      // Set clock divider
            pwm_set_wrap(slice, 125000000 / SAMPLE_RATE - 1); // Set wrap for sample rate
            pwm_set_enabled(slice, true);

            for (size_t i = 0; i < data_size; ++i)
            {
                uint8_t sample = data[i];
                pwm_set_chan_level(slice, pwm_gpio_to_channel(gpio), sample);
                sleep_us(1000000 / SAMPLE_RATE); // Wait for next sample
            }

            pwm_set_enabled(slice, false);
        }
};

class Motor_display : public display
{
public:
    // your code goes here
};

int main()
{
    stdio_init_all();
    stdio_init_all();
    Button input_a(10);//initialize Button
    display oled;//initialize display
    Adc potentiometer(0, true);//initialize adc
    Servo_cont m1(21);//initialize Continous servo class
    Buzzer buzz;
    while (true)
    {
    //  uint32_t result = potentiometer.Read(); // get adc value
    //  if (result < deadzone)                  // check if in deadzone
    //  {
    //      result = 0;
    //  }
    //  float V = result * conversion_factor_V;                                       // convert to V
    //  float degrees = result * conversion_factor_deg;                               // convert to degrees
    //  float percent = result * conversion_factor_percent;                           // convert to percent
    //  oled.clear(false);                                                            // clear display without immediate render
    //  oled._printf(0, false, "Button:");                                            // print line 0 without immediate render
    //  oled._printf(1, false, "State: %d", input_a.is_pressed());                    // print line 1 without immediate render
    //  oled._printf(2, false, "Total: %d", input_a.pressed_total());                 // print line 2 without immediate render
    //  oled._printf(3, false, "Since last: %d", input_a.pressed_since_last_check()); // print line 3 without immediate render
    //  oled._printf(4, false, "ADC:");                                               // print line 4 without immediate render
    //  oled._printf(5, false, "V: %f", V);                                           // print line 5 without immediate render
    //  oled._printf(6, false, "Degrees: %f", degrees);                               // print line 6 without immediate render
    //  oled._printf(7, true, "Percent: %f", percent);                                // print line 7 with immediate render
    //  sleep_ms(100);                                                                // sleep for 3 seconds for a chance to press button multiple times inbetween checks

    oled.clear(false);
    oled._printf(0, true, "Button:");
    buzz.play_wav(wav_data, sizeof(wav_data), BUZZER_PIN);
    tight_loop_contents();  // Keep the program running
    }
}

#ifndef THERMISTANCE_H_

# include <Arduino.h>
#include <math.h>
// reference pour A,B,C,D coef : https://www.vishay.com/en/thermistors/ntc-rt-calculator/
// datasheet : https://www.vishay.com/docs/29049/ntcle100.pdf

class Thermistance
{
    public: 

    uint8_t analog_pin;
    float res;
    float V_ref;
    void init_thermistance(uint8_t pin_number)
    {
        analog_pin = pin_number;
        res = 10000;
        V_ref = 5;
    }
    void change_analog_pin(uint8_t pin_number)
    {
        analog_pin = pin_number;   
    }
    void change_res_value(float value)
    {
        res = value;
    }
    float get_temperature()
    {
        return read_temperatre(analog_pin,res);
    }
    private:
    float A = -14.63371957;
    float B = 4791.84200000;
    float C = -115334.00000000;
    float D = -3730535.00000000;
    float Rref = 10000;
    float read_temperatre(uint8_t pin, float res)
    {
        float temperature = 0;
        int Vout = analogRead(pin);
        float Rtherm = 0;

        float Vout_analogique = (V_ref/1023)*(float)Vout;
        Rtherm = Vout_analogique*res/(V_ref-Vout);
        temperature = A + B*log(Rtherm/Rref)+C*pow(log(Rtherm/Rref),2)+D*pow(log(Rtherm/Rref),3);

        return temperature;
    }


};
    
#endif
    
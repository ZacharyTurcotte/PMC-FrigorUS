#ifndef THERMISTANCE_H_

#include <Arduino.h>
#include <math.h>
// reference pour A,B,C,D coef : https://www.vishay.com/en/thermistors/ntc-rt-calculator/
// datasheet : https://www.vishay.com/docs/29049/ntcle100.pdf
// reference calcul coef : https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html
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

    //float A = 3.354016/1000;
    //float B = 2.569850/10000;
    //float C = 2.620131/1000000;
    //float D = 6.383091/100000000;
    float A = 1.131024546/1000;
    float B = 2.338051738/10000;
    float C = 0;
    float D = 0.8903773352/10000000;
    float Rref = 10000;
    float read_temperatre(uint8_t pin, float res)
    {
        float temperature = 0;
        float Vout = analogRead(pin);
        
        float Rtherm = 0;
        Rtherm = Rref*(1023/Vout-1);
        temperature = 1/(A + B*log(Rtherm)+C*pow(log(Rtherm),2)+D*pow(log(Rtherm),3));

        return temperature-273.15;
    }


};
    
#endif
    
Inverter Counter Readme v79

For Inverter MITSUBISHI
E820S-0030(0.4K)-4
E820S-0050(0.75K)-4
or similar

unstructured readme

mode P.79=3
External buttons: START/STOP
----------------------------------------
faster/slower control P.128=0
PID control P.128=1010
this has to be done only once,
inverter will remember it:
turn dial to set
any freq and press "SET"
F will blink few times and
program will control speed

mode P.79=6
Onboard buttons RUN/STOP (PU mode) or
Enboard buttons START/STOP (EXT mode)
-------------------------------------
PID doesn't work with this mode.
faster/slower control works P.128=0
control needs manual start:
this has to be done every power on:
from PU mode press RUN to start
then press PU/EXT to EXT mode
turn dial to set any freq and press "SET"
F will blink few times and
program will control speed

setup
-----
open cover, to normal run, white switch to "SINK" logic
to temporary disable PLC and inputs, white switch to "SOURCE" logic
to open cover with power lines, AC supply and UVW motor output
place flat screwdriver into "PUSH" hole and carefully lift screwhandle
up, pushing down a plastic holder. Carefully, plastic is fragile.

(all pins activated by connecting to GND)

pin     function    description
---     --------    -----------
SD      GND         (common pin to pull other pins down)
MRS     RUN PLC     (jumper for PLC enabled keep it always connected to SD)
STF     START MOTOR (external button, PLC X0)
RH      STOP MOTOR  (external switch, PLC X2)
RM      DOOR CLOSED (external button, PLC X3)
RL      Counter     (external switch or sensor, PLC X4)

S1      safety1     (jumper to PC 24V)
S2      safety2     (jumper to PC 24V)
PC      24V         (24V 100mA power supply)

schematics
----------

S1  S2  PC  RUN FU  SE
│   │   │
│   └───┤ JUMPER (FACTORY DEFAULT)
├───────┘                             SENSOR
└───────────────────────────────────  RED/BROWN +24V
    ┌───────────────────────────────  BLACK     SIGNAL
    │       ┌───────────────────────  BLUE      GND
    │       │
RL  RM  RH  SD  MRS RES SD  STF STR
│        │   │   │   │   │
│        │   └───┤   └───────────────┐
│        │       │       │            ┫ DOOR  (NO)
│        │       └───────────────────┘
│        │               ├───────────┐
│        │               │            ┫ START (NO)
│        └───────────────────────────┘
│                        └───────────┐
│                                     ┫ STOP  (NO)
└────────────────────────────────────┘


SINK
┌─┐
│▒│ switch position to "SINK"
│ │
└─┘
SOURCE

Inductive sensor XEPRO IPS12-S4NO50-A2P DC 10-30V NPN/open collector,
normally open contact.
When object is approached, sensor makes contact between SIGNAL and GND.

basic parameters
----------------
  P.1150  12000    Number of cycles (initial countdown)
  P.1151  10       measure time every P.1151=10 cycles
  P.1154  5715  ms MIN allowed cycle time for P.1151=10 cycles, E. 16
                   stop if motor runs faster than 3278ms 183rpm
  P.1155  6315  ms MAX allowed cycle time for P.1151=10 cycles, E. 17
                   stop if motor runs slower than 3390ms 177rpm
  P.1156  10       MAX allowed too fast cycles, E. 16
                   stop if motor runs too fast for P.1151*P.1156=30 cycles
  P.1157  10       MAX allowed too slow cycles, E. 17
                   stop if motor runs too slow for P.1151*P.1157=30 cycles
  P.1158  50     s *0.1 MAX allowed run time without cycle sensor signal, E. 18
                   stop if motor runs for P.1158=50*0.1s=5s without sensor signal
  P.1160  0        for countdown < P.1160, allow START add P.1161 to countdown
  P.1161  0        if START is pressed during run, add this value to countdown
  P.1162  0        dial push shows 0:cycle time [ms], 1:too fast/slow error count
  P.1164  1        after power failure 0:stop and counter reset, 1:continue
  P.1165  7700   s stop after P.1160=7700s run time if countdown didn't reach 0


setup for first use
-------------------

reset all parameters (but PLC program will stay)
MODE -> Turn dial anticlockwise -> ALLC -> SET -> 0 
-> rotate change to 1 -> SET -> 1 should blink

when uploading program fails with error PLC response 4406
PLC memory should be cleared with P.414=0 P.498=9696

clear
-----
  ALLC    1        resets most parameters to factory default
  P.414   0        turn PLC OFF
  P.498   9696     PLC flash memory clean (when PLC OFF P.414=0)
                   read P.498 after 9696 to check:
                   P.498=0 successful clear
                   P.498=1 not cleared

set parameters:
--------------
  P.0     4.0   %  torque boost (required to start)
  P.1    50.00  Hz max freq
  P.2    48.00  Hz min freq this is default running freq
  P.7    30.0   s  Acceleration time (required to start)
  P.8     0.5   s  Deceleration time (adjust to park)
  P.9     3.80  A  rated motor current (required to start)
  P.13   40.00  Hz starting frequency (required to start)
  P.14    0        load pattern selection 0:V/f = const 1:V/f^2 = const
  P.15   48.00  Hz freq in "JOG" mode while holding "RUN" button
  P.22    150   %  stall prevention
  P.29    1        s-pattern acceleration/decelration
  P.44   20.0   s  2nd acceleration (RH/RM remote control)
  P.45   20.0   s  2nd deceleration (RH/RM remote control)
  P.59    1        0:multispeed RH/RM/RL, 1:RH/RM faster/slower remembers, 2:faster/slower forgets
  P.60    9        power saving, (required to start)
  P.72    0    kHz 0-default 0.7kHz, 15kHz fastest PWM, "silent" operation
  P.79    6        PU start, PU frequency set, LED PU should turn ON
  P.82    0.00  A  motor excitation current
  P.127  48.00  Hz PID start with linear accelerate to this freq, then switch to PID control
  P.128   0        0:No PID (default), 1010:PID (optional)
  P.156   0        stall prevention P.22 bitmap 0-all enabled 31-all disabled
  P.183   50       MRS input = RUN PLC, LED P.RUN should turn ON now or after P.414
  P.192   9999     ABC relay no function (free to be used by PLC)
  P.251   0        disable output phase loss detection (allow connecting 1-phase motor)
  P.261   1        on power failure, decelerate to stop
  P.277   0        torque limit (current limit) 0-disabled 1-enabled (required to start?)
  P.414   1        PLC enable (doesn't reset by ALLC, LED P.RUN should turn ON, not blink)
  P.571   2      s Holding time at start
  P.609   5        PLC is source of deviation value, write -10000..+10000 to SD1248
  P.610   5        PLC is source of measured value (not used)
  P.675   1        PLC auto-save P.1195-P.1199 PLC D251-D255 at power off
  P.775   42       LED 2nd menu displays countdown value at SD1217 (instead of motor current A)
* P.775   2        LED 2nd menu shows motor current A
  P.776   41       LED 3rd menu displays run time value at SD1218
* P.776   2        LED 3rd menu shows motor current A
  P.801   9999     output limit level (9999-from P.22) others override P.22?
  P.803   1        0-torq constant, 1-torq rising (required to start)
  P.810   0        0-torq limit by parameters, ignore external
  P.816   9999     torq limit acceleration
  P.817   9999     torq limit deceleration
  P.874   400 %    overload shutdown torq OLT limit maximum
  P.888   33       free parameter, parameters version
  P.889   33       free parameter, program version
  P.992   40       when dial pushed LED displays cycle time or too fast/slow counts
  P.1150  12000    D206 Number of cycles (initial countdown)
  P.1151  10       D207 measure time of N cycles
  P.1152  20       D208 control loop feedback 1-strong 1025-weak
  P.1153  6000  ms D209 PID setpoint time ideal for N cycles P.1151=10 6000ms 100rpm D208->D209
  P.1154  5715  ms D210 MIN allowed cycle time for P.1151=10 5715ms 105rpm too fast limit E. 16
  P.1155  6315  ms D211 MAX allowed cycle time for P.1151=10 6315ms  95rpm too slow limit E. 17
  P.1156  10       D212 MAX allowed too fast cycles until STOP E. 16
  P.1157  10       D213 MAX allowed too slow cycles until STOP E. 17
  P.1158  50     s D214 *0.1 MAX allowed run time without cycle sensor signal, STOP E. 18
  P.1159  0        D215 countdown early stop for slow deceleration to end with wanted number of cycles
  P.1160  12000    D216 for countdown < P.1160 allow START to increase countdown
  P.1161  0        D217 if START is pressed during run, add this value to countdown
  P.1162  0        D218 dial push shows 0:N cycle time, 1:too fast/slow error count
  P.1163  1      s D219 *0.1 start button delay time (debounce)
  P.1164  1        D220 after power failure 0:stop and counter reset, 1:continue
  P.1165  2        D221 onboard RUN: 1:EXT mode (EXT button starts), 2:PU mode (onboard RUN starts)
  P.1166  9000     D222 max run time
  P.1167  10     s D223 *0.1 ticks for one time unit (10:second, 600:minute)
  P.1195  0        D251 auto-saved countdown SD1218 at power off, reloaded at power on
  P.1197  0        D253 auto-saved M9 motor on/off state


for PID control set this:

  P.127   48.00 Hz PID start with linear accelerate to this freq, then switch to PID control
  P.128   1010     PID reverse action
  P.1151  10       measure time of 1 cycle (each cycle), D207 in PLC
  P.1153  6000  ms PID setpoint P.1151=1 cycle time          600ms 100rpm ideal
  P.1154  5715  ms MIN allowed  P.1151=1 cycle time PLC D210 571ms 105rpm too fast limit
  P.1155  6315  ms MAX allowed  P.1151=1 cycle time PLC D211 631ms  95rpm too slow limit

explained PID P.128 parameter

  P.128      0     No PID (default for this program)
                   speed control using RH/RM "remote" control from internal PLC
          1010     PID reverse action (can be used with this program)
                   (when deviation is positive, frequency is increased),
                   deviation by P.609, measured value by P.610
          1011     PID forward action (not applicable for this program)
                   (when deviation is positive, frequency is decreased),
                   deviation by P.609, measured value by P.610

troubleshooting
---------------

P.RUN blinking means PLC program error
in this case PLC function does not work.
Unplug USB, power OFF/ON, if P.RUN is
still blinking then PLC program must be
changed.

after setting, disconnect all STF STR MRS
turn inverter OFF, wait until LED panel completely turns OFF
turn back ON

while connected SD+STF, motor should run at 50Hz.
display shows motor frequency in Hz
pressing SET 1x LED should display counter decrementing
pressing SET 2x LED will show run time [s]
pressing SET 3x LED should display again motor frequency [Hz]
hold SET for >3 s to make current LED display mode the power-on default

hold dial pushed, LED should blink and show either
(P.1162=0) cycle time [ms] or
(P.1162=1) cycle errors count in FF.SS format
FF=count of too fast cycles, SS=count of too slow cycles

errors
E. 16  reached max count too fast - check P.1154, P.1156
E. 17  reached max count too slow - check P.1155, P.1157
E. 18  sensor not working         - check P.1158
E. 19  workaround to stop from p.79=6

manual RUN
set P.79 = 0 or 1, only PU LED should turn ON, EXT LED OFF.
press RUN motor should start at 50Hz.
press SET 2x counter should be counting.
press STOP motor should stop, counter should keep last value.

see which parameters have non-default setting
don't know how to actually use this
MODE P.0 -> Rotate left -> Pr.Nd -> SET 1

see simple EXAMPLE https://www.youtube.com/watch?v=FXpdkhMkUdE
right click, debug, force relay set -> shortcut is click and SHIFT-ENTER
device batch monitor, to see and change registers, type SD1148

BOX graphics to copy-paste
─┌┬┐
│├┼┤
─└┴┘

P.79=1 RUN/STOP button starts motor, PLC controls frequency
motor can be stopped by issuing error for example E.19
[MOVP K19 SD1214]

P.79=6 RUN/STOP button starts motor, PLC controls frequency
motor can be stopped by switching from PU to EXT mode
[MOVP K1 SD1143]. Avoid double coiling to Y23.

Usage

unplug USB, rotate dial anti-clockwise until lowest frequency
46.00 Hz is shown, press SET to store frequency to 46Hz and press SET
"F" and "46.00Hz" should alternate blink.
This set frequency is actually the lowest freqency when PLC
controls speed with internal RL/RM. Lowest frequncy in P.2
is not the actual lowest frequency for RL/RM control. 

connect SD+MRS, green LED "P.RUN" should turn ON (not blink)
connect SD+STF, green LED "RUN" should turn ON (not blink)

SET 1x pressed should show counter decrementing
SET 2x pressed should show run time in seconds

when counter reaches value of P.1161, motor decelerates to stop.
Motor can't be stopped immediately, there may be few
additional counts because of deceleration time
this can be fixed with setting non-zero early stop P.1161

Programming information

PLC programming manual
read PLC programming manual section 1.9.2 special relay (SM...)
and section 1.10

special relays and devices

SM1216 ON when motor running
SM400 always ON
SM401 always OFF
SM402 ON one pulse after RUN

SM1200 software control STF
SM1201 software control STR
SM1202 RH
SM1203 RM
SM1204 RL

SM1216 motor running
SM1219 up to frequency (speed reached)
SM1222 output frequency detection

SD520  scan time milliseconds 0-65535
SD521  scan time microseconds *100 0-900
SD1133 output frequency *100
SD1182 feedback pulse (quadrature encoder)
SD1248 PID control deviation -100%..+100% (-10000 .. 10000)

SD1143  write 1 to enter EXT mode (todo example on pulsing Y23)
SD1148  software control bits             0:STF 1:STR 2:RH 3:RM 4:RL
SD1149  software control bits enable mask 0:STF 1:STR 2:RH 3:RM 4:RL
SD1151  inverter status bits 0:RUN 1:FORWARD 2:REVERSE 3:UP TO FREQUENCY ...

SD1215  LED decimal points (for now leave at default)
1.To display SD1216 without decimals
• Set H0000 in SD1215.
• Set "40" in Pr.774.
2.To display SD1216 in 0.1 increment, and SD1218 in 0.001 increment.
• Set H3100 in SD1215.
• Set "40" in Pr.774 and "42" in Pr.776
3.To display SD1217 in 0.1 increment, SD1218 in 1 increment
• Set H0400 in SD1215.
• Set "41" in Pr.774 and "42" in Pr.776
4.To display SD1216 in 0.01 increment
• Set H0300 in SD1215.
• Set "40" in Pr.992

SD1216  LED value P.774-P.776, P.992 = 40
SD1217  LED value P.774-P.776, P.992 = 41
SD1218  LED value P.774-P.776, P.992 = 42

SD1255  1:PLC takes PID control, 0:PLC releases PID control

set debug batch monitor to realtime change special
relays and registers and test them:
testing special registers
4095 -> SM1149
   0 -> SM1255
   1 -> SD1148 (STF) forward 
   2 -> SD1148 (STR) reverse

PID for FR-E800

Set Pr.128 to enable setting of set point/ deviation and measured value for PID control with PLC function
PID operation is performed using the value of SD1248 as the set point/deviation, and the value of SD1249 as the measured
value. The manipulated amount will be stored in SD1250.
To perform first PID control using the PLC function, set "1" in SD1255. When "14" is set in any of Pr.178 to Pr.189 (input
terminal function selection) to assign the X14 signal, turn ON X14 and set "1" in SD1255.
When X14 is not set to the input terminal function selection, start/stop of the operation can be set with bit 0 of SD1255.

TODO
[ ] rotate dial to set number of cycles,
    as quick shortcut to P.1150 setting
[ ] read directly onboard RUN/STOP buttons
[ ] door open safety prevention RM->S1 (after S1 reconnects, is restart programmable?)
[x] show turn time in ms or RPM
[ ] read manual for parameters to allow start directly from power up
    and not need to have 0.1s delay
[x] X0 -> T5 0.1s timer delay to allow start from power on
[x] test timer precision, 30s ok
[ ] test timer 1h precision

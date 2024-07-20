# Mitsubishi E800 inverter PLC counter

Rotation counter with speed regulation
for Mitsubishi E800 inverter with PLC function,
written in ST language code 

After power failure it restarts from
remaining counts.

quick usage:

    start           : Press START
    increase counts : press START while motor is running
    stop            : Press STOP
    reset counter   : Hold STOP for 1 second
    reset speed     : Power OFF, hold STOP, Power ON, release STOP

Demo equipment:

motor    : Končar 3 ~Mot 5AZ 63A-4 0.12 kW = 120 W
reductor : Bonfiglioli VF 44 (30 RPM)

# Durip Raspberry Pi Notes

## 8mosfet Notes
program is in the directory: `/home/admin/8mosfet-rpi`
program name is: `8mosfet`
turn channel on: `8mosfet <id> write <chan> on/off`
Board id is 0
Channel mapping: 6 7 4 3 2 1 8 5 : board       1 2 3 4 5 6 7 8 : board
                 1 2 3 4 5 6 7 8 : address     6 5 4 3 8 1 2 7 : address

SM8mosfet Channel to instrument mapping. CH 1 - 4: 2A/240V, CH 5 - 8: 8A/24V

SM8mosfet Channel	Instrument
CH1			cDAQ
CH2			AML, Seabird TM
CH3			
CH4
CH5			subNero
CH6			FSO
CH7			TX array
CH8			UV lights

DURIP computer static IP address: 169.254.20.100 Mask 255.255.0.0
THOR computer Static IP address: 169.254.20.5 Mask 255.255.255.0
cDAQ Static IP Address eth0: 169.254.20.212 Mask 255.255.0.0
cDAQ Static IP Address eth1 (USB): 169.254.190.91
RaspberryPi Static IP Address: 169.254.20.99 Mask
cDAQ shutdown command: shutdown -h -P now

Set up the RP ip address by:
1. Turn of wifi 169.254.20
2. Find connections advanced settings. Set the ip address under the IPv4 settings
3. Set IP address to 169.254.20.99 (Gateway 169.254.2.98?)
4. The python files are in: /home/admin/Documents/PythonCode

## Power Profile Notes
AML: Powered with 12V, 0.1 Ohm resistor in series, oscilliscope image emailed to gdeane@ucsd.edu. 
External power is 8 to 26 Volts.
Sampling current: 250 mA
Standby: 50 mA
Low power: 60 uA

cDAQ: Powered with cDAQ power supply @ 24V, 0.1 Ohm resistor in series, 'scope image emailed to gdeane@ucsd.edu

subNero: 24V, limit current to 3.5A
Startup current draw: picture emailed to gdeane@ucsd.edu
Transmit current draw: peak currents are 2A. 
IP address: 192.168.42.176 = A   (IP address on hull) and 192.168.42.21 = B


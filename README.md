# IMT-Lab-Durip
All the code and documentation for the Durip Project at the SIO IMT Lab

## Task list

* [DONE] Create a Labview executable that runs on startup

* Automatic upload of Rx files to DURIP computer

* Check contents of binary file. This can be transferred using sftp and Filezilla.

* Install some error checking routines to avoid filling up the disk and transmitting 'improper' waveforms.

* Decide on what acquisition variables are programmable and give the user access to them (sampling rate? gain control?).
 
* Implement transmit and receive scheduling protocols from a configuration file.

* Manual override for immediate transmit.

## Notes

Testbed is going to run. There is an instrument schedule that gets executed, which is loaded onto the Durip computer and downloaded onto the underwater testbed and executed. The files from the instruments are uploaded.

The schedule for each instrument depends on the instrument. 

* AML Water Quality Sensor
* Seabird transmissometer

These instruments give serial data that needs to be logged. The data rate is low. If we run autonomously with batteries, we turn them off. We turn them on at a specified time, and then get the serial data, and then turn them off.

The subnero modems have web servers on them, and we communicate to them via Ethernet. They get turned on, and there are command functions (e.g. transmit and receive data) which are executed at regular intervals. And then the modem gets turned off. This is the same with the FSO. The command functions are currently unknown.

Then there's the cDAQ. It gets turned on, and it transmits files that are specified, and generates files of receieved data, and then it gets turned off.

The nodes are the FSO, cDAQ, subnero, AML, and seabird and these nodes talk to each other. Thus, there needs to be accurate clock calendars and they need to be synchronized.

Let's decide on a scheduling format.
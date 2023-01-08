# SmlParserLight
[MicroPython](https://micropython.org/) compatible parser for the SML (Smart Message Language) protocol

# The Challenge

Starting point was to integrate the reading of a smart meter into the home automation iot network.

The infrastructure mosquitto MQTT server and node-red for visualization is already setup.
Not wanting to spend a full Raspberry Pi to "just" read the SML messages and send them via MQTT
lead to implementing the required on a MicroPython compatible hardware (e.g. ESP32, Raspberry Pi Pico W, ...)

There are quite a few projects out there providing support for SML, but unfortunately they cannot be run on the 
reduced functionality of MicroPython.

# The Inspiration

* Good entry point is the [Volkszähler](https://volkszaehler.org/) project (German)

* Full spec [Technische Richtlinie BSI TR-03109-1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR03109/TR-03109-1_Anlage_Feinspezifikation_Drahtgebundene_LMN-Schnittstelle_Teilb.pdf?__blob=publicationFile)
 (German)

* List of [OBIS codes](https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm)

* Deconstruction of the protocol with the setup of the [SML IR interface](https://www.stefan-weigert.de/php_loader/sml.php) (Gernam)
This helped a lot to understand the protocol.

This python script is in fact a light version of [smllib](https://github.com/spacemanspiff2007/SmlLib).
Removing a lot of functionality (and convenience) to be able to run it on micropython.

Use the smllib to analyse the raw messages from your eMeter to extract the available OBIS codes.

# The Script

The scrip fulfills two tasks.

1) Accumulate bytes read from UART to extract full frames from the stream. 
   The validity the is checked based on the CRC signature.
2) Once a frame is returned by get_frame() the entries can be extracted by using the
   sml_get_entry() function.

The entry contains all 7 components, (None is they are not set)

# The Usage

The example_usage.py shows how to use the parser.
For the full setup the data shall be fed from the UART attached to the SML IR interface.











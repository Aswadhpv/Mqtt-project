# Mqtt-project

i have used mosquito mqtt broker

and after put socat -u UDP-LISTEN:<udp server port>,fork OPEN:received_messages.txt,creat,append
where udp server port is based on your systems.
This command will listen on the specified UDP port and save received messages to 'received_messages.txt'.
------------------------------------------------------------------------------------------------------
updated according to the requirements
------------------------------------------------------------------------------------------------------
1.Logging: Implemented logging using the Python logging module. Errors related to external processes (mqtt, network subsystem, volume control) are logged with appropriate error messages. The logger object is used to log messages with timestamps, logging levels, and subsystem names.
2.Crash Resistance: Exception handling is added around the external process calls (adjusting volume, sending UDP messages) to catch and log any errors that might occur. If MQTT communication is lost during operation, the on_disconnect callback is triggered, and a warning message is logged.
3.Synchronous Interaction: In the synchronous interaction scenario, delays in volume control could lead to interruptions in the UDP data stream. However, the code provided does not introduce any delays in volume control or UDP message sending. If there are specific timing requirements, additional logic may be needed to ensure timely processing of messages.
4. Meaningful Names: Variables, functions, and files are named descriptively to convey their purpose and functionality. For example, meaningful names like adjust_volume, send_udp_message, mqtt_broker_address, etc., are used throughout the code.

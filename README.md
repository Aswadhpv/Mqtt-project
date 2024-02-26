# Mqtt-project

i have used mosquito mqtt broker

and after put socat -u UDP-LISTEN:<udp server port>,fork OPEN:received_messages.txt,creat,append
where udp server port is based on your systems.
This command will listen on the specified UDP port and save received messages to 'received_messages.txt'.

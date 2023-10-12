"""
THIS ONE WORKS
"""

import pynmea2

def calculate_checksum(sentence):
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return '{:02X}'.format(checksum)

file = open('src/sensors/mock.log', encoding='utf-8')

for line in file.readlines():
    try:
        # Extract the characters between '$' and '*'
        sentence = line[line.find('$')+1:line.find('*')]
        print(sentence)
        
        # Calculate the correct checksum
        calculated_checksum = calculate_checksum(sentence)
        print(calculated_checksum)
        
        # Extract the provided checksum in the sentence
        provided_checksum = int(line[line.find('*')+1:line.find('*')+3], 16)
        print(provided_checksum)
        
        # If the calculated checksum doesn't match the provided checksum, replace it
        if calculated_checksum != provided_checksum:
            line = line.replace('*' + line[line.find('*')+1:line.find('*')+3], '*' + calculated_checksum)
        
        # Parse the sentence
        msg = pynmea2.parse(line)
        print(repr(msg))
        print (msg.latitude)
        print (msg.longitude)
        print (msg.spd_over_grnd)
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
    except ValueError:
        print('Invalid checksum in the sentence.')
    continue

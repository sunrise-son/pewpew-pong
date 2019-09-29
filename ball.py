import serial
import time


ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=900,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
#ser.write(chr(2).encode())
#ser.write(chr(2).encode())
print('GO')

pos = [1, 1]
direction = [1, 0.5]

for i in range(1, 7):
    for j in range(8):
        ser.write('screen.pixel({}, {}, 0)\r\n'.format(i, j).encode())

c = 0
game_over = False

while True:
    print('screen.pixel({}, {}, 0)\r\n'.format(pos[0], int(pos[1])))
    ser.write('screen.pixel({}, {}, 0)\r\n'.format(pos[0], int(pos[1])).encode())
    last_pos1 = pos[1]

    pos[0] += direction[0]
    pos[1] += direction[1]

    #if pos[1] in (0, 7):
    if (pos[1] <= 1 and last_pos1 > 1) or (pos[1] >= 7 and last_pos1 < 7):
        direction[1] *= -1
        
    if pos[0] in (0, 7):
        direction[0] *= -1

        with open('/tmp/pos' + str(int(pos[0]/7))) as opened:
            paddle_pos = int(opened.read())

        if int(pos[1]) < paddle_pos or int(pos[1]) > paddle_pos + 2:
            game_over = True


    print('screen.pixel({}, {}, 2)\r\n'.format(pos[0], int(pos[1])))
    ser.write('screen.pixel({}, {}, 3)\r\n'.format(pos[0], int(pos[1])).encode())
    ser.write(b'pew.show(screen)\r\n')
    time.sleep(0.25)
    c += 1
    print(pos, c)

    if game_over:
        for i in range(8):
            for j in range(8):
                ser.write('screen.pixel({}, {}, 0)\r\n'.format(i, j).encode())
        if pos[0] > 3:
            ser.write(b'screen.pixel(2, 2, 3)\r\n')
            ser.write(b'screen.pixel(2, 3, 3)\r\n')
            ser.write(b'screen.pixel(2, 4, 3)\r\n')
            ser.write(b'screen.pixel(2, 5, 3)\r\n')
            ser.write(b'screen.pixel(3, 5, 3)\r\n')
            ser.write(b'screen.pixel(4, 5, 3)\r\n')
        else:
            ser.write(b'screen.pixel(2, 2, 3)\r\n')
            ser.write(b'screen.pixel(2, 3, 3)\r\n')
            ser.write(b'screen.pixel(2, 4, 3)\r\n')
            ser.write(b'screen.pixel(2, 5, 3)\r\n')
            ser.write(b'screen.pixel(3, 2, 3)\r\n')
            ser.write(b'screen.pixel(3, 3, 3)\r\n')
            ser.write(b'screen.pixel(4, 2, 3)\r\n')
            ser.write(b'screen.pixel(4, 3, 3)\r\n')
            ser.write(b'screen.pixel(3, 4, 3)\r\n')
            ser.write(b'screen.pixel(4, 5, 3)\r\n')
            
        ser.write(b'pew.show(screen)\r\n')
        break 

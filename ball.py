import serial
import time

SERIAL_PORT = '/dev/ttyACM0'


ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=900,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

L_winner_shape = (
    (2, 2), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5)
)

R_winner_shape = (
    (2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (4, 2), (4, 3), (3, 4), (4, 5), 
)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_int(self):
        return self.__class__(int(self.x), int(self.y))


def init_session():
    ser.write(chr(2).encode())
    ser.write(chr(10).encode())


def ser_write(code):
    ser.write(f'{code}\r\n'.encode())


def pixel(pos, color):    
    pos = pos.as_int()
    ser_write(f'screen.pixel({pos.x}, {pos.y}, {color})')


def show():
    ser_write('pew.show(screen)')


def draw_shape(shape, color):
    for pix in shape:
        pixel(pix[0], pix[1], color)
    show()


def clear_screen():
    for i in range(8):
        for j in range(8):
            pixel(i, j, 0)
    show()


if __name__ == '__main__':
    
    # The initial position of the ball
    pos = Vector(1, 1)

    # The initial move direction of the ball
    # The idea is to take X steps by integers and Y by floats
    direction = Vector(1, 0.5)

    game_over = False

    # When you kick off the match the device is typically already initiated
    init_session()

    clear_screen()

    # Let's loop until we check that the game is over
    while not game_over:
        
        # Clear the last ball position
        pixel(pos, 0)

        # We need to save this value to calculate bouncing
        last_pos_y = pos.y

        # Take a step
        pos.x += direction.x
        pos.y += direction.y

        # Bounce if close to the top or bottom edge
        if (pos.y <= 1 and last_pos_y > 1) or (pos.y >= 7 and last_pos_y < 7):
            direction.y *= -1

        # Bounce if close to the left or right edge
        if pos.as_int().x in (0, 7):
            direction.x *= -1

            # Read the current paddle position (provided by the django app)
            with open('/tmp/pos' + str(int(pos.y/7))) as opened:
                paddle_pos = int(opened.read())

            # If paddle was not present on the ball position, it's over
            if int(pos.y) < paddle_pos or int(pos.y) > paddle_pos + 2:
                game_over = True

        # Draw new ball position
        pixel(pos, 0)
        show()

        # Interval between the ball steps
        time.sleep(0.25)


    # Draw the winner letter on the screen ([L]eft or [R]ight)
    clear_screen()
    if pos.x > 3:
        draw_shape(L_winner_shape)
    else:
        draw_shape(R_winner_shape)

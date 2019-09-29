from django.http import HttpResponse
from django.conf import settings

ser = settings.SER
pixels = settings.PIXELS


def index1(request):
    ser.write('screen.pixel({}, {}, 1)\r\n'.format(*pixels[0]).encode())
    ser.write(b'pew.show(screen)\r\n')
    return HttpResponse('''
        <script>
            function move(slug) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/' + slug);
                xhr.send();
            }
        </script>
        <h1>Welcome</h1>
        <button onclick="move('left_up')" style="font-size: 72">&nbsp;&nbsp;UP&nbsp;&nbsp;</button>
        <button onclick="move('left_down')" style="font-size: 72">DOWN</button>
    ''')

def index2(request):
    ser.write('screen.pixel({}, {}, 1)\r\n'.format(*pixels[0]).encode())
    ser.write(b'pew.show(screen)\r\n')
    return HttpResponse('''
        <script>
            function move(slug) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/' + slug);
                xhr.send();
            }
        </script>
        <h1>Welcome</h1>
        <button onclick="move('right_up')" style="font-size: 72">&nbsp;&nbsp;UP&nbsp;&nbsp;</button>
        <button onclick="move('right_down')" style="font-size: 72">DOWN</button>
    ''')

def move_left_up(request):
    return _move(request, 0, -1)

def move_left_down(request):
    return _move(request, 0, 1)

def move_right_up(request):
    return _move(request, 1, -1)

def move_right_down(request):
    return _move(request, 1, 1)

def _move(request, side, direction):
    for i in range(3):
        ser.write('screen.pixel({}, {}, 0)\r\n'.format(pixels[side][0], pixels[side][1]+i).encode())
    pixels[side][1] = (pixels[side][1] + direction) % 8
    for i in range(3):
        ser.write('screen.pixel({}, {}, 1)\r\n'.format(pixels[side][0], pixels[side][1]+i).encode())
    ser.write(b'pew.show(screen)\r\n')
    print(pixels)
    with open('/tmp/pos' + str(side), 'w') as opened:
        opened.write(str(pixels[side][1]))
    return HttpResponse('')

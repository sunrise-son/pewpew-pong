from django.http import HttpResponse
from django.conf import settings

ser = settings.SER
pixels = settings.PIXELS


def index1(request):
    return HttpResponse(_index_template('left'))


def index2(request):
    return HttpResponse(_index_template('right'))


def _index_template(side):
    return f'''
        <script>
            function move(slug) {{
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/' + slug);
                xhr.send();
            }}
        </script>
        <h1>Welcome player {side}</h1>
        <button onclick="move('{side}_up')" style="font-size: 72">&nbsp;&nbsp;UP&nbsp;&nbsp;</button>
        <button onclick="move('{side}_down')" style="font-size: 72">DOWN</button>
    '''


def move_left_up(request):
    return _move(request, 0, -1)


def move_left_down(request):
    return _move(request, 0, 1)


def move_right_up(request):
    return _move(request, 1, -1)


def move_right_down(request):
    return _move(request, 1, 1)


def _move(request, side, direction):
    _draw_paddle(side, 0)
    pixels[side][1] = (pixels[side][1] + direction) % 8
    _draw_paddle(side, 1)
    ser.write(b'pew.show(screen)\r\n')

    with open('/tmp/pos' + str(side), 'w') as opened:
        opened.write(str(pixels[side][1]))
    return HttpResponse('')


def _draw_paddle(side, color):
    for i in range(3):
        ser.write('screen.pixel({}, {}, {})\r\n'.format(pixels[side][0], pixels[side][1]+i, color).encode())

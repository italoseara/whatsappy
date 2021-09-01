import qrcode
import colorama

colorama.init()


def draw(str,version=1):
    white_block = '\033[0;0;47m  '
    black_block = '\033[0;0;48m  '
    new_line = '\033[m\n'

    qr = qrcode.QRCode(version)
    qr.add_data(str)
    qr.make()
    output = white_block*(qr.modules_count+2) + new_line
    for mn in qr.modules:
        output += white_block
        for m in mn:
            if m:
                output += black_block
            else:
                output += white_block
        output += white_block + new_line
    output += white_block*(qr.modules_count+2) + new_line
    return output

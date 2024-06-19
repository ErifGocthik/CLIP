from cloudapp.models import Design


def get_style(request):
    file = Design.objects.get(pk=2).file.path
    file = (open(file, 'r').read()).split('\n')
    return {
        'text': file[0].split(':')[1],
        'background': file[1].split(':')[1],
        'animation': file[2].split(':')[1],
        'icons': file[3].split(':')[1],
        'general_color': file[4].split(':')[1],
        'card_bg': file[5].split(':')[1],
        'btn_clr': file[6].split(':')[1]
            }
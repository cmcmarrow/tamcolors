# tamcolors libraries
from tamcolors import tam_io
from . import tam_film


"""
tam fade in fades in a buffer
can be reversed 
"""


def tam_fade_in(buffer,
                char,
                foreground_color,
                background_color,
                rand=(True, False, False, False, False),
                reverse=False):

    """
    info: makes a fade in or fade out via TAMFilm
    :param buffer: TAMBuffer
    :param char: single block char
    :param foreground_color: Color
    :param background_color: Color
    :param rand: list: [True, bool, bool, bool, ...]
    :param reverse: bool
    :return: TAMFilm
    """
    frames = []

    start_pool = []
    for y in range(buffer.get_dimensions()[1]):
        for x in range(buffer.get_dimensions()[0]):
            start_pool.append((x, y, *buffer.get_spot(x, y)))

    char_pool = []
    foreground_pool = []
    background_pool = []
    done_pool = []

    while any((len(start_pool), len(char_pool), len(foreground_pool), len(background_pool))):
        new_frame = tam_io.tam_buffer.TAMBuffer(*buffer.get_dimensions(), char, foreground_color, background_color)

        for pixel in done_pool:
            new_frame.set_spot(*pixel)

        for count, pools in enumerate(((background_pool, done_pool),
                                       (foreground_pool, background_pool),
                                       (char_pool, foreground_pool))):

            for spot, pixel in enumerate(pools[0]):
                if rand[spot % len(rand)]:
                    if count == 0:
                        new_frame.set_spot(*pixel[:3], foreground_color, background_color)
                    elif count == 1:
                        new_frame.set_spot(*pixel[:4], background_color)
                    else:
                        new_frame.set_spot(*pixel)

                    pools[0].remove(pixel)
                    pools[1].append(pixel)
                else:
                    if count == 0:
                        new_frame.set_spot(*pixel[:3], foreground_color, background_color)
                    elif count == 1:
                        new_frame.set_spot(*pixel[:4], background_color)
                    else:
                        new_frame.set_spot(*pixel)

        for spot, pixel in enumerate(start_pool.copy()):
            if rand[spot % len(rand)]:
                char_pool.append(pixel)
                start_pool.remove(pixel)

        frames.append(new_frame)

    if len(frames) == 0:
        frames.append(buffer.copy())
    elif frames[-1] != buffer:
        frames.append(buffer.copy())

    if reverse:
        frames.reverse()

    return tam_film.TAMFilm(frames)

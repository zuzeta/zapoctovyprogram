from procesnik import Board, pytaj_se
from pynput import keyboard

def procesnik():
    print(b)
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress = True) as listener:
        listener.join()

def on_press(key):
    b.refresh()
"""spojenie vstupu od klavesnice spolu s pohybmi v hre"""

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    elif key == keyboard.Key.up:
        b.board, b.prazdne_miesto = b.move_up(b.board, b.prazdne_miesto)
    elif key == keyboard.Key.right:
        b.board, b.prazdne_miesto = b.move_right(b.board, b.prazdne_miesto)
    elif key == keyboard.Key.down:
        b.board, b.prazdne_miesto = b.move_down(b.board, b.prazdne_miesto)
    elif key == keyboard.Key.left:
        b.board, b.prazdne_miesto = b.move_left(b.board, b.prazdne_miesto)
    elif key == keyboard.Key.space:
        print("minutku...")
        moves = b.solve()
        m = moves[0]
        b.moves[m](b.board, b.prazdne_miesto)
    """obnovuje obrazovku, dokial nie je hra vyriesena"""
    isSolved = b.refresh()
    return not isSolved

if __name__ == "__main__":
    while True:
        mam_vygenerovat_tabulku, shuffle_magnitude, n, riadky, stlpce = pytaj_se()
        b = Board(mam_vygenerovat_tabulku, shuffle_magnitude, n, riadky, stlpce)
        if b.isSolvable:
            b.shuffle()
            procesnik()
        input()

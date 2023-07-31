
import global_constants
import chess
import bad_chess
import chess_los_alamos
import circle_chess
import dark_chess
import frozen_chess
import garner
import gekso_chess
import haotic
import kamikaze
import magic_play
import nuclear_chess
import rasing
import schatranj
import week_chess
import legan_chess
import sovereign_chess
import uprising
import jungles_chess



def find_chess_module(tip):
    if tip in ['classic', 'fisher', 'horse_battle', 'permutation', 'horde', 'inverse']:
        return chess
    elif tip == 'los_alamos':
        return chess_los_alamos
    elif tip in ['circle_chess', 'bizantion']:
        return circle_chess
    elif tip in ['glinskiy', 'kuej']:
        return gekso_chess
    elif tip == 'garner':
        return garner
    elif tip == 'week':
        return week_chess
    elif tip == 'magik':
        return magic_play
    elif tip == 'kamikadze':
        return kamikaze
    elif tip == 'bad_chess':
        return bad_chess
    elif tip == 'rasing':
        return rasing
    elif tip == 'haotic':
        return haotic
    elif tip == 'schatranj':
        return schatranj
    elif tip == 'dark_chess':
        return dark_chess
    elif tip == 'frozen':
        return frozen_chess
    elif tip == 'nuclear':
        return nuclear_chess
    elif tip == 'legan':
        return legan_chess
    elif tip == 'sovereign':
        return sovereign_chess
    elif tip == 'uprising':
        return uprising
    elif tip == 'jungles':
        return jungles_chess
    if global_constants.game.test:
        print()
        print('you tryes to run undefined chess type!!!!!!')
        print('file main.py def find_chess_module')
        print()
    quit()








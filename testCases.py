# -*- coding: utf8 -*-
from draughtsFunctions import *
import sys
import unittest
import inspect

# Raw check to restrict copy-past code


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.dim = 10
        self.board = initBoard(self.dim)
        self.referrer = initBoard(self.dim)
        self.whiteList = [	(0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
                           (1, 1), (1, 3), (1, 5), (1, 7), (1, 9),
                           (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
                           (3, 1), (3, 3), (3, 5), (3, 7), (3, 9),
                           (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
                           (5, 1), (5, 3), (5, 5), (5, 7), (5, 9),
                           (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
                           (7, 1), (7, 3), (7, 5), (7, 7), (7, 9),
                           (8, 0), (8, 2), (8, 4), (8, 6), (8, 8),
                           (9, 1), (9, 3), (9,
                           5), (9, 7), (9, 9)
                           ]
        self.blackList = []
        for row in range(self.dim):
            for col in range(self.dim):
                self.blackList.append((row, col))
        for elem in self.whiteList:
            self.blackList.remove(elem)
    #
    #

    def test_signatures(self):
        sig = inspect.getargspec(movePiece)
        self.assertTrue(self.checkSignature(
            sig, 5, (1,)), "Bad signature for \"movePiece\" method")
        #
        sig = inspect.getargspec(checkEndOfGame)
        self.assertTrue(self.checkSignature(
            sig, 2), "Bad signature for \"checkEndOfGame\" method")
        #
        sig = inspect.getargspec(checkMove)
        self.assertTrue(self.checkSignature(sig, 8, (
            1, False, False)), "Bad signature for \"checkMove\" method")
        #
        sig = inspect.getargspec(becomeKing)
        self.assertTrue(self.checkSignature(
            sig, 3), "Bad signature for \"becomeKing\" method")
        #
        sig = inspect.getargspec(initBoard)
        self.assertTrue(self.checkSignature(
            sig, 1), "Bad signature for \"initBoard\" method")
        #
        sig = inspect.getargspec(capture)
        self.assertTrue(self.checkSignature(
            sig, 3), "Bad signature for \"capture\" method")
        #
        sig = inspect.getargspec(countFree)
        self.assertTrue(self.checkSignature(
            sig, 6, (None, 0)), "Bad signature for \"countFree\" method")
    #
    #

    def test_initBoard(self):
        center = int(self.dim / 2)
        for dim in (5, self.dim):
            board = initBoard(dim)
            #
            squarre = True
            for row in range(dim):
                if(len(board[row]) != dim):
                    squarre = False
            self.assertTrue(squarre, "initBoard must generate a square array")
        #
        centerIsEmpty = True
        for col in range(self.dim):
            if(self.board[center - 1][col] != self.board[center][col] or self.board[center][col] != FREE_SPACE):
                centerIsEmpty = False
        self.assertTrue(centerIsEmpty, "initBoard must generate a square array with empty center lines")
        #
        whiteSpacesAreFree = True
        for x, y in self.whiteList:
            if(self.board[x][y] != FREE_SPACE):
                whiteSpacesAreFree = False
        self.assertTrue(whiteSpacesAreFree, "initBoard must generate a square array with no piece on white spaces")
        #
        simplePieceFillPlayersSide = True
        for x, y in list(filter(lambda pos: (pos[0] > center or pos[0] < center - 1), self.blackList)):
            color = WHITE_PLAYER if(x > center)else BLACK_PLAYER
            if(self.board[x][y] != color):
                simplePieceFillPlayersSide = False
        self.assertTrue(simplePieceFillPlayersSide, "initBoard must place only simple piece and on the right side")
    #
    #

    def test_capture(self):
        center = int(self.dim / 2)
        center = (center, center - 1)
        captureCenter = True
        for y, x in list(filter(lambda pos: (pos[0] in center), self.blackList)):
            self.board[y][x] = 2
            capture(self.board, y, x)
            if(self.board[y][x] != FREE_SPACE):
                captureCenter = False
            self.board[y][x] = FREE_SPACE
            self.checkSideEffect()
        positionedPiece = True
        for y, x in list(filter(lambda pos: (pos[0] not in center), self.blackList)):
            backup = self.board[y][x]
            capture(self.board, y, x)
            if(self.board[y][x] != FREE_SPACE):
                positionedPiece = False
            self.board[y][x] = backup
            self.checkSideEffect()
        self.assertTrue(captureCenter, "Cannot capture piece on center lines")
        self.assertTrue(positionedPiece, "Cannot capture piece")
    #
    #

    def test_countFree(self):
        tmpBoard = self.createEmptyBoard()
        row, col = 4, 5
        tmpBoard[row][col] = WHITE_PLAYER
        directions = ['L', 'R', 'LB', 'RB']
        results = [True, True, True, True]
        blackList = [	[(1, 2), (1, 8), (7, 2), (7, 8)],
                      [(2, 3),
                       (2, 7), (6, 3), (6, 7)],
                      [(3, 4),
                       (3, 6), (5, 4), (5, 6)],
                      [(9, 0)]]
        lengths = [2, 1, 0, 4]
        for index in range(len(lengths)):
            length = lengths[index]
            for y, x in blackList[index]:
                tmpBoard[y][x] = BLACK_PLAYER
            for direction in directions:
                if(countFree(tmpBoard, row, col, direction) != length):
                    results[index] = False
            for y, x in blackList[index]:
                tmpBoard[y][x] = FREE_SPACE
            self.assertTrue(results[index], (
                "Mishandling of " + str(length) + "-free spaces"))
    #
    #

    def test_movePiece(self):
        x, y = self.humanToIndices('d', 7)
        (toY, toX), cap = movePiece(self.board, y, x, 'R', 1)
        self.assertTrue((
            toY, toX) == (5, 4), "Mishandling of movePiece (bad destination)")
        self.assertTrue(
            cap == None, "Mishandling of movePiece (no capture occured)")
        self.assertTrue(self.board[6][3] == FREE_SPACE and self.board[
                        5][4] == WHITE_PLAYER, "Mishandling of movePiece")
        self.board[toY][toX] *= 2
        movePiece(self.board, toY, toX, 'LB', 1)
        self.board[y][x] /= 2
        self.checkSideEffect()
        advX, advY = self.humanToIndices('e', 6)
        self.board[advY][advX] = BLACK_PLAYER
        (toY, toX), cap = movePiece(self.board, y, x, 'R', 1)
        self.assertTrue(
            cap == (5, 4), "Mishandling of movePiece (capture not found)")
    #
    #

    def test_becomeKing(self):
        rows = (0, self.dim - 1)
        for y, x in list(filter(lambda pos: (pos[0] in rows), self.blackList)):
            self.board[y][x] = self.board[y][x] * -1
        kingsValue, kingsSign = True, True
        for y, x in self.blackList:
            becomeKing(self.board, y, x)
        for color, row in [(WHITE_PLAYER, 0), (BLACK_PLAYER, self.dim - 1)]:
            for y, x in list(filter(lambda pos: (pos[0] == row), self.blackList)):
                sign = -1 if(self.board[y][x] < 0) else (
                    1 if(self.board[y][x] > 0) else 0)
                if(abs(self.board[y][x]) < 2):
                    kingsValue = False
                if(sign != color):
                    kingsSign = False
                self.board[y][x] = color * -1
        self.assertTrue(kingsValue, "The value of kings must be incremented")
        self.assertTrue(kingsSign, "The king sign must be unchanged")
        self.checkSideEffect()
    #
    #

    def test_checkMove(self):
        tests = [	('NO_PIECE', [('i', 7, 'L', 1)]),
                  ('CANNOT_GO_OUTSIDE',
                  [('j', 7, 'R', 1)]),
                  (
                  'NO_ERROR', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1)
                  ]),
                  (
                  'PAWN_ONLY_ONE_MOVE', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('d', 5, 'L', 2)
                  ]),
                  ('BAD_DIRECTION_FORMAT',
                  [('j', 7, 'C', 1)]),
                  ('BAD_DIRECTION_FORMAT',
                  [('j', 7, 'CD', 1)]),
                  ('BAD_DIRECTION_FORMAT',
                  [('j', 7, 'LD', 1)]),
                  ('BAD_DIRECTION_FORMAT',
                  [('j', 7, 'CB', 1)]),
                  (
                  'ONLY_KING_GO_BACK', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('b', 5, 'RB', 1)
                  ]),
                  (
                  'CANNOT_JUMP_OUTSIDE', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('i', 4, 'L', 1)
                  ]),
                  ('SPACE_OCCUPIED', [('g', 8, 'R', 1)]),
                  (
                  'TOO_LONG_JUMP', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('d', 1, 'R', 1), (
                          'i', 8, 'R', 1), ('b', 3, 'R', 1), ('j', 9, 'L', 1),
                      ('d', 5, 'L', 1), ('c', 6,
                  'R', 1), ('g', 4, 'L', 1),
                      ('d', 5, 'L', 1), (
                          'b', 3, 'R', 1),  # make king
                      ('d', 3,
                  'L', 1), ('d', 1, 'RB', 1)
                  ]),
                  (
                  'NO_FREE_WAY', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('d', 1, 'R', 1), (
                          'i', 8, 'R', 1), ('b', 3, 'R', 1), ('j', 9, 'L', 1),
                      ('d', 5, 'L', 1), ('c', 6,
                  'R', 1), ('g', 4, 'L', 1),
                      ('d', 5, 'L', 1), (
                          'b', 3, 'R', 1),  # make king
                      ('d', 3, 'L', 1), ('a', 8,
                  'R', 1), ('e', 4, 'R', 1),
                      ('b', 7,
                  'L', 1), ('f', 3, 'R', 1),
                      ('d', 1, 'RB', 2)
                  ]),
                  ('OPPONENT_PIECE', [('i', 4, 'R', 1)]),
                  (
                  'MUST_CAPTURE', [('b', 7, 'R', 1), ('a', 4, 'L', 1), ('j', 7, 'L', 1),
                  ('e', 4, 'L', 1), (
                      'i', 6, 'R', 1), ('d', 3, 'L', 1), ('h', 7, 'R', 1),
                      ('c', 2, 'L', 1), (
                          'i', 6, 'L', 1), ('e', 4, 'R', 1), ('f', 7, 'R', 1),
                      ('d', 1, 'R', 1), (
                          'i', 8, 'R', 1), ('b', 3, 'R', 1), ('j', 9, 'L', 1),
                      ('d', 5, 'L', 1), ('c', 6, 'R',
                  1), ('b', 5, 'R', 1), ('d', 5, 'RB', 1),
                      ('f', 7, 'L', 1),
                  ])
                  ]
        for test in tests:
            final, moves = test
            last = moves.pop()
            success = True
            board = initBoard(10)
            hasPlayer = False
            hasCaptured = False
            previous = None
            for x, y, direction, length in moves:
                x, y = self.humanToIndices(x, y)

                if((y, x) == previous):
                    hasPlayer = True
                else:
                    hasPlayer = hasCaptured = False
                player = self.color(board[y][x])
                res = checkMove(board, y, x, direction,
                                player, length, hasPlayer, hasCaptured)
                if(res == NO_ERROR):
                    (y, x), cap = movePiece(board, y, x, direction, length)
                    previous = (y, x)
                    if(cap != None):
                        capY, capX = cap
                        capture(board, capY, capX)
                        hasCaptured = True
                    becomeKing(board, y, x)
                else:
                    success = False
            if(success):
                x, y, direction, length = last
                x, y = self.humanToIndices(x, y)
                if((y, x) == previous):
                    hasPlayer = True
                else:
                    hasPlayer = hasCaptured = False
                player = self.color(board[y][x])
                if(eval(final) == OPPONENT_PIECE):
                    player = -player
                success = checkMove(board, y, x, direction, player, length,
                                    hasPlayer, hasCaptured) == eval(final)
                self.assertTrue(
                    success, "Mishandling of the error code : " + final)
            else:
                self.assertTrue(success, "Mishandling in a sequence of moves to generate the error code : " + final)
    #
    #

    def test_checkEndOfGame(self):
        board = initBoard(10)
        #
        res = checkEndOfGame(board, WHITE_PLAYER)
        self.assertTrue(isinstance(res, bool) and (not res), "Mishandling of checkEndOfGame when not finished for White turn")
        res = checkEndOfGame(board, BLACK_PLAYER)
        self.assertTrue(isinstance(res, bool) and (not res), "Mishandling of checkEndOfGame when not finished for Black turn")
        #
        for y, x in list(filter(lambda pos: (board[pos[0]][pos[1]] == WHITE_PLAYER), self.blackList)):
            board[y][x] = FREE_SPACE
        res = checkEndOfGame(board, WHITE_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == BLACK_PLAYER), "Mishandling of checkEndOfGame when Black must win for White turn")
        res = checkEndOfGame(board, BLACK_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == BLACK_PLAYER), "Mishandling of checkEndOfGame when Black must win for Black turn")
        #
        board = initBoard(10)
        for y, x in list(filter(lambda pos: (board[pos[0]][pos[1]] == BLACK_PLAYER), self.blackList)):
            board[y][x] = FREE_SPACE
        res = checkEndOfGame(board, WHITE_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == WHITE_PLAYER), "Mishandling of checkEndOfGame when White must win for White turn")
        res = checkEndOfGame(board, BLACK_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == WHITE_PLAYER), "Mishandling of checkEndOfGame when White must win for Black turn")
        #
        board = initBoard(10)
        for y, x in list(filter(lambda pos: (board[pos[0]][pos[1]] == FREE_SPACE), self.blackList)):
            board[y][x] = BLACK_PLAYER
        res = checkEndOfGame(board, WHITE_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == 0), "Mishandling of checkEndOfGame when null party for White turn")
        res = checkEndOfGame(board, BLACK_PLAYER)
        self.assertTrue(isinstance(res, int) and (res == 0), "Mishandling of checkEndOfGame when null party for Black turn")
        #
        board = initBoard(10)
        moves = [
            ('b', 7, 'L'), ('a', 4, 'L'), ('d', 7, 'L'), ('c', 4, 'L'), (
                'f', 7, 'L'), ('e', 4, 'L'), ('h', 7, 'L'), ('g', 4, 'L'),
            ('j', 7, 'L'), ('i', 4, 'L'), ('a', 6, 'R'), ('b', 3, 'R'), (
                'c', 6, 'R'), ('a', 4, 'L'), ('e', 6, 'R'), ('c', 2, 'R'),
            ('g', 6, 'R'), ('b', 3, 'R'), ('c', 4, 'LB'), ('a', 4, 'L'), (
                'a', 6, 'R'), ('a', 2, 'L'), ('c', 4, 'L'), ('d', 1, 'R'),
            ('c', 8, 'L'), ('c', 2, 'R'), ('e', 4, 'L'), ('e', 2, 'R'), (
                'g', 4, 'L'), ('g', 2, 'R'), ('i', 4, 'L'), ('i', 2, 'R'),
            ('a', 2, 'RB'), ('b', 1, 'R'), ('c', 2, 'RB'), ('a', 2, 'L'), (
                'e', 2, 'RB'), ('b', 3, 'R'), ('g', 2, 'RB'), ('j', 1, 'R'),
            ('g', 4, 'R'), ('h', 1, 'R'), ('e', 4, 'R'), ('f', 1, 'R'), (
                'h', 3, 'R'), ('e', 2, 'R'), ('c', 4, 'R'), ('a', 4, 'L'),
            ('f', 3, 'R'), ('b', 5, 'L'), ('b', 7, 'R'), (
                'j', 3, 'R'), ('i', 8, 'L'), ('h', 5, 'R'), ('e', 8, 'R'),
            ('g', 6, 'R', 1, False, WHITE_PLAYER), (
                'd', 9, 'R', 1, False, WHITE_PLAYER)
        ]
        for move in moves:
            (white, black) = self.moveHelper(board, list(move))
            self.assertTrue(white, "Mishandling of checkEndOfGame in simulation for White player")
            self.assertTrue(black, "Mishandling of checkEndOfGame in simulation for Black player")
    #
    #

    def moveHelper(self, board, args):
        dic = {
            'X': ord(args.pop(0).lower()) - ord('a'),
            'Y': args.pop(0) - 1,
            'DIRECTION': args.pop(0).upper(),
            'LENGTH': 1,
            'WHITE_END': False,
            'BLACK_END': False
        }
        if(args):
            dic['LENGTH'] = args.pop(0)
        if(args):
            dic['WHITE_END'] = args.pop(0)
        if(args):
            dic['BLACK_END'] = args.pop(0)
        current = self.color(board[dic['Y']][dic['X']])
        (y, x), cap = movePiece(
            board, dic['Y'], dic['X'], dic['DIRECTION'], dic['LENGTH'])
        if(cap != None):
            capY, capX = cap
            capture(board, capY, capX)
        becomeKing(board, y, x)
        return (
            self.same(
                checkEndOfGame(board, WHITE_PLAYER), dic['WHITE_END']),
            self.same(
                checkEndOfGame(board, BLACK_PLAYER), dic['BLACK_END'])
        )

    def same(self, a, b):
        if(isinstance(a, bool)):
            if(not isinstance(b, bool)):
                return False
            return a == b
        if(isinstance(a, int)):
            if(not isinstance(b, int)):
                return False
            return a == b
        return False
    #
    #

    def createEmptyBoard(self):
        tmpBoard = initBoard(10)
        for y, x in self.blackList:
            tmpBoard[y][x] = FREE_SPACE
        return tmpBoard
    #
    #

    def createSpecialTestBoard(self):
        #  a  b  c  d  e  f  g  h  i  j
        #  0  1  2  3  4  5  6  7  8  9
        #|  |. |  |. |  |. |  |. |  |. | => 0
        #|. |  |p |  |. |  |. |  |p |  | => 1
        #|  |. |  |. |  |. |  |. |  |. | => 2
        #|. |  |. |  |. |  |. |  |. |  | => 3
        #|  |. |  |. |  |O |  |. |  |. | => 4
        #|. |  |. |  |. |  |. |  |. |  | => 5
        #|  |. |  |. |  |. |  |. |  |. | => 6
        #|. |  |p |  |. |  |. |  |p |  | => 7
        #|  |. |  |. |  |. |  |. |  |. | => 8
        #|. |  |. |  |. |  |. |  |. |  | => 9
        tmpBoard = self.createEmptyBoard()
        tmpBoard[4][5] = 2 * WHITE_PLAYER
        for y, x in [(1, 2), (1, 8), (7, 2), (7, 8)]:
            tmpBoard[y][x] = BLACK_PLAYER
        return tmpBoard
    #
    #

    def checkSideEffect(self):
        self.assertTrue(
            self.board == self.referrer, "side effect, board is changed")
    #
    #

    def humanToIndices(self, x, y):
        return ord(x) - ord('a'), y - 1
    #
    #

    def color(self, value):
        if(value <= BLACK_PLAYER):
            return BLACK_PLAYER
        if(value >= WHITE_PLAYER):
            return WHITE_PLAYER
        return FREE_SPACE
    #
    #

    def checkSignature(self, sig, length, defaults=None):
        return (
            len(sig.args) == length
            and sig.varargs == None
            and sig.keywords == None
            and sig.defaults == defaults
        )

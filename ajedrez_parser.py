#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re               # para los regex
import operator         # para ordenar por valor o clave los diccionarios en listas de tuplas
#import json             # utilizado en generateMoves

class Chess() :
  BLACK = 'b'
  WHITE = 'w'
  
  #// aqui uso None en lugar de self.EMPTY
  #//~ const EMPTY = -1;
  
  PAWN = 'p'
  KNIGHT = 'n'
  BISHOP = 'b'
  ROOK = 'r'
  QUEEN = 'q'
  KING = 'k'
  
  SYMBOLS = 'pnbrqkPNBRQK'
  
  DEFAULT_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
  
  POSSIBLE_RESULTS = ['1-0', '0-1', '1/2-1/2', '*']
  
  PAWN_OFFSETS = {
    BLACK : [ 16,  32,  17,  15],
    WHITE : [-16, -32, -17, -15]
  }
  
  PIECE_OFFSETS = {
    KNIGHT : [-18, -33, -31, -14,  18,  33,  31,  14],
    BISHOP : [-17, -15,  17,  15],
    ROOK : [-16,   1,  16,  -1],
    QUEEN : [-17, -16, -15,   1,  17,  16,  15,  -1],
    KING : [-17, -16, -15,   1,  17,  16,  15,  -1]
  }
  
  ATTACKS = [
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
    24,24,24,24,24,24,56,  0, 56,24,24,24,24,24,24, 0,
     0, 0, 0, 0, 0, 2,53, 56, 53, 2, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0,20, 2, 24,  2,20, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0,20, 0, 0, 24,  0, 0,20, 0, 0, 0, 0, 0,
     0, 0, 0,20, 0, 0, 0, 24,  0, 0, 0,20, 0, 0, 0, 0,
     0, 0,20, 0, 0, 0, 0, 24,  0, 0, 0, 0,20, 0, 0, 0,
     0,20, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0,20, 0, 0,
    20, 0, 0, 0, 0, 0, 0, 24,  0, 0, 0, 0, 0, 0,20
  ]
  
  RAYS = [
    17,  0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0, 15, 0,
     0, 17,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0,  0, 15,  0, 0,
     0,  0, 17,  0,  0,  0,  0, 16,  0,  0,  0,  0, 15,  0,  0, 0,
     0,  0,  0, 17,  0,  0,  0, 16,  0,  0,  0, 15,  0,  0,  0, 0,
     0,  0,  0,  0, 17,  0,  0, 16,  0,  0, 15,  0,  0,  0,  0, 0,
     0,  0,  0,  0,  0, 17,  0, 16,  0, 15,  0,  0,  0,  0,  0, 0,
     0,  0,  0,  0,  0,  0, 17, 16, 15,  0,  0,  0,  0,  0,  0, 0,
     1,  1,  1,  1,  1,  1,  1,  0, -1, -1,  -1,-1, -1, -1, -1, 0,
     0,  0,  0,  0,  0,  0,-15,-16,-17,  0,  0,  0,  0,  0,  0, 0,
     0,  0,  0,  0,  0,-15,  0,-16,  0,-17,  0,  0,  0,  0,  0, 0,
     0,  0,  0,  0,-15,  0,  0,-16,  0,  0,-17,  0,  0,  0,  0, 0,
     0,  0,  0,-15,  0,  0,  0,-16,  0,  0,  0,-17,  0,  0,  0, 0,
     0,  0,-15,  0,  0,  0,  0,-16,  0,  0,  0,  0,-17,  0,  0, 0,
     0,-15,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,-17,  0, 0,
   -15,  0,  0,  0,  0,  0,  0,-16,  0,  0,  0,  0,  0,  0,-17
  ]
  
  SHIFTS = {
    PAWN	: 0,
    KNIGHT : 1,
    BISHOP : 2,
    ROOK : 3,
    QUEEN : 4,
    KING : 5
  }
  
  FLAGS = {
    'NORMAL' : 'n',
    'CAPTURE' : 'c',
    'BIG_PAWN' : 'b',
    'EP_CAPTURE' : 'e',
    'PROMOTION' : 'p',
    'KSIDE_CASTLE' : 'k',
    'QSIDE_CASTLE' : 'q'
  }
  
  BITS = {
    'NORMAL' : 1,
    'CAPTURE' : 2,
    'BIG_PAWN' : 4,
    'EP_CAPTURE' : 8,
    'PROMOTION' : 16,
    'KSIDE_CASTLE' : 32,
    'QSIDE_CASTLE' : 64
  }

  RANK_1 = 7
  RANK_2 = 6
  RANK_3 = 5
  RANK_4 = 4
  RANK_5 = 3
  RANK_6 = 2
  RANK_7 = 1
  RANK_8 = 0

  SQUARES = {
    'a8' :   0, 'b8' :   1, 'c8' :   2, 'd8' :   3, 'e8' :   4, 'f8' :   5, 'g8' :   6, 'h8' :   7,
    'a7' :  16, 'b7' :  17, 'c7' :  18, 'd7' :  19, 'e7' :  20, 'f7' :  21, 'g7' :  22, 'h7' :  23,
    'a6' :  32, 'b6' :  33, 'c6' :  34, 'd6' :  35, 'e6' :  36, 'f6' :  37, 'g6' :  38, 'h6' :  39,
    'a5' :  48, 'b5' :  49, 'c5' :  50, 'd5' :  51, 'e5' :  52, 'f5' :  53, 'g5' :  54, 'h5' :  55,
    'a4' :  64, 'b4' :  65, 'c4' :  66, 'd4' :  67, 'e4' :  68, 'f4' :  69, 'g4' :  70, 'h4' :  71,
    'a3' :  80, 'b3' :  81, 'c3' :  82, 'd3' :  83, 'e3' :  84, 'f3' :  85, 'g3' :  86, 'h3' :  87,
    'a2' :  96, 'b2' :  97, 'c2' :  98, 'd2' :  99, 'e2' : 100, 'f2' : 101, 'g2' : 102, 'h2' : 103,
    'a1' : 112, 'b1' : 113, 'c1' : 114, 'd1' : 115, 'e1' : 116, 'f1' : 117, 'g1' : 118, 'h1' : 119
  }

  ROOKS = {
    WHITE : [{'square': SQUARES['a1'], 'flag': BITS['QSIDE_CASTLE']},
            {'square' : SQUARES['h1'], 'flag' : BITS['KSIDE_CASTLE']}],
    BLACK : [{'square' : SQUARES['a8'], 'flag' : BITS['QSIDE_CASTLE']},
            {'square' : SQUARES['h8'], 'flag' : BITS['KSIDE_CASTLE']}]
  }

  board = [None] * 120
  kings = {'w': None, 'b': None}
  turn = WHITE
  castling = {'w': 0, 'b': 0}
  epSquare = None
  halfMoves = 0
  moveNumber = 1
  history = []
  headerDict = {}
  generateMovesCache = {}

  def __init__(self, fen = ""):
    self.clear()
    
    if (len(str(fen)) > 0) :
      self.load(str(fen))
    else :
      self.reset()
  
  
  def clear(self) :
    self.board = [None] * 120
    self.kings = {self.WHITE : None, self.BLACK : None}
    self.turn = self.WHITE
    self.castling = {self.WHITE : 0, self.BLACK : 0}
    self.epSquare = None
    self.halfMoves = 0
    self.moveNumber = 1
    self.history = []
    self.headerDict = {}
    self.generateMovesCache = {}
    
  
  
  def updateSetup(self, fen) :
    if (len(self.history) > 0) :
      return
    if (fen != self.DEFAULT_POSITION) :
      self.headerDict['SetUp'] = '1'
      self.headerDict['FEN'] = fen
    else :
      del self.headerDict['SetUp']
      del self.headerDict['FEN']
  
  
    
  def header(self, key = None, value = '') :
    if (key != None) :
      self.headerDict[key] = value
    return self.headerDict
  
  
  
  
  def load(self, fen):
    if (not self.validateFen(fen)['valid']) :
      return False
      
    tokens = fen.split(' ')
    self.clear()
    
    #// position
    position = tokens[0]
    square = 0
    
    for i in range(len(position)) :
      piece = position[i]
      
      if(piece == '/') :
        square += 8
      
      elif piece.isdigit() :
        square += int(piece, 10)
      
      else :
        color=''
        if ord(piece) < ord('a') :
          color = self.WHITE
        else:
          color = self.BLACK
        
        self.put({
          'type' : piece.lower(),
          'color' : color,
        },
          self.algebraic(square)
        )
        square += 1
     
    #// turno
    self.turn = tokens[1]
    
    #// opciones enroque
    if 'K' in tokens[2] :
      self.castling['w'] |= self.BITS['KSIDE_CASTLE']
    if 'Q' in tokens[2] :
      self.castling['w'] |= self.BITS['QSIDE_CASTLE']
    if 'k' in tokens[2] :
      self.castling['b'] |= self.BITS['KSIDE_CASTLE']
    if 'q' in tokens[2] :
      self.castling['b'] |= self.BITS['QSIDE_CASTLE']
        
    #// casilla al paso
    if tokens[3] == '-' :
      self.epSquare = None
    else:
      self.epSquare = self.SQUARES[tokens[3]]
        
    #// medias jugadas
    self.halfMoves = int(tokens[4], 10)
        
    #// numero jugada
    self.moveNumber = int(tokens[5], 10)
        
    self.updateSetup(self.generateFen())
    return True
  
  
  
  
  def reset(self) :
    return self.load(self.DEFAULT_POSITION)
  
  
  
  def fen(self, onlyPosition = False) :
    empty = 0
    fen = ''
    # los diccionarios no se pueden ordenar. Necesito ordenar el diccionario SQUARES asi:
    # [('a8', 0), ('b8', 1), ... , ('g1', 118), ('h1', 119)]  lo cual es una lista de tuplas
    # ordeno por los valores:
    # se hace esto asi porque no se toca nada del tablero interno self.board
    sorted_squares = sorted(self.SQUARES.items(), key=operator.itemgetter(1))
    for i in sorted_squares :
      if self.board[i[1]] == None :
        empty += 1
      else:
        if empty > 0 :
          fen += str(empty)
          empty = 0
        color = self.board[i[1]]['color']
        piece = self.board[i[1]]['type']
    
        if color == self.WHITE :
          fen += piece.upper()
        else:
          fen += piece.lower()
          
      if (i[1] +1) & 0x88 :
        if empty > 0 :
          fen += str(empty)
        if i[1] != self.SQUARES['h1'] :
          fen += '/'
        empty = 0
        #i += 8
    
    
    cFlags = ''
    if (self.castling[self.WHITE] & self.BITS['KSIDE_CASTLE']) :
      cFlags += 'K'
    if (self.castling[self.WHITE] & self.BITS['QSIDE_CASTLE']) :
      cFlags += 'Q'
    if (self.castling[self.BLACK] & self.BITS['KSIDE_CASTLE']) :
      cFlags += 'k'
    if (self.castling[self.BLACK] & self.BITS['QSIDE_CASTLE']) :
      cFlags += 'q'
    if (cFlags == '') :
      cFlags = '-'
    
    # casilla al paso
    epFlags = ''
    if self.epSquare == None :
      epFlags = '-'
    else:
      epFlags = self.algebraic(self.epSquare)
    
    if onlyPosition:
      return ' '.join([fen, self.turn, cFlags, epFlags])
    else:
      return ' '.join([fen, self.turn, cFlags, epFlags, str(self.halfMoves), str(self.moveNumber)])
    
  
  
  
  
  # solo un alias
  def generateFen(self):
    return self.fen()
  
  
  
  
  
  def validateFen(self, fen):
    errors = {
      0 : 'No errors.',
      1 : 'FEN string must contain six space-delimited fields.',
      2	: '6th field (move number) must be a positive integer.',
      3	: '5th field (half move counter) must be a non-negative integer.',
      4	: '4th field (en-passant square) is invalid.',
      5	: '3rd field (castling availability) is invalid.',
      6	: '2nd field (side to move) is invalid.',
      7	: '1st field (piece positions) does not contain 8 \'/\'-delimited rows.',
      8	: '1st field (piece positions) is invalid [consecutive numbers].',
      9	: '1st field (piece positions) is invalid [invalid piece].',
      10 : '1st field (piece positions) is invalid [row too large].',
      11 : 'Illegal en-passant square'
    }
    
    tokens = fen.split(' ')
    
    # 1er critero: ¿ 6 campos separados por espacios? #
    if len(tokens) != 6:
      return {'valid': False, 'error_number': 1, 'error': errors[1]}
    
    # 2do criterio: ¿ campo numero jugada es un valor entero > 0? 
    if not tokens[5].isdigit() or int(tokens[5], 10) <= 0 :
      return {'valid': False, 'error_number' : 2, 'error' : errors[2]}
    
    #  3er criterio: contador medias jugadas es un entero >= 0
    if not tokens[4].isdigit() or int(tokens[4], 10) < 0 :
      return {'valid' : False, 'error_number' : 3, 'error' : errors[3]}
    
    # 4to criterio: 4to es una string válida? */
    patron = re.compile('^(-|[a-h]{1}[3|6]{1})$')
    if patron.search(tokens[3]) == None:
      return {'valid' : False, 'error_number' : 4, 'error' : errors[4]}
    
    # 5to criterio: 3er campo es una cadena valida de enroque
    patron = re.compile('(^-$)|(^[K|Q|k|q]{1,}$)')
    if patron.search(tokens[2]) == None:
      return {'valid' : False, 'error_number' : 5, 'error' : errors[5]}
    
    # 6to criterio: 2do campo es "w" (blancas-white) o "b" (negras-black)
    patron = re.compile('^(w|b)$')
    if patron.search(tokens[1]) == None:
      return {'valid' : False, 'error_number' : 6, 'error' : errors[6]}
    
    # 7mo criterio: ¿ 1ert campo contiene 8 filas ?
    rows = tokens[0].split('/')
    if len(rows) != 8 :
      return {'valid': False, 'error_number': 7, 'error': errors[7]}
    
    # 8-10 criterio: ¿cada fila es valida?
    for i in range(len(rows)) :
      sumFields = 0
      previousWasNumber = False
      
      for k in range(len(rows[i])) :
        if rows[i][k].isdigit() :
          # 8vo criterio: cada fila es valida
          if previousWasNumber :
            return {'valid' : False, 'error_number' : 8, 'error' : errors[8]}
          sumFields += int(rows[i][k], 10)
          previousWasNumber = True
        else :
          # 9no criterio: comprobar los simbolos de las piezas
          patron = re.compile('^[prnbqkPRNBQK]$')
          if patron.search(rows[i][k]) == None:
            return {'valid': False, 'error_number': 9, 'error': errors[9]}
          sumFields += 1
          previousWasNumber = False
    
      # 10mo criterio: compueba la suma de piezas + casillas en blanco debe ser 8    
      if sumFields != 8 :
        return {'valid': False, 'error_number': 10, 'error': errors[10]}
    
    # 11ro criterio: en-passant if last is black's move, then its must be white turn
    if len(tokens[3]) > 1 :
      if ((tokens[3][1] == '3' and tokens[1] == 'w') or (tokens[3][1] == '6' and tokens[1] == 'b')) :
        return {'valid': False, 'error_number': 11, 'error': errors[11]}
    
    # todo esta OK 
    return {'valid': True, 'error_number': 0, 'error': errors[0]}
  
  
  
  #/* using the specification from http://www.chessclub.com/help/PGN-spec
  # * example for html usage: chess.pgn({ 'max_width' : 72, 'newline_char' : "<br />" ])
  # * 
  # */
  def pgn(self, options = {}):
    max_width = 0
    try:
      if options['newline_char'] != "" :
        newline = options['newline_char']
    except:
      newline = "\n"
    try:
      if options['max_width'] != "" :
        max_width = options['max_width']
    except:
      max_width = 0
        
    result = []
    header_exists = False
    
    #// se procesa la cabecera
    for i in self.headerDict :
      result.append('[' + i + ' \"' + self.headerDict[i] + '\"]' + newline)
      header_exists = True
      
    if (header_exists and len(self.history) >0) :
        result.append(newline)
        
    #/* pop all of history onto reversed_history */
    reversed_history = []
    while (len(self.history) > 0) :
      reversed_history.append(self.undoMove())
    
    moves = []
    move_string = ''
    pgn_move_number = 1
    
    #/* build the list of moves.  a move_string looks like: "3. e3 e6" */
    while (len(reversed_history) > 0) :
      move = reversed_history.pop()

      #/* if the position started with black to move, start PGN with 1. ... */
      if (pgn_move_number == 1 and move['color'] == 'b') :
        move_string = '1. ...'
        pgn_move_number += 1
      elif (move['color'] == 'w') :
        #/* store the previous generated move_string if we have one */
        if (len(move_string) > 0) :
          moves.append(move_string)
        move_string = str(pgn_move_number) + '.'
        pgn_move_number += 1

      move_string = move_string + ' ' + self.moveToSan(move)
      self.makeMove(move)
    
    #/* are there any other leftover moves? */
    if (len(move_string) > 0) :
      moves.append(move_string)

    #/* is there a result? */
    try:
      moves.append(header["Result"])
    except:
      pass
    
    #/* history should be back to what is was before we started generating PGN,
    # * so join together moves
    # */
    if (max_width == 0) :
      return(''.join(result) + ' '.join(moves))
      #return result.join('') + moves.join(' ');
    
    
    #/* wrap the PGN output at max_width */
    current_width = 0
    for i in range(len(moves)) :
      #/* if the current move will push past max_width */
      if (current_width + len(moves[i]) > max_width and i != 0) :

        #/* don't end the line with whitespace */
        if (result[len(result) - 1] == ' ') :
          result.pop()

        result.append(newline)
        current_width = 0
      elif (i != 0) :
        result.append(' ')
        current_width += 1
      
      result.append(moves[i])
      current_width += len(moves[i])
    

    return ''.join(result)
    
    
  
  def historia(self, options = {}):
    # esto tiene el mismo comportamiento que empty de php
    #Return Values: Returns FALSE if var has a non-empty and non-zero value.
    def empty( variable ):
      if not variable:
        return True
      return False
    # ----------------------------------------------------------------
    reversed_history = []
    move_history = []
    opc = False
    try:
      if not empty(options):
        opc = True
    except:
      opc = False
      
    verbose = (opc != False and 'verbose' in options and options['verbose'])
            
    while (len(self.history) > 0) :
      reversed_history.append(self.undoMove())
    
    while (len(reversed_history) > 0) :
      move = reversed_history.pop()
      if (verbose) :
        # la función makePretty me cambia el diccionario que le envio(move)
        # por tanto hago una copia dura
        copia = move.copy()
        move_history.append(self.makePretty(copia))
      else :
        move_history.append(self.moveToSan(move))
      
      self.makeMove(move)
    

    return move_history 
    
  

  
  #// devuelve False si no existe la casilla, 
  # si existe devuelve la pieza
  def remove(self, square):
    if square in self.SQUARES :
      return False
    
    piece = self.get(square)
    self.board[self.SQUARES[square]] = None
    if (piece and piece['type'] == self.KING) :
      self.kings[piece['color']] = None
    
    self.updateSetup(self.generateFen())

    return piece
    
    
  
  
  def get(self, square) :
    #// check for valid square
    if square not in self.SQUARES:
      return None
        
    return self.board[self.SQUARES[square]]; #// ¿un atajo?
  
  
  
  def squareColor(self, square):
    if (square in self.SQUARES) :
      sq_0x88 = self.SQUARES[square]
      if (self.rank(sq_0x88) + self.file(sq_0x88)) % 2 == 0 :
        return 'light'
      else:
        return 'dark'
      #return ((self.rank(sq_0x88) + self.file(sq_0x88)) % 2 == 0) ? 'light' : 'dark';
    
    return None
  
  
  def put(self, piece, square) :
    # funcion ad-hoc------------------------------------
    # se le llama con comillas incluidas
    def isset(variable):
      return variable in locals() or variable in globals()
    # --------------------------------------------------- 
    #// check for valid piece object
    
    if (not('type' in piece and 'color' in piece)) :
      return False
    
    # comprueba si existe la pieza
    if piece['type'].lower() not in self.SYMBOLS :
      return False
    
    # comprueba si la casilla es valida
    if square not in self.SQUARES :
      return False
    
    sq = self.SQUARES[square];
    
    # no permitimos poner más de un rey
    if piece['type'] == self.KING and not(self.kings[piece['color']] == None or self.kings[piece['color']] == sq) :
      return False
        
    self.board[sq] = {'type' : piece['type'], 'color' : piece['color']}
    if (piece['type'] == self.KING) :
      self.kings[piece['color']] = sq
    
    self.updateSetup(self.generateFen())
    return True
  


  
  #// here, we add first parameter turn, to make this really static method
  #// because in chess.js var turn got from outside scope, 
  #// maybe need a little fix in chess.js or maybe i am :-p
  def buildMove(self, turn, board, _from, to, flags, promotion = None):
    move = {
      'color'	: turn,
      'from' : _from,
      'to' : to,
      'flags' : flags,
      'piece'	: board[_from]['type']
    }
    
    if (promotion != None) :
      move['flags'] |= self.BITS['PROMOTION']
      move['promotion'] = promotion
    
    
    if (board[to] != None) :
      move['captured'] = board[to]['type']
    elif (flags & self.BITS['EP_CAPTURE']) :
      move['captured'] = self.PAWN
    
    return move
  
  
  
  
  def makeMove(self, move) :
    us = self.turno();
    them = self.swap_color(us)
    historyKey = self.recordMove(move)
    
    self.board[move['to']] = self.board[move['from']]
    self.board[move['from']] = None
    
    #// if flags:EP_CAPTURE (en passant), remove the captured pawn 
    if move['flags'] & self.BITS['EP_CAPTURE'] :
      if us == self.BLACK :
        self.board[move['to'] - 16] = None
      else:
        self.board[move['to'] + 16] = None
    
    #// if pawn promotion, replace with new piece
    if (move['flags'] & self.BITS['PROMOTION']) :
      self.board[move['to']] = {'type' : move['promotion'], 'color' : us}
    
    #/* if big pawn move, update the en passant square */
    if move['flags'] & self.BITS['BIG_PAWN'] :
      if us == self.BLACK :
        self.epSquare = move['to'] - 16
      else :
        self.epSquare = move['to'] + 16
    else :
      self.epSquare = None
    
    #// reset the 50 move counter if a pawn is moved or piece is captured
    if (move['piece'] == self.PAWN) :
      self.halfMoves = 0;
    elif (move['flags'] & (self.BITS['CAPTURE'] | self.BITS['EP_CAPTURE'])) :
      self.halfMoves = 0
    else :
      self.halfMoves += 1
    
    
    #// if we moved the king
    if (self.board[move['to']]['type'] == self.KING) :
      #//~ self.kings[$this->board[$move['to']]['color']] = $move['to'];
      self.kings[us] = move['to']
      
      #// if we castled, move the rook next to the king
      if (move['flags'] & self.BITS['KSIDE_CASTLE']) :
        castlingTo = move['to'] - 1
        castlingFrom = move['to'] + 1
        self.board[castlingTo] = self.board[castlingFrom]
        self.board[castlingFrom] = None
      elif (move['flags'] & self.BITS['QSIDE_CASTLE']) :
        castlingTo = move['to'] + 1
        castlingFrom = move['to'] - 2
        self.board[castlingTo] = self.board[castlingFrom];
        self.board[castlingFrom] = None
      
      self.castling[us] = 0  #// or maybe ''
    
    
    #// turn of castling of we move a rock
    if (self.castling[us] > 0) :
      for i in range(len(self.ROOKS[us])) :
        if (
            move['from'] == self.ROOKS[us][i]['square'] and
            self.castling[us] & self.ROOKS[us][i]['flag']
            ) :
          self.castling[us] ^= self.ROOKS[us][i]['flag']
          break
          
    #// turn of castling of we capture a rock
    if (self.castling[them] > 0) :
      for i in range(len(self.ROOKS[them])) :
        if (
            move['to'] == self.ROOKS[them][i]['square'] and
            self.castling[them] & self.ROOKS[them][i]['flag']
            ) :
          self.castling[them] ^= self.ROOKS[them][i]['flag']
          break
        
    
    if (us == self.BLACK) :
      self.moveNumber += 1
    
    self.turn = them
    
    #//~ echo $historyKey . PHP_EOL;
    #// needed caching for short inThreefoldRepetition()
    self.history[historyKey]['position'] = self.fen(True)
    
  
  
  
  def push(self, move):
    #// solo un alias por conveniencia para la api publica
    return self.recordMove(move)
  

  def recordMove(self, move) :
    # --- para ponernos al final del array/lista history
    def end(tmp):
      return tmp[-1]
    #---------------------------------------------------
    jugada = {
      'move' : move,
      'kings' : {
              self.WHITE : self.kings[self.WHITE], 
              self.BLACK : self.kings[self.BLACK]
              },
      'turn' : self.turno(),
      'castling' : {
              self.WHITE : self.castling[self.WHITE], 
              self.BLACK : self.castling[self.BLACK]
              },
      'epSquare' : self.epSquare,
      'halfMoves' : self.halfMoves,
      'moveNumber' : self.moveNumber,
    }
    self.history.append(jugada)
    end(self.history)
    indice = self.history.index(end(self.history))  # obtenemos el num. de indice
    
    return(indice)
  
  
  
  def undoMove(self) :
    old = self.history.pop()
    
    if old == None :
      return None
        
    move = old['move']
    self.kings = old['kings']
    self.turn = old['turn']
    self.castling = old['castling']
    self.epSquare = old['epSquare']
    self.halfMoves = old['halfMoves']
    self.moveNumber = old['moveNumber']
    
    us = self.turn
    them = self.swap_color(us)
    
    self.board[move['from']] = self.board[move['to']]
    self.board[move['from']]['type'] = move['piece'];   #// to undo any promotions
    self.board[move['to']] = None
    
    #// if capture
    if (move['flags'] & self.BITS['CAPTURE']) :
      self.board[move['to']] = {'type' : move['captured'], 'color' : them}
    elif (move['flags'] & self.BITS['EP_CAPTURE']) :
      #index = 0
      if us == self.BLACK :
        index = move['to'] - 16
      else :
        index = move['to'] + 16
      self.board[index] = {'type': self.PAWN, 'color': them}
    
    
    #// if castling
    if (move['flags'] & (self.BITS['KSIDE_CASTLE'] | self.BITS['QSIDE_CASTLE'])) :
      if (move['flags'] & self.BITS['KSIDE_CASTLE']) :
        castlingTo = move['to'] + 1
        castlingFrom = move['to'] - 1
      elif (move['flags'] & self.BITS['QSIDE_CASTLE']) :
        castlingTo = move['to'] - 2
        castlingFrom = move['to'] + 1      
      self.board[castlingTo] = self.board[castlingFrom]
      self.board[castlingFrom] = None
    
    return move
  
  
  
  
  def undo(self) :
    move = self.undoMove()
    if move != None :
      return self.makePretty(move)
    else:
      return None
  
  
  
  
  def generateMoves(self, options = {}) :
    # esto parece feo, pero...
    # la lista moves es mutable y se puede modificar dentro de la funcion
    # con sus metodos estandar, cambiandose tambien en el exterior de la funcion
    def addMove(turno, board, moves, _from, to, flags) :
      #/* if pawn promotion */
      if (board[_from]['type'] == self.PAWN and
          (self.rank(to) == self.RANK_8 or self.rank(to) == self.RANK_1)) :
        promotionPieces = [self.QUEEN, self.ROOK, self.BISHOP, self.KNIGHT]
        for i in range(0, len(promotionPieces)) :
          moves.append(self.buildMove(turno, board, _from, to, flags, promotionPieces[i]))
      else :
        moves.append(self.buildMove(turno, board, _from, to, flags))
    
    
    opciones = options.copy()
    
    #// legal moves only? 
    clave = ""
    legal = ""
    hay_clave = opciones.keys()
    for i in hay_clave:
      clave = i    
    if clave == 'legal':
      es_legal = opciones.values()
      for k in es_legal:
        legal = k
        
    moves = []
    us = self.turno()
    them = self.swap_color(us)
    secondRank = {self.BLACK : self.RANK_7,
            self.WHITE : self.RANK_2}
    
    firstSquare = self.SQUARES['a8']
    lastSquare = self.SQUARES['h1']
    singleSquare = False
    
    #/* are we generating moves for a single square? */
    if len(options)> 0 and 'square' in options :
      if (options['square'] in self.SQUARES) :
        firstSquare = lastSquare = self.SQUARES[options['square']]
        singleSquare = True
      else:
        singleSquare = False
    
    
    for i in range(firstSquare, lastSquare + 1) :
      if (i & 0x88) : 
        i += 7
        continue
      
      piece = self.board[i]
      if (piece == None or piece['color'] != us) :
        continue
      
      if (piece['type'] == self.PAWN) :
        #// single square, non-capturing
        square = i + self.PAWN_OFFSETS[us][0]
        if (self.board[square] == None) :
          addMove(us, self.board, moves, i, square, self.BITS['NORMAL'])
          
          #// double square
          square = i + self.PAWN_OFFSETS[us][1]
          if (secondRank[us] == self.rank(i) and self.board[square] == None) :
            addMove(us, self.board, moves, i, square, self.BITS['BIG_PAWN'])
        
        #// pawn captures
        for j in range(2,4) :
          square = i + self.PAWN_OFFSETS[us][j]
          if (square & 0x88) :
            continue
          if (self.board[square] != None ) :
            if (self.board[square]['color'] == them) :
              addMove(us, self.board, moves, i, square, self.BITS['CAPTURE'])
          elif (square == self.epSquare) :    #// get epSquare from enemy
            addMove(us, self.board, moves, i, self.epSquare, self.BITS['EP_CAPTURE'])
        
      else:
        for j in range(len(self.PIECE_OFFSETS[piece['type']])) :
          offset = self.PIECE_OFFSETS[piece['type']][j]
          square = i
          
          while True :
            square += offset
            if (square & 0x88) :
              break
            
            if (self.board[square] == None) :
              addMove(us, self.board, moves, i, square, self.BITS['NORMAL'])
            else :
              if (self.board[square]['color'] == us) :
                break
              addMove(us, self.board, moves, i, square, self.BITS['CAPTURE'])
              break;
            
            if (piece['type'] == self.KNIGHT or piece['type'] == self.KING) :
              break
    
    
    #// castling
    #// a) we're generating all moves
    #// b) we're doing single square move generation on king's square
    if (not singleSquare or lastSquare == self.kings[us]) :
      if (self.castling[us] & self.BITS['KSIDE_CASTLE']) :
        castlingFrom = self.kings[us]
        castlingTo = castlingFrom + 2
        
        if (
            self.board[castlingFrom + 1] == None and
            self.board[castlingTo] == None and
            not self.attacked(them, self.kings[us]) and
            not self.attacked(them, castlingFrom + 1) and
            not self.attacked(them, castlingTo)
            ) :          
          addMove(us, self.board, moves, self.kings[us], castlingTo, self.BITS['KSIDE_CASTLE'])
        
      #
      if (self.castling[us] & self.BITS['QSIDE_CASTLE']) :
        castlingFrom 	= self.kings[us]
        castlingTo 	= castlingFrom - 2
        
        if (
            self.board[castlingFrom - 1] == None and
            self.board[castlingFrom - 2] == None and     # && // $castlingTo
            self.board[castlingFrom - 3] == None and     # && // col "b", next to rock
            not self.attacked(them, self.kings[us]) and
            not self.attacked(them, castlingFrom - 1) and
            not self.attacked(them, castlingTo)
            ) :
          addMove(us, self.board, moves, self.kings[us], castlingTo, self.BITS['QSIDE_CASTLE'])
    """
    es_legal = options.values()
    for k in es_legal:
      legal = k
    """
    
    # // return all pseudo-legal moves (this includes moves that allow the king to be captured)
    if (legal == False) :
      #self.generateMovesCache[cacheKey] = moves
      return moves
    
    
    #/* filter out illegal moves */
    legalMoves = []
    
    for i in range(0, len(moves)) :
      self.makeMove(moves[i])
      if (not self.kingAttacked(us)) :
        legalMoves.append(moves[i])
      self.undoMove()
        
    #self.generateMovesCache[cacheKey] = legalMoves
    return legalMoves
    
  
  
  
  # parses all of the decorators out of a SAN string
  def strippedSan(self, move) :
    jug = move.replace('=','')
    jug1 = re.sub('[+#]?[?!]*$','', jug)
    return jug1
  
  
  
  
  #// convert a move from Standard Algebraic Notation (SAN) to 0x88 coordinates
  def moveFromSan(self, move, sloppy = {}) :
    # strip off any move decorations: e.g Nf3+?!
    clean_move = self.strippedSan(move)
    matches = []
    piece = _from = to = promotion = ""
    #// if we're using the sloppy parser run a regex to grab piece, to, and from
    #// this should parse invalid SAN like: Pe2-e4, Rc1c4, Qf3xf7
    if sloppy :
      patron = re.compile('([pnbrqkPNBRQK])?([a-h][1-8])x?-?([a-h][1-8])([qrbnQRBN])?')
      matches = patron.findall(clean_move)
      if (matches) :
        piece = matches[0][0]
        _from = matches[0][1]
        to = matches[0][2]
        promotion = matches[0][3]
    
    moves = self.generateMoves()
    for i in range(len(moves)):
      #// try the strict parser first, then the sloppy parser if requested
      #// by the user
      if ((clean_move == self.strippedSan(self.moveToSan(moves[i]))) or
          (sloppy and clean_move == self.strippedSan(self.moveToSan(moves[i], True)))) :
        return moves[i]
      else :
        if (len(matches) > 0 and
            (not piece or piece.lower() == moves[i]['piece']) and
            self.SQUARES[_from] == moves[i]['from'] and
            self.SQUARES[to] == moves[i]['to'] and
            (not promotion or promotion.lower() == moves[i]['promotion'])) :
          return moves[i]
    
    return None
    
  
  
  
  #/* The move function can be called with in the following parameters:
  # *
  # * .move('Nxb7')      <- where 'move' is a case-sensitive SAN string
  # *
  # * .move({ from: 'h7', <- where the 'move' is a move object (additional
  # *         to :'h8',      fields are ignored)
  # *         promotion: 'q', 
  # *      })
  # */
  def move(self, sanOrArray, options = {}):
    moveArray = None
    #moves = []
    #moves = self.generateMoves()
    
    #// allow the user to specify the sloppy move parser to work around over
    #// disambiguation bugs in Fritz and Chessbase
    #var sloppy = (typeof options !== 'undefined' && 'sloppy' in options) ?
    #              options.sloppy : false;
    try:
      sloppy = options['sloppy']
    except:
      sloppy = False
        
    if type(sanOrArray) == str :
      #/* convert the move string to a move object */
      """
      for i in range(0, len(moves)) :
        if sanOrArray == self.moveToSan(moves[i]) :
          moveArray = moves[i]
          break
      """
      moveArray = self.moveFromSan(sanOrArray, sloppy)
      
    elif type(sanOrArray) == dict :
      moves = self.generateMoves()
      try:
        sanOrArray['promotion']
        #sanOrArray['promotion'] = sanOrArray['promotion']
      except:
        sanOrArray['promotion'] = None
      
      #/* convert the pretty move object to an ugly move object */
      for move in moves :
        try:
          move['promotion']
        except:
          move['promotion'] = None
        
        if sanOrArray['from'] == self.algebraic(move['from']) and sanOrArray['to'] == self.algebraic(move['to']) and (move['promotion'] == None or sanOrArray['promotion'] == move['promotion']):
          moveArray = move
          break

    if(moveArray == None) :
      return None
    
    # la jugada están froma diccionario. Necesito hacer una copia
    # dura porque parece que el diccionario se pasa por referencia
    # y en makePretty() lo modifica
    moveFea = moveArray.copy()
    
    movePretty = self.makePretty(moveArray)
    self.makeMove(moveFea)
    
    return movePretty
    
    
  
  
  #/* The internal representation of a chess move is in 0x88 format, and
  # * not meant to be human-readable.  The code below converts the 0x88
  # * square coordinates to algebraic coordinates.  It also prunes an
  # * unnecessary move keys resulting from a verbose call.
  # */
  def moves(self, options = {'verbose' : False}):
    ugly_moves = self.generateMoves()
    
    moves = []
        
    for i in range(len(ugly_moves)) :

      #/* does the user want a full move object (most likely not), or just
      # * SAN
      # */
      
      if options['verbose'] != False and 'verbose' in options and options['verbose'] :
        moves.append(self.makePretty(ugly_moves[i]))
      else :
        moves.append(self.moveToSan(ugly_moves[i]))
    
    return moves
    
  
  

  def turno(self):
    return self.turn
  
  
  
  
  def attacked(self, color, square) :
    for i in range(self.SQUARES['a8'], self.SQUARES['h1'] + 1) :
      if (i & 0x88) :    #// check edge of board
        i += 7
        continue     
      
      if (self.board[i] == None) :    # // check empty square
        continue
      if (self.board[i]['color'] != color) :   #// check color
        continue
      
      piece = self.board[i]
      difference = i - square
      index = difference + 119
      
      if (self.ATTACKS[index] & (1 << self.SHIFTS[piece['type']])) :
        if (piece['type'] == self.PAWN) :
          if (difference > 0) :
            if (piece['color'] == self.WHITE) :
              return True
          else :
            if (piece['color'] == self.BLACK) :
              return True
          continue
                
        if (piece['type'] == self.KNIGHT or piece['type'] == self.KING) :
          return True
        
        offset = self.RAYS[index]
        j = i + offset
        blocked = False
        while (j != square) :
          if (self.board[j] != None) :
            blocked = True
            break
          j += offset
        
        if (not blocked) :
          return True
    
    return False
    
    
    
  
  def kingAttacked(self, color) :
    return self.attacked(self.swap_color(color), self.kings[color])
  
  
  def inCheck(self) :
    return self.kingAttacked(self.turn)
  

  def inCheckmate(self):
    return self.inCheck() and len(self.generateMoves()) == 0
  

  def inStalemate(self):
    return not self.inCheck() and len(self.generateMoves()) == 0
  
  
  def insufficientMaterial(self):
    pieces = {
      self.PAWN : 0,
      self.KNIGHT : 0,
      self.BISHOP : 0,
      self.ROOK : 0,
      self.QUEEN : 0,
      self.KING : 0
    }
    bishops = None
    numPieces = 0
    sqColor = 0
    
    # como aqui no se escribe en el tablero interno solo recorro las 64 casillas
    # "ordeno" el diccionario SQUARES
    sorted_squares = sorted(self.SQUARES.items(), key=operator.itemgetter(1))
    
    for i in sorted_squares :
      sqColor = (sqColor + 1) % 2
      if (i[1] & 0x88):
        #i += 7
        continue
        
      piece = self.board[i[1]]
      if (piece != None):
        if piece['type'] in pieces :
          pieces[piece['type']] = pieces[piece['type']] + 1
        else:
          pieces[piece['type']] = 1
          
        numPieces += 1
        
    #// k vs k
    if (numPieces == 2) :
      return True
    
    #// k vs kn / k vs kb
    if (numPieces == 3 and (pieces[self.BISHOP] == 1 or pieces[self.KNIGHT] == 1)) :
      return True
    
    #// k(b){0,} vs k(b){0,}  , because maybe you are a programmer we talk in regex (preg) :-p
    if (numPieces == pieces[self.BISHOP] + 2) :
      sum = 0
      lenB = len(bishops)
      for alfil in bishops:
        sum += alfil
      
      if (sum == 0 or sum == lenB) :
        return True
    
    
    return False
  
  
  
  #/* TODO: while this function is fine for casual use, a better
  #   * implementation would use a Zobrist key (instead of FEN). the
  #   * Zobrist key would be maintained in the make_move/undo_move functions,
  #   * avoiding the costly that we do below.
  #   */
  def inThreefoldRepetition(self):
    hash = {}
    for historia in self.history:
      if historia['position'] in hash:
        hash[historia['position']] += 1
      else :
        hash[historia['position']] = 1
        
      if (hash[historia['position']] >= 3) :
        return True
        
    return False
  
  
  
  
  def halfMovesExceeded(self):
    return self.halfMoves >= 100
  

  #// alias in*()
  def inHalfMovesExceeded(self):
    return self.halfMovesExceeded()
  
  
  def inDraw(self):
    return (self.halfMovesExceeded() or
      self.inStalemate() or
      self.insufficientMaterial() or
      self.inThreefoldRepetition())
  

  def gameOver(self):
    return self.inDraw() or self.inCheckmate()
  


  def rank(self, i) :
    return i >> 4


  def file(self, i) :
    return i & 15


  def algebraic(self, i) :
    f = self.file(i)
    r = self.rank(i)
    
    return 'abcdefgh'[f:f+1] + '87654321'[r:r+1]
	
  
  def swap_color(self, color) :
    if color == self.WHITE:
      color = self.BLACK
    else:
      color = self.WHITE
    return color
  
  
  #// this function is used to uniquely identify ambiguous moves
  def getDisambiguator(self, move, sloppy = {}):
    contrario = not sloppy 
    
    moves = self.generateMoves({'legal' : contrario})
    
    _from = move['from']
    to = move['to']
    piece = move['piece']
    
    ambiguities = 0
    sameRank = 0
    sameFile = 0
    
    for i in range(len(moves)) :
      ambiguityFrom = moves[i]['from']
      ambiguityTo = moves[i]['to']
      ambiguityPiece = moves[i]['piece']
      
      #/* if a move of the same piece type ends on the same to square, we'll
      # * need to add a disambiguator to the algebraic notation
      # */
      if (
          piece == ambiguityPiece and
          _from != ambiguityFrom and
          to == ambiguityTo
          ) :
        ambiguities +=1
        if (self.rank(_from) == self.rank(ambiguityFrom)) :
          sameRank += 1
        if (self.file(_from) == self.file(ambiguityFrom)) :
          sameFile += 1
    
    
    if (ambiguities > 0) :
      #/* if there exists a similar moving piece on the same rank and file as
      # * the move in question, use the square as the disambiguator
      # */
      if (sameRank > 0 and sameFile > 0) :
        return self.algebraic(_from)
      
      #/* if the moving piece rests on the same file, use the rank symbol as the
      # * disambiguator
      # */
      elif (sameFile > 0) :
        return self.algebraic(_from)[1:2]
      
      #// else use the file symbol
      else:
        return self.algebraic(_from)[0:1]
    
    return ''
  
  
  
  
  #// convert a move from 0x88 to SAN
  def moveToSan(self, move, sloppy = {}) :
    output = ''
    
    if move['flags'] & self.BITS['KSIDE_CASTLE'] :
      output = 'O-O'
    elif move['flags'] & self.BITS['QSIDE_CASTLE'] :
      output = 'O-O-O'
    else:
      disambiguator = self.getDisambiguator(move, sloppy)
      
      #// pawn e2->e4 is "e4", knight g8->f6 is "Nf6"
      if move['piece'] != self.PAWN :
        output += move['piece'].upper() + disambiguator
          
      #// x on capture
      if move['flags'] & (self.BITS['CAPTURE'] | self.BITS['EP_CAPTURE']) :
        if (move['piece'] == self.PAWN) :
          output += self.algebraic(move['from'])[0:1]
          
        output += 'x'
      
      output += self.algebraic(move['to'])
      
      #// promotion example: e8=Q
      if (move['flags'] & self.BITS['PROMOTION']) :
        output += '=' + move['promotion'].upper()
    
    #// check / checkmate
    self.makeMove(move)
    if self.inCheck() :
      if self.inCheckmate() :
        output += '#'
      else :
        output += '+'
    
    self.undoMove()
    
    return output
  
  
  
  
  
  def makePretty(self, uglyMove):
    #move = uglyMove   #tengo que clonarla
    move = uglyMove.copy()
    move['san'] = self.moveToSan(move)
    move['to'] = self.algebraic(move['to'])
    move['from'] = self.algebraic(move['from'])
    
    flags = ''
    
    for flag in self.BITS :
      if self.BITS[flag] & move['flags'] :
        flags += self.FLAGS[flag]
       
    move['flags'] = flags
    
    return move
  


  def _toString(self):
    return self.ascii()
  
  
  def ascii(self):
    s = '   +------------------------+\n'
    
    # "ordeno" el diccionario SQUARES
    sorted_squares = sorted(self.SQUARES.items(), key=operator.itemgetter(1))
    
    for i in sorted_squares :
      # i[0] = es la clave; i[1] es el valor
      #// display the rank
      if self.file(i[1]) == 0 :
        s += '   ' + '87654321'[self.rank(i[1])]

      #/* empty piece */
      if self.board[i[1]] == None : 
        s += ' . '
      else :
        piece = self.board[i[1]]['type']
        color = self.board[i[1]]['color']
        symbol = ""
        if color == self.WHITE :
          symbol = piece.upper()
        else:
          symbol = piece.lower()

        s += ' ' + symbol + ' '

      if ((i[1] + 1) & 0x88) :
        s += '|\n'
        #i[1] += 8
    
    s += '   +------------------------+\n'
    s += '     a  b  c  d  e  f  g  h\n'

    return s
  
  
  
  """
  // Debug Utility 
  function perft(depth) {
    var moves = generate_moves({legal: false});
    var nodes = 0;
    var color = turn;

    for (var i = 0, len = moves.length; i < len; i++) {
      make_move(moves[i]);
      if (!king_attacked(color)) {
        if (depth - 1 > 0) {
          var child_nodes = perft(depth - 1);
          nodes += child_nodes;
        } else {
          nodes++;
        }
      }
      undo_move();
    }

    return nodes;
  }
  """
  


#!/usr/bin/env python3
import sys
import time
import random
import numpy as np
import time

def piece_score(symbol):
  symbol = symbol.upper()
  if symbol == "P":
    return 1
  if symbol == "N":
    return 3
  if symbol == "B":
    return 3.5
  if symbol == "R":
    return 5
  if symbol == "Q":
    return 9
  if symbol == "K":
    return 100
  return 0

# def game_over



def pieces_score(board, turn):
  score = 0
  pieces = board.piece_map().values()
  for piece in pieces:
    symbol = piece.symbol()
    if turn and symbol.isupper() or not turn and symbol.islower():
      score += piece_score(symbol)
  return score



def utility(board, turn):
   score = 0
   score += pieces_score(board, turn)
   score -= pieces_score(board, not turn)
   return score



def get_move(board, limit=100):
  # TODO: Fill this in with an actual chess engine

  start = time.time() * 1000


  move = random.choice(list(board.legal_moves))

  turn = board.turn

  
  i = 1
  while time.time() * 1000 - start < limit - 30:
      max_score, max_move = tree(board=board, time_start=start, maximize=turn, turn=turn, turns_left=i, limit=limit)
      i += 1
  if max_move == None:
    return move
  return max_move



def tree(board, time_start, maximize, turn, turns_left, limit):
  if time.clock() * 1000 - time_start > limit - 30 or turns_left <= 0:
    return utility(board, turn), None
  moves = list(board.legal_moves)
  max_score = 0
  max_move = None
  for move in moves:
    new_board = board.copy()
    new_board.push(move)
    score, move = tree(new_board, time_start, not maximize, turn,  turns_left - 1, limit)
    if maximize and score > max_score:
      max_score = score
      max_move = move
    if not maximize and score < max_score:
      max_score = score
      max_move = move
  return max_score, max_move






if __name__ == "__main__":
  while 1:
    cmd = input().split(" ")
    #print(cmd, file=sys.stderr)

    if cmd[0] == "uci":
      print("uciok")
    elif cmd[0] == "ucinewgame":
      pass
    elif cmd[0] == "isready":
      print("readyok")
    elif cmd[0] == "position":
      if cmd[1] == "startpos":
        board = chess.Board()
        if len(cmd) > 2 and cmd[2] == "moves":
          for m in cmd[3:]:
            board.push(chess.Move.from_uci(m))
    elif cmd[0] == "go":
      if len(cmd) > 1 and cmd[1] == "movetime":
        move = get_move(board, limit=int(cmd[2]))
      else:
        move = get_move(board)
      print("bestmove %s" % move)
    elif cmd[0] == "quit":
      exit(0)
      

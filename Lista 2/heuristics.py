def _taken(board):
    taken = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] in [1,2]:
                taken += 1
    return taken / board.n ** 2
            

def count_tiles(board, player):
    score = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == (player + 1):
                score += 1 
            elif board.board[row][col] != 0:
                score -= 1
    return score

def tile_value(board, player):
    weight = [
        [ 10,  -5,   5,   3,   3,   5,  -5,  10],
        [ -5,  -5,  -3,  -1,  -1,  -3,  -5,  -5],
        [  5,  -3,   3,   3,   3,   3,  -5,   5],
        [  3,  -1,   2,   1,   1,   2,  -1,   3],
        [  3,  -1,   2,   1,   1,   2,  -1,   3],
        [  5,  -5,   3,   3,   3,   3,  -5,   5],
        [ -5,  -5,  -3,  -1,  -1,  -3,  -5,  -5],
        [ 10,  -5,   5,   3,   3,   5,  -5,  10]
    ]

    score = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == (player + 1):
                score += weight[row][col]
            elif board.board[row][col] != 0:
                score -= weight[row][col]
    return score

def progressive_aggressiveness(board, player):
    coeff = _taken(board)
    prim_coeff = 1 - coeff
    return tile_value(board, player) * prim_coeff + count_tiles(board, player) * coeff
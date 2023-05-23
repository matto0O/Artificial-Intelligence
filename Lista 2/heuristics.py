def count_tiles(board, player):
    """
    Heuristic function that returns a score based on the number of tiles
    occupied by the given player. More tiles result in a higher score.

    Parameters:
    - board (Board)     : the current board
    - player (int)      : player for whom tiles are counted

    Returns:
    - score (int)       : the score for the move
    """
    score = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == (player + 1):
                score += 1 
            elif board.board[row][col] != 0:
                score -= 1
    return score

def progressive_aggressiveness(board, player):
    """
    Heuristic function that returns a score based on the number of tiles
    occupied by the given player. More tiles result in a higher score.

    Parameters:
    - board (Board)     : the current board
    - player (int)      : player for whom tiles are counted

    Returns:
    - score (int)       : the score for the move
    """
    score = 0
    total_tiles_taken = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == (player + 1):
                score += 1 
            elif board.board[row][col] != 0:
                score -= 1
            else:
                total_tiles_taken += 1
    return score * ((total_tiles_taken - score) ** 2)
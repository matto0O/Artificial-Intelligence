def minimax(board, player, depth, rating):
    bestMove = None

    if depth == 0 or board.is_over():
        return bestMove, rating(board, player)
    
    if player:
        maxEval = float('-inf')
        for move in board.get_legal_moves():
            board.move = move
            board.make_move(False)
            board.current_player = int(not player)
            _, eval = minimax(board, board.current_player, depth - 1, rating)
            if maxEval < eval:
                maxEval = eval
                bestMove = move
                print(move, maxEval, eval, bestMove)
        return bestMove, maxEval
    
    minEval = float('inf')
    for move in board.get_legal_moves():
        board.move = move
        board.make_move(False)
        board.current_player = int(not player)
        _, eval = minimax(board, board.current_player, depth - 1, rating)
        if minEval > eval:
            minEval = eval
            bestMove = move
    return bestMove, minEval

def abpruning(board, player, depth, rating):
    alpha = float('-inf')
    beta = float('inf')
    bestMove = None

    if depth == 0 or board.is_over():
        return bestMove, rating(board, player)
    
    if player:
        maxEval = float('-inf')
        for move in board.get_legal_moves():
            board.move = move
            board.make_move(False)
            board.current_player = int(not player)
            _, eval = abpruning(board, board.current_player, depth - 1, rating)
            if maxEval < eval:
                maxEval = eval
                bestMove = move
            alpha = max(alpha, maxEval)

            if beta <= alpha:
                return bestMove, alpha
        return bestMove, maxEval
    
    minEval = float('inf')
    for move in board.get_legal_moves():
        board.move = move
        board.make_move(False)
        board.current_player = int(not player)
        _, eval = abpruning(board, board.current_player, depth - 1, rating)
        if minEval > eval:
            minEval = eval
            bestMove = move
        beta = min(beta, minEval)

        if alpha <= beta:
            return bestMove, beta
    return bestMove, minEval
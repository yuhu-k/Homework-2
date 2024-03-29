liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def balancer(input_token_liquidity, output_token_liquidity, input_amount):
    fee = 0.003
    return output_token_liquidity - input_token_liquidity * output_token_liquidity / (input_token_liquidity + input_amount * (1 - fee))

def find_profitable_paths(start_token, current_token, liquidity, current_balance, path, paths):
    if current_token == start_token and path:
        if current_balance > 20:
            paths.append((path.copy(), current_balance))
        return
    
    for (token1, token2), (liquidity1, liquidity2) in liquidity.items():
        if token1 == current_token:
            next_balance = balancer(liquidity1, liquidity2, current_balance)
            if token2 not in path:  # 避免循環
                find_profitable_paths(start_token, token2, liquidity, next_balance, path + [token2], paths)
        elif token2 == current_token:
            next_balance = balancer(liquidity2, liquidity1, current_balance)
            if token1 not in path:  # 避免循環
                find_profitable_paths(start_token, token1, liquidity, next_balance, path + [token1], paths)

start_token = "tokenB"
paths = []
find_profitable_paths(start_token, start_token, liquidity, 5, [], paths)

for path, balance in paths:
    print(f"path: tokenB->{'->'.join(path)}, tokenB balance={balance:.6f}")
    
# tokenB->tokenA->tokenD->tokenC->tokenB
path = ["tokenB", "tokenA", "tokenD", "tokenC", "tokenB"]
balance = 5
for i in range(0, len(path)-1):
    if path[i] > path[i+1]:
        balance = balancer(liquidity[(path[i+1], path[i])][1], liquidity[(path[i+1], path[i])][0], balance)
        print(f"{path[i]}->{path[i+1]}: {balance:.6f}")
    else:
        balance = balancer(liquidity[(path[i], path[i+1])][0], liquidity[(path[i], path[i+1])][1], balance)
        print(f"{path[i]}->{path[i+1]}: {balance:.6f}")

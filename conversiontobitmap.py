gamematrix = ['Wl', 'Wn', 'Ws', 'Wg', 'Wk', 'Wg', 'Ws', 'Wn', 'Wl', 0, 'Wr', 0, 0, 0, 0, 0, 'Wb', 0, 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Bp', 0, 0, 0, 0, 0, 0, 'Bp', 'Bp', 0, 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 0, 'Bb', 0, 0, 0, 0, 0, 'Br', 0, 'Bl', 'Bn', 'Bs', 'Bg', 'Bk', 'Bg', 'Bs', 'Bn', 'Bl', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

print(len(gamematrix))

pcs = ['Wl', 'Wn', 'Ws', 'Wg', 'Wk', 'Wr', 'Wb', 'Wp', 'Bl', 'Bn', 'Bs', 'Bg', 'Bk', 'Br', 'Bb', 'Bp', 'WL', 'WN', 'WS', 'WR', 'WB', 'WP', 'BL', 'BN', 'BS', 'BR', 'BB', 'BP']
bitmap = []

for pc in pcs: 
    for x in gamematrix:
        if x == pc:
            bitmap.append(1)
        else:
            bitmap.append(0)

print(len(pcs))
print(len(bitmap))
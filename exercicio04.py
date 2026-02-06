x = 'python'
achou = False
vogal = 'aeiou'
while x and not achou:
    if x[0] in vogal:
        print('X', end=' ')
        achou = True
    else:
        x = x[1:]
if not achou:
    print('O', end=' ')

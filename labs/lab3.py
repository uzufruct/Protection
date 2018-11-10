from protection import signature

file = 'Немного новостей.pdf'
signature.sign(file, method='gost')
print(signature.check(file + '-sgn.gost'))

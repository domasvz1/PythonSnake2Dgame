def funkcija_1( stringas ):
    print( stringas )


print('pirmas "print"')
print(__name__ )


    
funkcija_1('Pirmas kreipinys į funkciją')


if __name__ == 'main':
    print('antras "print"')
    print(__name__)
    funkcija_1('Antras kreipinys į funkciją')
    

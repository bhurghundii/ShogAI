# -*- coding: UTF-8 -*-
class ml_util():
    def LetterToNumber(self, Letter):
        for chrval in range(97, 123):
            if (Letter == chr(chrval)):
                return chrval - 97

    def ShogNotationToY(self, num):
        return 9 - num

    def YValueToShogNotation(self, num):
        return 9 - num

    def numberToLetter(self, num):
        return chr(num + 65).lower()

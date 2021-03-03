#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

#A continuación, definimos nuestra clase Tablero como una subclase del tipo incorporado dict. 
#Esto es porque almacenaremos el tablero como un diccionario.
class TableroAjedrez(dict):
    # A continuación, definimos x_eje y y_eje para nuestro tablero de ajedrez como tuplas inmutables.
    y_eje = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    x_eje = (1,2,3,4,5,6,7,8)
    
    patt = None
    
    def __init__(self, fen, juego):
        self.juego = juego
        self.procesa_notacion(fen)
        
        
    #Se pueden mostrar las piezas en TableroAjedrez para una FEN dada, de la siguiente manera:
    """
    El trabajo del método procesa_notacion es expandir primero los espacios 
    en blanco representados por enteros en espacios reales. 
    Utiliza el módulo de expresión regular incorporado (re) de Python para 
    expandir los espacios en blanco en una notación FEN dada.
    
    El código, expande_espacios_blancos, reemplaza cada dígito por el número 
    correspondiente de espacios en blanco, 
    de modo que puede asumir más adelante que un espacio en blanco es un cuadrado vacío. 
    A continuación, convierte la notacion FEN en una cadena correspondiente a 
    coordenadas alfanuméricas x e y para cada pieza. 
    Para ello, llama a otro método denominado alpha_notation.
    
    Las dos últimas líneas mantienen un control del turno de los jugadores, 
    aunque lo hago con mi parser.
    """
    def procesa_notacion(self, patt):
        patt = patt.split(' ')
        # expand espacios en blanco
        def expande_espacios(match): 
            return ' ' * int(match.group(0))
        patt[0] = re.compile(r'\d').sub(expande_espacios, patt[0])
        for x, row in enumerate(patt[0].split('/')):
            for y, alphabet in enumerate(row):
                if alphabet == ' ': continue
                xycoord = self.alfa_notacion((7-x,y))
                # xycoord es A8 , A7, etc
                self[xycoord] = self.juego.get(xycoord)
                        

    #Necesitamos una manera de convertir las coordenadas x e y de una pieza a 
    #su notación equivalente alfabética, por ejemplo, A1, D5, E3, etc.
    def alfa_notacion(self,xycoord):
        if not self.esta_en_tablero(xycoord): return
        return self.y_eje[xycoord[1]] + str(self.x_eje[xycoord[0]])

    #Del mismo modo, definimos un método que toma una coordenada x, y como entrada y 
    #devuelve su notación numérica equivalente, de la siguiente manera:
    def num_notacion(self, xycoord):
        return int(xycoord[1])-1, self.y_eje.index(xycoord[0])
        
    #la definición de un método para comprobar si una determinada coordenada está en el tablero,
    def esta_en_tablero(self, coord):
        if coord[1] < 0 or coord[1] > 7 or coord[0] < 0 or coord[0] > 7:
            return False
        else: return True
        
    

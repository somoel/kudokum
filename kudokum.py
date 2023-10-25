import tkinter as tk
import random as rd
from tkinter import messagebox

# Ventana
root = tk.Tk()
root.title("Kudoku")

# Frame del juego
kudokuFrame = tk.Frame(root)
kudokuFrame.pack()

grid_entrys = {} # 81 Entrys en el diccionario. Se almacenan como "entry" + row + col

# Permite que únicamente puedan ser números o espacios vacíos en cada entry
def validateNumber(valor):
    if valor.isdigit() and len(valor) == 1:
        return True
    elif valor == "":
        return True
    else:
        return False
    
vcmd = (root.register(validateNumber), '%P')


# Cuando haya un evento de focusear un entry
def entryFocused(event, a, b):
    # Cuando se focusea
    if event.widget == root.focus_get():
        event.widget.config(bg='#dddddd') # El entry se vuelve gris

        # Y todos los entrys con ese número, también
        if event.widget.get() != "":
            for i in range(9):
                for j in range(9):
                    if grid_entrys[f"entry{i}{j}"].get() == event.widget.get():
                        grid_entrys[f"entry{i}{j}"].config(background='#cccccc', disabledbackground='#cccccc')
        if event.widget.cget('state') == 'normal':
            for i in range(9):
                if i != b:
                    grid_entrys[f"entry{a}{i}"].config(background='#eeeeee', disabledbackground='#eeeeee')
                if i != a:
                    grid_entrys[f"entry{i}{b}"].config(background='#eeeeee', disabledbackground='#eeeeee')
            
    # Cuando se desfocusea
    else:
        # Regresa todo a como setaba
        event.widget.config(bg='white')
        if event.widget.get() != "":
            for i in range(9):
                for j in range(9):
                    if grid_entrys[f"entry{i}{j}"].get() == event.widget.get():
                        grid_entrys[f"entry{i}{j}"].config(background='white', disabledbackground='white')
        
        if event.widget.cget('state') == 'normal':
            for i in range(9):
                grid_entrys[f"entry{a}{i}"].config(background='white', disabledbackground='white')
                grid_entrys[f"entry{i}{b}"].config(background='white', disabledbackground='white')
        
        

# Cuando se pone un número
def keyEntered(event, a, b):
    # Limpia el color de los entrys
    for i in range(9):
        for j in range(9):
            grid_entrys[f"entry{i}{j}"].config(background='white', disabledbackground='white')

    # Refocusea
    if event.widget == root.focus_get():
        event.widget.config(bg='#dddddd')
        if event.widget.get() != "":
            for i in range(9):
                for j in range(9):
                    if grid_entrys[f"entry{i}{j}"].get() == event.widget.get():
                        grid_entrys[f"entry{i}{j}"].config(background='#cccccc', disabledbackground='#cccccc')
        if event.widget.cget('state') == 'normal':
            for i in range(9):
                if i != b:
                    grid_entrys[f"entry{a}{i}"].config(background='#eeeeee', disabledbackground='#eeeeee')
                if i != a:
                    grid_entrys[f"entry{i}{b}"].config(background='#eeeeee', disabledbackground='#eeeeee')

    # Desfocusea
    else:
        event.widget.config(bg='white')
        if event.widget.get() != "":
            for i in range(9):
                for j in range(9):
                    if grid_entrys[f"entry{i}{j}"].get() == event.widget.get():
                        grid_entrys[f"entry{i}{j}"].config(background='white', disabledbackground='white')
        
        if event.widget.cget('state') == 'normal':
            for i in range(9):
                grid_entrys[f"entry{a}{i}"].config(background='white', disabledbackground='white')
                grid_entrys[f"entry{i}{b}"].config(background='white', disabledbackground='white')

    # Checkea la integridad para subrayar el error
    error_integrity = checkIntegrity(a, b, event.widget.get())
    if error_integrity != [] and event.widget.get() != "": # Si hay una repetida
        for error_site in error_integrity:
            grid_entrys[f"entry{error_site[0]}{error_site[1]}"].config(background='#fe7375', disabledbackground='#fe7375') 
                # Colorea todas las ocurrencias
    
    # Revisa si el jugador ganó
    win_state = True 
    for i in getNumMatrix():
        for j in i:
            if j == "":
                win_state = False

    if win_state:
        messagebox.showinfo("Felicidades", "Ha ganado")

# Controles cuando esté focuseado alguno
def focus(event, a, b):
    key = event.keysym # tecla
    try:
        if key == "Up" or key == "w":
            grid_entrys[f"entry{a-1}{b}"].focus_set()
        elif key == "Down" or key == "s":
            grid_entrys[f"entry{a+1}{b}"].focus_set()
        elif key == "Left" or key == "a":
            grid_entrys[f"entry{a}{b-1}"].focus_set()
        elif key == "Right" or key == "d":
            grid_entrys[f"entry{a}{b+1}"].focus_set()
        elif key.isdigit() and key != "0":
            grid_entrys[f"entry{a}{b}"].delete(0, tk.END)
            grid_entrys[f"entry{a}{b}"].insert(0, event.char)
    except:
        pass

# Generación de la matriz de entrys
for i in range(9):
    for j in range(9):
        # Características del Entry
        grid_entrys[f"entry{i}{j}"] = tk.Entry(kudokuFrame, width=2,
                                                font=("Product Sans", 20),
                                                  justify="center", insertontime=0,
                                                    validate='key', validatecommand=vcmd)
        grid_entrys[f"entry{i}{j}"].grid(row = i * 2, column = j * 2) # Posición del entry en la grilla

        # Eventos
        grid_entrys[f"entry{i}{j}"].bind('<FocusIn>', lambda event, i=i, j=j: entryFocused(event, i, j))
        grid_entrys[f"entry{i}{j}"].bind('<FocusOut>', lambda event, i=i, j=j: entryFocused(event, i, j))

        grid_entrys[f"entry{i}{j}"].bind('<Key>', lambda event, i=i, j=j: focus(event, i, j))
        grid_entrys[f"entry{i}{j}"].bind("<KeyRelease>", lambda event, i=i, j=j: keyEntered(event, i, j))
        
# Espacios del sudoku
tk.Label(kudokuFrame).grid(row=0, column= 5, rowspan=18)
tk.Label(kudokuFrame).grid(row=0, column= 11, rowspan=18)
tk.Label(kudokuFrame, font=("Arial", 1)).grid(row=5, column= 0, columnspan=18)
tk.Label(kudokuFrame, font=("Arial", 1)).grid(row=11, column= 0, columnspan=18)

# Devuelve la matriz total
def getNumMatrix():
    numMatrix = []
    for i in range(9):
        numMatrix.append([])
        for j in range(9):
            numMatrix[i].append(grid_entrys[f"entry{i}{j}"].get())

    return numMatrix

# Revisa si el numero n en la posición axb tiene algúna coincidencia en su misma fila a, columna b o cuadrícula
# Argumentos: a -> Fila; b -> Columna; n -> Número
# Devuelve: [] si no hay conflictos. Si hay, da una lista de listas de donde está el conflicto
def checkIntegrity(a, b, n):
    numMatrix = getNumMatrix() # Obtiene la matriz
    error_data = [] # Lista para retornar las coordenadas donde coinciden
        
    # Revisa fila y columna
    for i in range(9):
        # Fila
        if numMatrix[a][i] == n and i != b:
            error_data.append([str(a), str(i)])
        #Columna
        if numMatrix[i][b] == n and i != a:
            error_data.append([str(i), str(b)])
    
    # Revisa cuadro
    tri1 = [0, 1, 2]
    tri2 = [3, 4, 5]
    tri3 = [6, 7, 8]
    for tri in [tri1, tri2, tri3]: # Obtiene la posición del cuadro  
        if a in tri:
            tria = tri
        if b in tri:
            trib = tri
    for i in tria: # Evalúa cada elemento del cuadro
        for j in trib:
            if numMatrix[i][j] == n and i != a and j != b:
                    error_data.append([str(i), str(j)])
                
    return error_data

# Debug: Muestra la matriz en consola
def showNumMatrix():
    for i in range(9):
        print("")
        for j in range(9):
            print(grid_entrys[f"entry{i}{j}"].get(), end="")



# Generación del sudoku

tries = 1 # Debug: Contador de intentos
while True:
    try: # Try, por si se genera un juego imposible, reiniciar.

        # Reinicia la matriz
        for i in range(9):
            for j in range(9):
                grid_entrys[f"entry{i}{j}"].delete(0, tk.END)

        # Generación de cada número
        for i in range(9):
            for j in range(9):
                # Actualizo la matriz, los números compatibles e incompatibles
                numMatrix = getNumMatrix()
                incompatible_numbers = []
                compatible_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

                # Reviso todos los números de la fila y columna inscritas
                for k in range(9):
                    # check row
                    if numMatrix[i][k] != "":
                        incompatible_numbers.append(numMatrix[i][k])

                    # check col
                    if numMatrix[k][j] != "":
                        incompatible_numbers.append(numMatrix[k][j])

                # Y del cuadrado
                tri1 = [0, 1, 2]
                tri2 = [3, 4, 5]
                tri3 = [6, 7, 8]
                for tri in [tri1, tri2, tri3]:        
                    if i in tri:
                        tria = tri
                    if j in tri:
                        trib = tri
                for k in tria:
                    for l in trib:
                        if numMatrix[k][l] != "":
                            incompatible_numbers.append(numMatrix[k][l])

                # Remover números incompatibles de la lista de los compatibles
                for number in incompatible_numbers:
                    if number in compatible_numbers:
                        compatible_numbers.pop(compatible_numbers.index(number))
                        
                # Elige un número al azar de los compatibles y lo asigna
                num = str(rd.choice(compatible_numbers))
                grid_entrys[f"entry{i}{j}"].delete(0, tk.END)
                grid_entrys[f"entry{i}{j}"].insert(0, num)

    except:
        # Si llega a crearse un sudoku imposible, se suma un intento al contador y se reinicia
        tries += 1
    else:
        print(f"intento {tries}")
        break

# Guarda el sudoku solucionado
saved_matrix = getNumMatrix()

# Ocultar algunas casillas en base a la dificultad (no hay definida)
for i in range(9):
    for j in range(9):
        if not rd.randint(0, 2) == 0: # La probabilidad de que se oculte es de 2/3
            grid_entrys[f"entry{i}{j}"].delete(0, tk.END)
        else:
            grid_entrys[f"entry{i}{j}"].config(state='disabled', disabledbackground='white', fg='gray')


root.mainloop()
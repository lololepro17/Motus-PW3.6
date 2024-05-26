import random
import tkinter as tk


# Ouverture du fichier "dico.txt" en lecture
fichier = open("dico_fr.txt", "r")
words2 = fichier.readlines()
fichier.close()

# Suppression du caractère '\n'
words = [word.rstrip() for word in words2]

# Chargement des listes de mots en français et anglais
with open('dico_fr.txt') as f:
  frenchWords = f.readlines()

# Mise en majuscule des mots (français et anglais) et suppression du '\n'
listFrenchWords = [word.strip('\n').upper() for word in frenchWords]

lgMotus = 7

currentLanguage = "french"  # Langue courante
dic = {'french': listFrenchWords}  # Dictionnaire de mots par langue
OKnb = 0  # Nombre de tentatives réussies (à initialiser)
TotalNb = 0  # Nombre total de tentatives (à initialiser)
current_mode = "light"  # Initial mode set to light
# Fonction de réinitialisation des variables globales (missing implementation)

def reinit():
  global mot, attemptsNb, lettersOK, motTrouve  # Déclaration des variables globales utilisées

  motTrouve = False  # Initialisation du mot trouvé (faux)
  attemptsNb = 0  # Initialisation du nombre de tentatives (0)
  mot = []  # Liste vide pour stocker le mot choisi
  lettersOK = []  # Liste vide pour stocker les lettres correctement devinées
  
  # Boucle pour effacer les caractères d'affichage et réinitialiser la couleur
  for count in range(lgMotus * 6):
    labChar[count].configure(text='_', fg='black')  # Affichage d'un underscore noir pour chaque caractère

  labError.configure(text=' ')  # Effacement du message d'erreur


def montrer(currentWord, i, couleur):
  global attemptsNb  # Déclaration de la variable globale utilisée

  rowId = lgMotus * (attemptsNb + i)  # Calcul de l'identifiant de la ligne

  if attemptsNb + i < 6:  # Vérification si la tentative est dans la limite autorisée
    for count in range(len(motus)):  # Boucle pour parcourir chaque caractère du mot
      labChar[rowId + count].configure(text=currentWord[count], fg=couleur)  # Affichage du caractère et de sa couleur

       
def choisirMot(length):
  global currentLanguage  # Déclaration de la variable globale utilisée

  words = dic[currentLanguage]  # Récupération des mots de la langue courante

  # Filtrage des mots ayant la longueur demandée
  wordCharNb = [word for word in words if len(word) == length]

  # Sélection d'un mot aléatoire parmi ceux filtrés
  wTG = wordCharNb[random.randint(0, len(wordCharNb) - 1)]

  return wTG  # Renvoi du mot choisi


def nombreOccurrencesCaracteres(mot): 

  mot = mot.upper()  # Conversion en majuscule

  dicOccurence = {}  # Dictionnaire pour stocker les occurrences

  for caractere in mot:  # Boucle pour parcourir chaque caractère du mot
    if caractere in dicOccurence:  # Si le caractère existe déjà dans le dictionnaire
      dicOccurence[caractere] += 1  # Incrémenter son nombre d'occurrences
    else:
      dicOccurence[caractere] = 1  # Ajouter le caractère et son occurrence initiale (1)

  return dicOccurence  # Renvoyer le dictionnaire des occurrences


def delete():
    labError.configure(text='')

# Reads the proposal from the entry box
def jouer():
  """
  Fonction principale du jeu. Gère la saisie de la proposition de l'utilisateur et la vérification du mot.
  """

  global lgMotus, attemptsNb, motTrouve, proposition, entry

  if attemptsNb < 7 and not motTrouve:  # Vérification si le nombre de tentatives est inférieur à la limite et si le mot n'a pas été trouvé
    proposition = entry.get()  # Récupération de la proposition de l'utilisateur dans la zone de saisie
    entry.delete(0, tk.END)  # Effacement de la zone de saisie après récupération de la proposition

    if len(proposition) == lgMotus:  # Vérification si la proposition a la bonne longueur
      montrer(proposition, 0, 'black')  # Affichage de la proposition en noir

      if proposition in words:  # Vérification si la proposition existe dans le dictionnaire de mots
        window.after(1000, verifier)  # Appel différé de la fonction `check` après un court délai (1 seconde)
      else:
        montrer(proposition, 0, 'black')  # Affichage de la proposition en noir
        labError.configure(text="Mot inconnu", fg='red')  # Message d'erreur : "Mot inconnu" en rouge
        attemptsNb += 1  # Incrémentation du nombre de tentatives
        montrer(lettersOK, 0, 'blue')  # Affichage des lettres correctement devinées en bleu
        window.after(1500, delete)  # Appel différé de la fonction `delete` après un court délai (1.5 seconde)
        if attemptsNb == 6:  # Si c'est la dernière tentative
          window.after(1500, rep)  # Appel différé de la fonction `answer` après un court délai (1.5 seconde)

    else:  # Si la proposition n'a pas la bonne longueur
      labError.configure(text="Longueur incorrecte", fg='red')  # Message d'erreur : "Longueur incorrecte" en rouge
      attemptsNb += 1  # Incrémentation du nombre de tentatives
      montrer(lettersOK, 0, 'blue')  # Affichage des lettres correctement devinées en bleu
      window.after(1000, delete)  # Appel différé de la fonction `delete` après un court délai (1 seconde)
      if attemptsNb == 6:  # Si c'est la dernière tentative
        window.after(500, rep)  # Appel différé de la fonction `answer` après un court délai (0.5 seconde)
        window.after(1500, game)  # Appel différé de la fonction `game` après un court délai (1.5 seconde) pour relancer la partie

# 
def verifier():
  """
  Fonction de vérification du mot proposé. Compare le mot proposé et le mot à deviner,
  et met à jour l'affichage en fonction des lettres correctes et mal placées.
  """

  global lgMotus, motus, mot, lettersOK, attemptsNb, motTrouve, OKnb, proposition

  # Création de dictionnaires d'occurrences des caractères pour le mot à deviner et la proposition
  dic = nombreOccurrencesCaracteres(motus)  # Occurences dans le mot à deviner
  dicProposal = nombreOccurrencesCaracteres(proposition)  # Occurences dans la proposition

  motTrouve = True  # hypothèse initiale : le mot est trouvé

  for count, charMotus in enumerate(motus):  # Boucle pour chaque caractère du mot à deviner
    letter = proposition[count].upper()  # Récupération et mise en majuscule de la lettre correspondante de la proposition
    dicProposal[letter] -= 1  # Décrémentation de l'occurrence de la lettre dans la proposition

    if letter == charMotus:  # Si la lettre est correcte et à la bonne place
      mot[count] = charMotus  # Mise à jour du mot deviné
      lettersOK[count] = charMotus  # Ajout à la liste des lettres correctement placées
      dic[letter] -= 1  # Décrémentation de l'occurrence de la lettre dans le mot à deviner
      labChar[lgMotus * (attemptsNb) + count].configure(text=letter, fg='green')  # Affichage en vert

    elif letter in dic and dic[letter] > 0 and dicProposal[letter] < dic[letter]:  # Si la lettre existe dans le mot à deviner, est présente dans la proposition mais pas assez
      mot[count] = letter.lower()  # Mise à jour du mot deviné (en minuscule)
      dic[letter] -= 1  # Décrémentation de l'occurrence de la lettre dans le mot à deviner
      labChar[lgMotus * (attemptsNb) + count].configure(text=letter, fg='red')  # Affichage en rouge
      motTrouve = False  # Le mot n'est pas encore trouvé

    else:  # Si la lettre est incorrecte
      mot[count] = '_'  # Affichage d'un underscore
      motTrouve = False  # Le mot n'est pas encore trouvé

  attemptsNb += 1  # Incrémentation du nombre de tentatives

  if motTrouve:  # Si le mot a été trouvé
    OKnb += 1  # Incrémentation du nombre de mots trouvés
    lab_OKnb.configure(text=str(OKnb))  # Mise à jour de l'affichage du nombre de mots trouvés
    window.after(1500, game)  # Appel différé de la fonction `game` après un court délai (1.5 seconde) pour relancer la partie

  else:  # Si le mot n'a pas été trouvé
    montrer(lettersOK, 0, 'blue')  # Affichage des lettres correctement placées en bleu

  if attemptsNb == 6:  # Si c'est la dernière tentative
    window.after(500, rep)  # Appel différé de la fonction `answer` après un court délai (0.5 seconde)
    window.after(1500, game)  # Appel différé de la fonction `game` après un court délai (1.5 seconde) pour relancer la partie
# Montre la bonne rep
def rep():
    global attemptsNb
    attemptsNb=6
    montrer(motus,-1,'green')
    window.after(1500,game)  
# launch
def game():
    print("Nouvelle Partie Commencez")

    global lgMotus,motus,mot,attemptsNb,lettersOK,motTrouve,TotalNb
    TotalNb+=1
    lab_TotalNb.configure(text=str(TotalNb))
    reinit()
    motus=choisirMot(lgMotus)
    mot.append(motus[0])
    lettersOK.append(motus[0])
    for i in range(lgMotus-1):
        mot.append('_')
        lettersOK.append('_')
    montrer(lettersOK,0,'blue')
  
#Creer une nouvelle partie
def newGame(): 
    global TotalNb,OKnb    
    TotalNb=0
    OKnb=0
    game()
    
    
def kill():
    print("Fin de la partie")
    window.destroy()
    
############################################################################
# Gui
############################################################################
fon = "Helvetica"
fg ="#E0E0E0"
window = tk.Tk()
window.title("Motus")

top = tk.Menu(window)
window.config(menu=top)
jeu = tk.Menu(top, tearoff=False)

top.add_cascade(label='Jeu', menu=jeu)
jeu.add_command(label='Nouveau Jeu', command=newGame)
jeu.add_command(label='Quitter', command=kill)
settings = tk.Menu(top, tearoff=False)


# Labels

# Info message
# Erreur message

labError=tk.Label(window,text='')
labError.grid(row=2,column=0)

# Motus grilles

labChar=[]
for i in range(lgMotus*6):
    labChar.append(tk.Label(window,text='_',font=(fon, 25), fg=fg))
for count in range(lgMotus*6):
    labChar[count].grid(row=1+count//lgMotus, column=3+count%lgMotus)

# Stats

lab_text_TotalNb=tk.Label(window,text='Partie Jouez',font=(fon, 15),fg=fg)
lab_text_TotalNb.grid(row=2,column=17)
lab_TotalNb=tk.Label(window,text=0,font=(fon, 15), fg=fg)
lab_TotalNb.grid(row=3,column=17)


lab_text_OKnb=tk.Label(window,text='Mots Trouvez',font=(fon), fg=fg)

lab_text_OKnb.grid(row=4,column=17)
lab_OKnb=tk.Label(window,text=0,font=(fon, 15), fg=fg)
lab_OKnb.grid(row=5,column=17)

# Entry box
# Entry box for player

entry=tk.Entry()
entry.grid(row=0,column=0)

# Bouttons
but_Enter=tk.Button(window,text="Enter",command=jouer)
but_Enter.grid(row=1,column=0)


but_Answer=tk.Button(window,text="Solution",command=rep)
but_Answer.grid(row=5,column=0)

# Start
game()
window.mainloop()

# Projet Génération d'un terrain de jeu vidéo

## Prérequis

L'utilisation du jeu nécessite python 3.8 et la librairie tkinter afin de pouvoir être utilisé.

## Présentation du jeu
Bienvenue dans le jeu **MINECERAFT** un jeu dans lequel VOUS êtes votre propre héros.

Dans ce jeu vous pourrez créer votre propre terrain grâce à l'addition de 6 paramètres.

Toutes les maps que vous y généreriez sont procédurales, c'est-à-dire, n'ont jamais de fin.

## Lancement du jeu


Au lancement du jeu vous pouvez observer 4 choix :

![Menu](menu.png)

1) Jouer permet tout simplement de lancer le jeu (si vous n'avez changeé aucun paramètre alors le jeu se lancera avec les paramètres par défaut).

2) Paramètres, quant à lui, emmène vers une autre fenêtre dans laquelle vous pourrez changer les différentes options du jeu.

3) Charger permet de charger une partie sauvegardée au préalable.

4) Et enfin quitter ferme le jeu.

# Paramètres

## Paramètres de générations du terrain:
Une fois après avoir appuyé sur paramètres, vous avez les options de génération de terrain regroupées dans **Choix de la taille** et **Choix des options**.

![parametre1](parametre.png)

## Choix de la taille :

Vous pouvez ensuite choisir la taille du terrain en hauteur en appuyant sur **Choix de la taille**. La valeur par défaut est 50, la valeur minimale est 2 et la valeur maximale est 100.

![Taille](taille.png)

Apres avoir choisi votre taille, il suffit d'appuyer sur valider.

## Choix des options de génération du terrain :

Vous pouvez choisir ensuite 5 conditions de génération pour le terrain en appuyant sur **Choix des options**.

![option](option.png)

Vous pouvez ici choisir 5 paramètres p, n, T, k **(voir explications des paramètres partie Code)** ici les valeurs par défaut sont  0.5, 4, 5 et 1 respectivement. Pour valider vos choix appuyer sur *valider*.

## Défaut

Lorsque qu'un changement est effectué dans les paramètres alors un nouveau bouton défaut apparaîtra, remettant toutes les valeurs par défaut.

![defaut](default.png)

## Paramètres aditionnels résolution

Cette option permet de choisir la taille de la fenêtre du jeu et vous permet, si vous le souhaiter, de jouer en plein écran.

![resolution](résolution.png)

Pour cela, il suffit de cliquer sur la taille voulue en pixel (note : les tailles sont en LARGEURxHAUTEUR et la valeur par défaut est 800x600 sans PleinEcran) et de cocher ou non **FullScreen**. Pour revenir au paramètres, il suffit de cliquer sur **Valider**.

# Début du jeu

Une fois avoir changé les paramètres comme vous le souhaitiez, vous pouvez appuyer sur **Valider** dans la fenêtre des paramètres pour retourner au menu principal et appuyer sur **jouer**.

![jeu](jeu.png)

C'est ici que votre aventure commence. Vous placez le personnage d'un **clic gauche** de la souris sur les cases de terre, vous le déplacez grâce aux **flèches directionnelles** et si vous souhaitez retirer le personnage, il suffit de faire un clic sur celui-ci.

Pour revenir en arrière dans vos mouvements, vous pouvez effectuer un **CTRL-Z**.

Pour revenir au menu principal il suffit d'appuyer sur la touche **Echap**

Si vous allez au-delà du dixième de l'écran sur la gauche ou la droite, le terrain se décalera.

# Sauvegarder/charger et réinitialisation

Une fois que vous avez généré votre premier terrain, vous pouvez revenir au au menu et 4 choix s'offre à vous:

1) Reprendre le jeu en cliquant sur **Reprendre**.

2) Sauvegarder votre terrain généré ainsi que l'emplacement de votre personnage en cliquant sur **sauvegarder** . Vous pourrez alors choisir l'emplacement de votre fichier de sauvegarde et lui donner un nom.

3) En cliquant sur **paramètres** vous pouvez encore changer les options. De ce fait, les prochaines parties du terrain qui se généreront le feront avec ces nouvelle options. *une fois un terrain généré, l'option de changement de taille n'est plus disponible. Pour la rendre disponible il faut réinitialiser le terrain*

4) Vous pouvez réinitialiser le terrain en cliquant sur **Recommencer** (ATTENTION, CETTE OPERATION EST IRREVERSIBLE). Cela détruira le terrain et vous replacera au menu principal *les options reste les mêmes après une réinitialisation*.

Si vous possédez une sauvegarde, vous pouvez à tout moment la charger sur le jeu en cliquant sur **Charger** dans le menu principal.

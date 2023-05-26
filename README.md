# NO ESCAPE - Top Down Shooter Game
![home_screen](https://github.com/AlbertBS2/Top_Down_Shooter_Game/assets/110198818/30acdd74-faa7-4d84-9044-26b3409afe5c)

## Table of Contents
[I. Description](#description)  
[II. Objectives](#objectives)     
[III. Controls](#controls)    
[IV. Mechanics](#mechanics)   
[V. Contributing](#contributing)

## Description
The protagonist has been locked inside a building in an apocalypse. His only goal is to escape from there to find a safer place, but it will not be an easy task. On the way to the exit you will encounter enemies (zombies) with the aim of killing him, and the doors to the exit are blocked. To make his way through these obstacles he will use the weapons and ammunition found on the floor.

This game is aimed at a non-child audience as it is mostly about killing although no explicit content appears due to the simplicity of the project. The game will take place in games of average duration of about 10-15 minutes where the player will progress through the building and while the enemies will be stronger and stronger.

## Objectives
The game consists in eliminating all possible enemies, without the protagonist's life level remaining at 0, to get points and unlock other parts of the map by opening doors. The final goal is to find the way out to escape the building where the main character, the only one the player controls, is cornered.

There are three different ways to accomplish this ultimate goal and manage to escape:
  1. *Key Ring:* Open the final door to escape the building using the red key.
  2. *Capitalist:* Open the final door to escape the building using the coins obtained during the game.
  3. *Change of mind:* Open the final door to escape the building using the coins obtained during the game, but with the red key in possession.

If you fail to escape from the building, that is, when the character runs out of life, the user loses the game and a final Game Over screen appears.

![game_over](https://github.com/AlbertBS2/Top_Down_Shooter_Game/assets/110198818/ed66633a-ef32-429a-8667-ece19f944ef0)

## Controls
For this game we will use the two types of inputs that pygame allows us:
- *Mouse:* The mouse has the function of aiming, in the game screen the cursor is replaced by a cross that represents the aiming point of a gun. By moving this crosshair across the screen, the protagonist rotates so that he is always looking where he is aiming. The weapon is fired with the left mouse button.
- *Keyboard:* Serves to move our protagonist, using the WASD keys as if they were the direction arrows, although if desired the arrows can also be used. For interaction with other elements of the game, such as opening doors or collecting objects, the SPACE key is used. Finally, if you want to stop the game, you can access the pause menu through "P" or the "ESC" key.

## Mechanics
- *Coins:* Coins are the resources used when opening doors. They are obtained by eliminating enemies. Depending on the type of enemy, you get more or less coins for killing him. At all times the player has full control of the number of coins available through an indicator located in the upper left corner.
- *Ammunition:* Ammunition is necessary to be able to fire the weapon carried by the character controlled by the player. If he runs out, he has to search around the building until he finds some, or he can't kill the enemies. During the course of the game, you can collect ammunition found in various places in the building.
- *Life:* You have 5 life units. If an enemy manages to attack you, you lose one. If you miss all five, it's game over and you lose, as you haven't managed to complete the final objective.
- *Keys:* There are three types of keys according to color: green, blue and red. Each of them is used to open the door of the same color as the key. They are located in various places on the map, and can be collected at any time.

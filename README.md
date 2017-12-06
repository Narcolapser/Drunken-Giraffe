# Flight-Night
A app for helping homebrewers estimate their BAC.

## Purpose:

A homebrewer's helper. It estimates your blood alcohol based off of a couple of factors. But you specifically can enter the ABV of each drink as well as its size. This is useful for homebrewers where the ABV of the drinks can vary wildly. 

## Post-mortem:

After a fair bit of fiddling around I got an app good enough to demo. After some attempts of using it we discovered two problems: 

1. It is fiddly. And that is not likely to get better regardless of how much the interface is improved. 
2. Despite being correctly implemented, it's accuracy is dubious. So it's critical feature is shaky at best.

These two problems lead to the end of this project. But lets talk a litlte about how it works. 

![Screenshot 1](https://github.com/narcolapser/Flight-Night/blob/master/flight_night1.png?raw=true)

The algorithm for estimating your BAC requires your gender and body mass. So one of the first things is that information. I had plans to make this hiden away in settings in later iterations. Perhaps having profiles that you could swap between since some people would rather not have their weight so clearly visible. Next was drink name, which was mostly for fun record keeping reasons. Then you can select what the ABV is and the amount of oz. that you drank. Finally there is the drink button that logs the drink as drank.

![Screenshot 2](https://github.com/narcolapser/Flight-Night/blob/master/flight_night2.png?raw=true)

The other feature is the drink list. This is where you can edit mistakes you made in entries, see what you have had so far, how much each drink is contributing to your BAC, and start a new drinking session. This list is populated automatically everytime you open the app with your previous session's information. So even if it's been months and your phone has died since you last opened, your session is safe. One thing that never got exposed but I had plans to was the record of your previous sessions. 

Code for this project can be found on [Github](https://github.com/Narcolapser/Flight-Night)


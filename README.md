# Strava Activity Visualizer
An application to graph my Strava activities by year, using `Vue`, `Flask` and the `Strava API`.



https://user-images.githubusercontent.com/56971054/176025649-c1d291cf-7dc1-4ceb-b85b-dc98d72df864.mov



## About The Project
I love using [Strava](https://www.strava.com/) to record my weekly physical activities, especially as I find myself trying new sports all the time! I wanted to track the range of my physical activities, at any time of the year. Was I riding my bike more often than I skiied? I found it hard to monitor within the app and decided it was the perfect opportunity to try the Strava API. 

## Implementation
**Front-end: [Vue 2](https://v2.vuejs.org/)**  
The Vue app is located at `/client/`.
    
**Back-end: [Flask](https://flask.palletsprojects.com/en/2.1.x/), [Strava API](https://developers.strava.com/)**  
The back-end is located at `/`. When the application starts running, all of my activities uploaded on Strava are fetched using the Strava API. The activities are stored in a temporary variable that can be accessed by the front-end with a *GET* request. 
  
## Features
I wanted to create a clear, visual reprentation of my yearly outings with a simple UI. I created a button with [Figma](https://www.figma.com/) and exported the SVGs to animate them on hover. 

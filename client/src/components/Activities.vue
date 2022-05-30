<template>
	<div id="canva-container">
		<canvas id="canvas"></canvas>
	</div>
</template>

<script>
/* eslint linebreak-style: ["error", "windows"] */
import axios from 'axios';

export default {
    name: 'my-activities',
	props: {
		//receives the current year set by user (from YearPicker.vue through App.vue)
		currentYear: Number
	},
	watch: {
		currentYear(val, oldVal){
			if (val!==oldVal) this.displayActivities()
		}
	},
    data() {
        return {
            years: new Set(),
            sports: [],
            totalTime: [],
			activitiesObjects: [],
			firstTimeRunning: true,
			rectangleArray:[]
        };
    },
    methods: {
        getActivities() {
            const path = 'http://127.0.0.1:5000/activities';
            axios.get(path)
                .then((res) => {
                    this.msg = res.data;
                    let act = this.msg;
					let yearsSet = new Set();

					var activitiesArray = act.map(function(activities){
						return {
							"date": new Date(
									(activities.start_date_local).substring(0, 4),
									(activities.start_date_local).substring(6, 7),
									(activities.start_date_local).substring(9, 10),
								),
							"year": (activities.start_date_local).substring(0, 4),
							"sport": activities.type,
							"time":activities.moving_time
						}
					});
					//contains unique activities and years
					let sportSet = new Set();
					let sportArray;
					for (var key in activitiesArray){
						yearsSet.add(activitiesArray[key]['year']);
						sportSet.add(activitiesArray[key]['sport']);
					}
					//extracts values from set to an array
					sportArray = Array.from(sportSet);
					this.sports = sportArray;	//assigns sport arrray
					
					this.activitiesObjects = activitiesArray;

                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
		displayActivities(){
				//get all days of the week
				let xAxisLabels = this.getXAxisLabels();
				//gets all the activity durations of the year
				let yAxisLabels = this.getYAxisLabels();
				//creates an array of colours associated with a sport and gives 
				//an intital length of 0
				var sportColoursAndLength = this.assignColourAndLengthToSport();
				//tracks last id that added shapes
				let idOfLastDrawn = 0;	
				//width of rectangles
				const rectangleWidth = Math.round(window.innerWidth/xAxisLabels.length); 
				//canvas variables
				const canvas = document.getElementById("canvas");
				const c = canvas.getContext('2d');
				canvas.width = window.innerWidth;
				canvas.height = window.innerHeight;
				c.translate(0, canvas.height);
				c.scale(1,-1);
				//temporary array of exercise for the year
				let recArray = [];
				//instance variables
				let currentYear = this.currentYear;
				let activitiesObjects = this.activitiesObjects;

				//loops for each week of the year
				for (var x = 0; x < xAxisLabels.length-1;x++){
					//loops through activities and finds activities of the week
					for (var y = 0; y < activitiesObjects.length;y++){
						if (activitiesObjects[y]['year'] == currentYear){
							if ((activitiesObjects[y]['date'] > xAxisLabels[x]) && (activitiesObjects[y]['date'] < xAxisLabels[x+1])){
								//determines index of current sport
								let sportIndex = sportColoursAndLength.findIndex((obj => obj.sport == activitiesObjects[y]['sport']));
								//determine current sport rectangle height
								let thisRectangleHeight =Math.round( (activitiesObjects[y]['time']/yAxisLabels)*window.innerHeight);
								let colourUsed = sportColoursAndLength[sportIndex]['colour'];
								recArray.push({
									"sport": sportIndex,
									"index": x,
									"h": thisRectangleHeight,
									"colour": colourUsed
								});
							}
						}
					}
					//draws the prvious shapes again 
					// if (counter == 0){
						
					// 	for (var y = 0; y < activitiesObjects.length;y++){
					// 		if (activitiesObjects[y]['year'] == this.currentYear){
					// 			if ((activitiesObjects[y]['date'] > xAxisLabels[idOfLastDrawn]) && (activitiesObjects[y]['date'] < xAxisLabels[idOfLastDrawn+1])){
					// 				//determines index of current sport
					// 				let sportIndex = sportColoursAndLength.findIndex((obj => obj.sport == activitiesObjects[y]['sport']));
					// 				//determine current sport rectangle height
					// 				console.log("heey")
					// 				let thisRectangleHeight = (activitiesObjects[y]['time']/yAxisLabels)*window.innerHeight;
					// 				let currentTotalLength = sportColoursAndLength[sportIndex].length;
					// 				let rectangleHeight = Math.round(thisRectangleHeight) + currentTotalLength;

					// 				let colourUsed = sportColoursAndLength[sportIndex]['colour'];
					// 				c.fillStyle = colourUsed;
					// 				c.fillRect(rectangleWidth*x,yPosition,rectangleWidth,rectangleHeight);
					// 				//console.log(rectangleHeight);
					// 				yPosition += thisRectangleHeight;

					// 			}
					// 		}
					// 	}
					// }
				}
				
				for (var x = 0; x < xAxisLabels.length-1;x++){
					let yPosition = 0;
					let counter = 0;
					for (var sp = 0; sp < this.sports.length;sp++){
						let currentTotalLength = sportColoursAndLength[sp].length;
						c.fillStyle = sportColoursAndLength[sp].colour;
						c.fillRect(rectangleWidth*x,yPosition, rectangleWidth,currentTotalLength);
						yPosition += currentTotalLength;
						for (var act = 0;act< recArray.length;act++){
							//if same sport from the same week
							if (recArray[act].sport == sp && recArray[act].index == x){
								c.fillStyle = recArray[act].colour;
								c.fillRect(rectangleWidth*x,yPosition, rectangleWidth,recArray[act].h);
								yPosition += recArray[act].h;
								sportColoursAndLength[sp].length += recArray[act].h;  //updates total height
							}
						}
					}
				}
				
				// const canvas = document.getElementById("canvas");
				// const c = canvas.getContext('2d');
				// canvas.width = window.innerWidth;
				// canvas.height = window.innerHeight;
				// let idOfLastDrawn = 0;	//tracks last id that added shapes
				// const rectangleWidth = Math.round(window.innerWidth/xAxisLabels.length); 
				// 		for (var i = 0; i < xAxisLabels.length;i++){
				// 			//console.log(rectangleArray);
				// 			for (var j = 0; j < rectangleArray.length;j++){
				// 				if (rectangleArray[j].index == i){
				// 					//console.log(rec);
				// 					c.fillStyle = (rectangleArray[j].colour);
				// 					c.fillRect(rectangleWidth*i,rectangleArray[j].y,rectangleWidth,rectangleArray[j].h);
				// 					idOfLastDrawn = i;
				// 				}
				// 				else {
				// 					c.fillStyle = (rectangleArray[idOfLastDrawn].colour);
				// 					c.fillRect(rectangleWidth*i,rectangleArray[idOfLastDrawn].y,rectangleWidth,rectangleArray[idOfLastDrawn].h);
				// 				}
				// 			}
				// 		}
					
				

		},
		//create array of x-axis labels (weeks for current year)
		getXAxisLabels(){
			let currentYear = this.currentYear;
			let currentDay = new Date(currentYear,0,1);
			let yearBeingUsedRightNow = currentYear;
			let nextYear = currentYear +1;
			let xAxisLabel = [];   //holds labels
			while (yearBeingUsedRightNow < nextYear) {
				xAxisLabel.push(new Date(currentDay));
				currentDay.setDate(currentDay.getDate() + 7);
				yearBeingUsedRightNow = currentDay.getFullYear();
			}
			return xAxisLabel;

		},
		getYAxisLabels(){
			let totalActivityTime = 0;
			console.log(this.activitiesObjects);
			for (var i = 0; i < this.activitiesObjects.length;i++){
				if (this.activitiesObjects[i]['year'] == this.currentYear){
					totalActivityTime += this.activitiesObjects[i]['time'];
					
				}
			}
			return totalActivityTime;
		},
		assignColourAndLengthToSport(){
			let array = [];
			for (var x = 0; x < this.sports.length; x++){
				let randColour = "#" + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0').toUpperCase();
				array.push({
				"sport": this.sports[x],
				"colour": randColour,
				"length": Number(0)
				});
			}
			return array;
		}
	},
	mounted() {
		var a = this.getActivities();
		var aa = this.displayActivities();
		console.log(a);
		console.log(aa);
    },
}


</script>

<style scoped>
	#canva-container{
		width: 100vw;
		height: 100vh;
		overflow: hidden;
		position: relative;
		z-index: 3;
	}

	canvas {
		background-color: #161D28;
		width: 100%;
		height: 100%;
	}
</style>

<template>
  <div>
    <HoverBox
      v-if="valueOnHover == true"
      :sportOnHover="sportOnHover"
      :dateOnHover="dateOnHover"
      :valueOnHover="valueOnHover"
      :currentTimeMoving="getCurrentTimeMoving()"
      :totalTimeMoving="getTotalTimeMoving()"
      :y="yPosition"
      :x="xPosition"
    />
    <div id="canva-container">
      <canvas id="canvas"></canvas>
    </div>
  </div>
</template>

<script>
//jquery import
import $ from "jquery";

//random color palette selector
import Gradient from "javascript-color-gradient";

/* eslint linebreak-style: ["error", "windows"] */
import axios from "axios";
import HoverBox from "./HoverBox.vue";

export default {
  name: "my-activities",
  props: {
    //receives the current year set by user (from YearPicker.vue through App.vue)
    currentYear: Number,
  },
  components: { HoverBox },
  watch: {
    currentYear(val, oldVal) {
      if (val !== oldVal) this.displayActivities();
    },
  },
  data() {
    return {
      //contains the different years
      years: new Set(),
      //an array of all the unique sports performed
      sports: [],
      //total time moving
      totalTime: [],
      //
      activitiesObjects: [],
      firstTimeRunning: true,
      rectangleArray: [],
      sportOnHover: {}, //returns the sport on hover
      dateOnHover: {}, //returns the date that the user hovers
      valueOnHover: false, //returns true if mouse hovers data
      xPosition: "",
      yPosition: "",
      timeMovedForThisSport: "",
      totalActivityTime: "",
    };
  },
  methods: {
    getActivities() {
      const path = "http://127.0.0.1:5000/activities";
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          let act = this.msg;
          let yearsSet = new Set();
          var activitiesArray = act.map(function (activities) {
            return {
              date: new Date(
                activities.start_date_local.substring(0, 4),
                activities.start_date_local.substring(6, 7),
                activities.start_date_local.substring(9, 10)
              ),
              year: activities.start_date_local.substring(0, 4),
              sport: activities.type,
              time: activities.moving_time,
            };
          });
          //contains unique activities and years
          let sportSet = new Set();
          let sportArray;
          for (var key in activitiesArray) {
            yearsSet.add(activitiesArray[key]["year"]);
            //add spaces to pascal case
            let s = activitiesArray[key]["sport"];
            let newS = s.replace(/([A-Z])/g, " $1").trim(); //change pascal case
            activitiesArray[key]["sport"] = newS;
            sportSet.add(newS);
          }
          //extracts values from set to an array
          sportArray = Array.from(sportSet);
          this.sports = sportArray; //assigns sport arrray

          this.activitiesObjects = activitiesArray;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    //creates an array of colours
    pickColours() {
      const currentColor = new Gradient()
        .setColorGradient("#715AFF", "#CC2936")
        .setMidpoint(this.sports.length + 1)
        .getColors();
      return currentColor;
    },

    displayActivities() {
      //get all days of the week
      let xAxisLabels = this.getXAxisLabels();

      //gets all the activity durations of the year
      let yAxisLabels = this.getYAxisLabels();
      console.log(yAxisLabels);
      //creates an array of colours associated with a sport and gives
      //an intital length of 0
      var sportColoursAndLength = this.assignColourAndLengthToSport();
      //width of rectangles
      const rectangleWidth = Math.round(window.innerWidth / xAxisLabels.length);
      //canvas variables
      const canvas = document.getElementById("canvas");
      console.log(canvas);
      const c = canvas.getContext("2d");
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      c.translate(0, canvas.height);
      c.scale(1, -1);
      //temporary array of exercise for the year
      let recArray = [];
      //instance variables
      let currentYear = this.currentYear;
      let activitiesObjects = this.activitiesObjects;

      //loops for each week of the year
      for (var x = 0; x < xAxisLabels.length - 1; x++) {
        //loops through activities and finds activities of the week
        for (var y = 0; y < activitiesObjects.length; y++) {
          if (activitiesObjects[y]["year"] == currentYear) {
            if (
              activitiesObjects[y]["date"] > xAxisLabels[x] &&
              activitiesObjects[y]["date"] < xAxisLabels[x + 1]
            ) {
              //determines index of current sport
              let sportIndex = sportColoursAndLength.findIndex(
                (obj) => obj.sport == activitiesObjects[y]["sport"]
              );
              //determine current sport rectangle height
              let thisRectangleHeight = Math.round(
                (activitiesObjects[y]["time"] / yAxisLabels) * window.innerHeight
              );
              let colourUsed = sportColoursAndLength[sportIndex]["colour"];
              recArray.push({
                sport: sportIndex,
                index: x,
                h: thisRectangleHeight,
                colour: colourUsed,
              });
            }
          }
        }
      }
      //draws the shapes
      for (let x = 0; x < xAxisLabels.length; x++) {
        let yPosition = 0;
        for (let sp = 0; sp < this.sports.length; sp++) {
          let currentTotalLength = sportColoursAndLength[sp].length;
          c.fillStyle = sportColoursAndLength[sp].colour;
          c.fillRect(rectangleWidth * x, yPosition, rectangleWidth, currentTotalLength);
          yPosition += currentTotalLength;
          for (let act = 0; act < recArray.length; act++) {
            //if same sport from the same week
            if (recArray[act].sport == sp && recArray[act].index == x) {
              c.fillStyle = recArray[act].colour;
              c.fillRect(rectangleWidth * x, yPosition, rectangleWidth, recArray[act].h);
              yPosition += recArray[act].h;
              sportColoursAndLength[sp].length += recArray[act].h; //updates total height
            }
          }
        }
      }
    },
    //create array of x-axis labels (weeks for current year)
    getXAxisLabels() {
      let currentYear = this.currentYear;
      let currentDay = new Date(currentYear, 0, 1);
      let yearBeingUsedRightNow = currentYear;
      let nextYear = currentYear + 1;
      let xAxisLabel = []; //holds labels
      while (yearBeingUsedRightNow < nextYear) {
        xAxisLabel.push(new Date(currentDay));
        currentDay.setDate(currentDay.getDate() + 7);
        yearBeingUsedRightNow = currentDay.getFullYear();
      }
      return xAxisLabel;
    },
    getYAxisLabels() {
      let totalActivityTime = 0;
      for (var i = 0; i < this.activitiesObjects.length; i++) {
        if (this.activitiesObjects[i]["year"] == this.currentYear) {
          totalActivityTime += this.activitiesObjects[i]["time"];
        }
      }
      return totalActivityTime;
    },
    assignColourAndLengthToSport() {
      let array = [];
      for (var x = 0; x < this.sports.length; x++) {
        array.push({
          sport: this.sports[x],
          colour: this.pickColours()[x],
          length: Number(0),
        });
      }
      return array;
    },
    //returns moving time based on mouse position
    getCurrentTimeMoving() {
      return this.timeMovedForThisSport;
    },
    //returns time moved up until mouse (total)
    getTotalTimeMoving() {
      return this.totalActivityTime;
    },
  },
  mounted() {
    this.getActivities();
    this.displayActivities();

    function findPos(obj) {
      var curleft = 0,
        curtop = 0;
      if (obj.offsetParent) {
        do {
          curleft += obj.offsetLeft;
          curtop += obj.offsetTop;
        } while ((obj = obj.offsetParent));
        return { x: curleft, y: curtop };
      }
      return undefined;
    }

    function rgbToHex(r, g, b) {
      if (r > 255 || g > 255 || b > 255) throw "Invalid color component";
      return ((r << 16) | (g << 8) | b).toString(16);
    }
    let self = this;
    $("#canvas").mousemove(function (e) {
      let arrayWithData = self.assignColourAndLengthToSport();
      //console.log(arrayWithData)
      var pos = findPos(this);
      var x = e.pageX - pos.x;
      self.xPosition = x + 15;
      var y = e.pageY - pos.y;
      self.yPosition = y - 10;
      var coord = x;
      var c = this.getContext("2d");
      var p = c.getImageData(x, y, 1, 1).data;
      var hex = "#" + ("000000" + rgbToHex(p[0], p[1], p[2])).slice(-6);

      //gets current date based on mouse position
      let xLabel = self.getXAxisLabels();
      let screenWidth = window.innerWidth;
      let currentDate = xLabel[Math.ceil(coord / (screenWidth / xLabel.length))];
      //   console.log(currentDate);
      self.dateOnHover =
        currentDate.getUTCDate() +
        "/" +
        (currentDate.getMonth() + 1) +
        "/" +
        currentDate.getFullYear();

      //if mouse is over a shape, set current sport to shape
      for (let x = 0; x < arrayWithData.length; x++) {
        //console.log(arrayWithData[x]);
        if (
          arrayWithData[x].colour == hex &&
          hex != "#212A39" &&
          hex != "#F4EBE8" &&
          hex != "#161d28"
        ) {
          //calculates activity time until mouse location
          let totalActivityTimeUntilMouse = 0;
          let totalTimeUntilMouse = 0;
          //check all activities
          for (let j = 0; j < self.activitiesObjects.length; j++) {
            //add activity time if it comes before current date
            if (
              self.activitiesObjects[j].date < currentDate &&
              self.activitiesObjects[j].date.getFullYear() == currentDate.getFullYear() &&
              arrayWithData[x].sport == self.activitiesObjects[j].sport
            ) {
              totalActivityTimeUntilMouse += self.activitiesObjects[j]["time"];
            }
            //add all activity time until mouse
            if (
              self.activitiesObjects[j].date < currentDate &&
              self.activitiesObjects[j].date.getFullYear() == currentDate.getFullYear()
            ) {
              totalTimeUntilMouse += self.activitiesObjects[j]["time"];
            }
          }
          self.totalActivityTime = Number(totalTimeUntilMouse / 3600).toFixed(1);
          self.timeMovedForThisSport = Number(totalActivityTimeUntilMouse / 3600).toFixed(1);
          self.sportOnHover = arrayWithData[x].sport;
          self.valueOnHover = true;
          break;
        } else {
          //if mouse isn't over shapes, stop display
          self.valueOnHover = false;
        }
      }

      //   console.log(self.dateOnHover);

      //   console.log(self.sportOnHover);
    });
  },
};
</script>

<style scoped>
#canva-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
  z-index: 3;
}

canvas {
  background-color: #161d28;
  width: 100%;
  height: 100%;
}
</style>

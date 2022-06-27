<template>
  <div id="hover-box-container" :style="{ top: y + 'px', left: x + 'px' }">
    <div>
      {{ sportOnHover }}
    </div>
    <div>
      {{ dateOnHover }}
    </div>
    <div id="time">Time: {{ currentTimeMoving }}/{{ totalTimeMoving }} hrs</div>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "HoverBox",
  props: {
    sportOnHover: String,
    dateOnHover: String,
    valueOnHover: Boolean,
    x: Number,
    y: Number,
    totalTimeMoving: String,
    currentTimeMoving: String,
  },
};
</script>
<style scoped>
svg,
svg * {
  pointer-events: visible;
}
#hover-box-container {
  fill: #f4ebe8;
  font-size: 1.5vw;
  font-family: "Roboto", sans-serif;
  text-align: center;
  position: fixed;
  display: flex;
  flex-direction: column;

  z-index: 10;
  max-width: 15%;
  height: auto;
  color: white;
  border: 1px solid white;
  padding: 1%;
  transition-delay: 1000;
}
#time {
  padding-top: 7%;
}
</style>

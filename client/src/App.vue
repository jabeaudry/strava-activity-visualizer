<template>
  <div id="app">
    <Activities :currentYear="currentYearSelected" />
    <YearPicker
      :currentYear="currentYearSelected"
      @changeYearUp="currentYearSelected = currentYearSelected + 1"
      @changeYearDown="currentYearSelected = currentYearSelected - 1"
    />
  </div>
</template>

<script>
import Activities from "./components/Activities.vue";
import YearPicker from "./components/YearPicker.vue";

export default {
  components: {
    Activities,
    YearPicker,
  },
  data() {
    return {
      //stores the year selected by the user in YearPicker
      currentYearSelected: new Date().getFullYear(),
      firstTimeRunning: true,
    };
  },
  mounted() {
    if (this.firstTimeRunning) {
      this.currentYearSelected = 2022;
      this.firstTimeRunning = false;
    }
  },
};
</script>

<style>
* {
  margin: 0;
  background-color: #161d28;
  padding: 0;
}
</style>

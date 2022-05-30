<template>
<div id="app">
    <Activities 
		:currentYear="currentYearSelected"   
	/>
	<YearPicker 
		:currentYear="currentYearSelected"
		@changeYearUp="currentYearSelected = currentYearSelected+1"
		@changeYearDown="currentYearSelected = currentYearSelected-1"
	/>
</div>
</template>

<script>
import Activities from './components/Activities.vue'
import YearPicker from './components/YearPicker.vue'

export default {
    components: {
        Activities, YearPicker
    },
	data(){
		return{
			
			currentYearSelected: new Date().getFullYear()
			
		}
	}
}
</script>

<style>


* {
    margin: 0;
    
	background-color: #161D28;
}
</style>

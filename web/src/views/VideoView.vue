<script setup>
import { ref } from 'vue'
import VideoPlayer from '../components/VideoPlayer.vue';
import { useRoute } from 'vue-router';

const route = useRoute()

</script>

<template>
	<div>
		<!-- <pre>{{ route.query }}</pre> -->
		<VideoPlayer :videoUrl="route.query.videoUrl" :timeStamp="route.query.timeStamp"/>
	</div>
</template>

<style scoped>
	div {
		background: darkgray;
		margin: 0;
		width: 100%;
		position: relative;
		box-sizing: border-box;
		overflow: hidden;
	}
</style>

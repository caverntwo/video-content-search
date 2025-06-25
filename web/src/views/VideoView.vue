<script setup>
import { ref } from 'vue'
import VideoPlayer from '../components/VideoPlayer.vue';
import { useRoute } from 'vue-router';

const route = useRoute()

</script>

<template>
	<div>
		<!-- <pre>{{ route.query }}</pre> -->
		<VideoPlayer :videoId="route.query.videoId" :videoUrl="route.query.videoUrl" :frame="route.query.frame" :timeStamp="route.query.timeStamp" :title="route.query.title" :thumbnail="route.query.thumbnail" />
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

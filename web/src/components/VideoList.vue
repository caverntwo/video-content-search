<script setup>
import { ref, watch } from 'vue'
import VideoCard from './VideoCard.vue';

defineProps({
	videos: {
		type: Array,
		required: false
	}
})

</script>

<template>
	<h1>Videos</h1>

	<div class="video-list-container">
		<VideoCard v-for="(video, i) in videos" :key="i" :videoId="video.id" :thumbnail="video.thumbnail" :videoUrl="video.video" :timeStamp="video.time" :frame="video.frame" :title="video.id"/>
	</div>
</template>

<style scoped>
.video-list-container {
	background-color: darkgray;
}
</style>

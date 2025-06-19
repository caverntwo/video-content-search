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
		<VideoCard v-for="(video, i) in videos" :key="i" :thumbnail="video.thumbnail" :videoUrl="video.video" :timeStamp="video.frame" :title="video.video"/>
	</div>
</template>

<style scoped>
.video-list-container {
	background-color: darkgray;
}
</style>

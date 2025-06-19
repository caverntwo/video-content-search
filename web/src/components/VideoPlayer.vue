<script setup>
import { ref } from 'vue'

const props = defineProps({
	videoUrl: {
		type: String,
		required: true
	},
	thumbnail: {
		type: String,
		required: true
	},
	timeStamp: {
		type: Number,
		required: false
	},
	title: {
		type: String,
		required: true
	}
})

const videoElement = ref(null)

function videoloaded() {
	videoElement.value.currentTime = props.timeStamp / 100;
	videoElement.value.volume = 0.1;
	videoElement.value.muted = true;
	videoElement.value.play();
}

</script>

<template>

	<div class="video-container">
		<video id="main-video" ref="videoElement" controls :src="'http://127.0.0.1:3456' + videoUrl" @loadedmetadata="videoloaded"></video>
	</div>
	<h2>Title</h2>
</template>

<style scoped>
	.video-container {
		background-color: darkslategray;
	}
	video {
		width: 100%;
		min-width: 800px;
		padding: 10px;
		box-sizing: border-box;
	}
</style>
<script setup>
import { ref, computed } from 'vue'



const props = defineProps({
	videoId: {
		type: String,
		required: true
	},
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
	frame: {
		type: Number,
		required: false
	},
	title: {
		type: String,
		required: true
	}
})

const videoElement = ref(null)
const videoTime = ref(0)
const formData = ref({
	text: '',
	start: 0,
	end: 0
})
const submitResult = ref('')


const updateTime = () => {
	if (videoElement.value) {
		videoTime.value = videoElement.value.currentTime;
	}
}

const formattedVideoTime = computed(() => {
	return formatTime(videoTime.value * 1000)
});

async function submitVideoResult() {
	console.log("Submitting result...")
	formData.value.start = videoTime;
	formData.value.end = videoTime;
	const options = {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(formData.value)
	}
	const res = await fetch('http://127.0.0.1:3456/submit/' + props.videoId, options)
		.then(res => res.json())
		.then(raw => {
			console.log("response: " , raw);
			return raw;
		})
	submitResult.value = JSON.stringify(res);
}

function videoloaded() {
	videoElement.value.currentTime = props.timeStamp / 1000;
	videoElement.value.volume = 0.1;
	videoElement.value.muted = true;
	videoElement.value.play();
}

function formatTime(millies) {
	const totalSeconds = Math.floor(millies / 1000);
	const minutes = Math.floor(totalSeconds / 60);
	const seconds = totalSeconds % 60;
	return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

</script>

<template>

	<div class="video-container">
		<video id="main-video" ref="videoElement" controls :src="'http://127.0.0.1:3456' + videoUrl" @loadedmetadata="videoloaded" @timeupdate="updateTime"></video>
	</div>
	<h2>Video {{ title }}</h2>
	<p>Video ID: {{ videoId }}</p>
	<p>URL: {{ videoUrl }}</p>
	<form @submit.prevent="submitVideoResult">
		<div class="form-row">
			<label>Submission Text: </label>
			<input type="text" id="submission-text" name="text" placeholder="my submission text" v-model="formData.text"></input>
		</div>
		<div class="form-row">
			<label>Start Timestamp: </label>
			<input type="text" id="submission-start-time" name="start" :value="formattedVideoTime" readonly></input>
		</div>
		<div class="form-row">
			<label>End Timestamp: </label>
			<input type="text" id="submission-end-time" name="end" :value="formattedVideoTime" readonly></input>
		</div>
		<div class="form-row">
			<button type="submit">Submit</button>
		</div>
	</form>
	<div class="form-row">
		<textarea :value="submitResult" placeholder="Result appears here..."></textarea>
	</div>

	<h2>Referenced Shot</h2>
	<div class="image-container">
		<img id="thumbnail-display" :src="'http://127.0.0.1:3456' + thumbnail"></img>
	</div>
	<p>Timestamp: {{ formatTime(timeStamp) }}</p>
	<p>Thumbnail URL: {{ thumbnail }}</p>

</template>

<style scoped>
	.image-container {
		background-color: darkslategray;
		position: relative;
	}
	image {
		width: 100%;
		min-width: 400px;
		padding: 10px;
		box-sizing: border-box;
	}
	.video-container {
		background-color: darkslategray;
	}
	video {
		width: 100%;
		min-width: 800px;
		padding: 10px;
		box-sizing: border-box;
	}
	.form-row {
		display: block;
	}
	.form-row > * {
		position: relative;
	}
	input {
		display: inline-block;
	}
	textarea {
		width: 100%;
		box-sizing: border-box;
	}
	button {
		margin: 10px 20px;
	}
</style>
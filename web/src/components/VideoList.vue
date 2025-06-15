<script setup>
import { ref } from 'vue'

defineProps({
	searchTerms: {
		type: String,
		required: false
	}
})

watch({
	searchTerms: {
		immediate: true,
		handler(newTerms){
			loadVideos(newTerms);
		}
	}
})

async function loadVideos(search) {
	const options = {
		method: "GET"
	}
	const res = await fetch('http://127.0.0.1:3456/videos?search=' + search)
		.then(res => res.text())
		.then(text => {
			console.log("response: " + text);
		})
}
</script>

<template>
	<h1>Videos</h1>

	<div class="video-list-container">
		
	</div>
</template>

<style scoped>
.video-list-container {
	background-color: blueviolet;
}
</style>

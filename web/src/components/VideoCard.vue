<script setup>
import { ref, watch } from 'vue'
import { RouterLink } from 'vue-router';

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
		type: String,
		required: false
	},
	title: {
		type: String,
		required: true
	}
})

// watch(() => props.videoUrl, (newVideoUrl) => {

// })

</script>

<template>
	<RouterLink :to="{name: 'Player', query:props}">
		<div class="video-card-container card">
			<img :src="'http://127.0.0.1:3456' + thumbnail" width="400px">
			<div class="video-info">
				<p>{{ title }}</p>
				<p>{{ timeStamp / 1000 }} s</p>
			</div>
		</div>
	</RouterLink>
</template>

<style scoped>
.video-list-container {
	background-color: darkgray;
}
.video-info {
	background-color: beige;
}
</style>

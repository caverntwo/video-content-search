<script setup>
import { ref } from 'vue'
import VideoPlayer from '../components/VideoPlayer.vue';
import { useRoute } from 'vue-router';

const route = useRoute()

</script>

<template>
	<div>
		<pre>{{ route.query }}</pre>
		<VideoPlayer :videoUrl="route.query.videoUrl" :timeStamp="route.query.timeStamp"/>
	</div>
</template>

<style scoped>

</style>

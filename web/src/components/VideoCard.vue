<script setup>
import { ref } from 'vue'

defineProps({
	videoUrl: {
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

</script>

<template>
  <div class="video-card-container">
    <p>{{ title }}</p>
  </div>
</template>

<style scoped>
.video-list-container {
  background-color: blueviolet;
}
</style>

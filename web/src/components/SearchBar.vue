<script setup>
import { ref } from 'vue'

defineProps({
	searchTerms: {
		type: String,
		required: false
	}
})
const emit = defineEmits(['search'])
</script>

<template>
	<div class="search-bar-container">
		<h1 class="green">{{ source }}</h1>
		<input :value="searchTerms" @input="(e) => emit('search', e.target.value)" placeholder="Enter search terms..."></input>
	</div>
</template>

<style scoped>
.search-bar-container {
	background-color: goldenrod;
}
</style>

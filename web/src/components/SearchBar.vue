<script setup>
import { ref } from 'vue'

const searchTerms = ref('')
</script>

<template>
	<div class="search-bar-container">
		<h1 class="green">{{ source }}</h1>
		<input v-model="searchTerms" placeholder="Enter search terms..."></input>
		<button @click="emit('search', sourceText)">Search</button>
	</div>
</template>

<style scoped>
.search-bar-container {
	background-color: goldenrod;
}
</style>

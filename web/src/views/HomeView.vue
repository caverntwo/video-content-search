<script setup>
import { onMounted, ref } from 'vue'
import SearchBar from '../components/SearchBar.vue'
import VideoList from '../components/VideoList.vue';
import { useAppStore } from '../stores/app';


const appStore = useAppStore()

const searchTerms = ref(appStore.search)
const videos = ref([])
const info = ref('None')

onMounted(() => {
	console.log("search " + appStore.search);
	loadInfo()
	if (searchTerms.value)
		loadVideos(searchTerms.value);
})


async function search(s) {
	searchTerms.value = s;
	console.log("searching " + s);
	appStore.setSearch(s);
	await loadVideos(s);
}

async function loadInfo() {
	const options = {
		method: "GET"
	}
	const res = await fetch('http://127.0.0.1:3456/info')
		.then(res => res.json())
		.then(raw => {
			console.log("response: " , raw);
			return raw;
		})
	info.value = JSON.stringify(res);
}

async function loadVideos(search) {
	const options = {
		method: "GET"
	}
	const res = await fetch('http://127.0.0.1:3456/videos?search=' + search)
		.then(res => res.json())
		.then(raw => {
			console.log("response: " , raw);
			return raw;
		})
	videos.value = res;
}
</script>

<template>
	<div>
		<h1>Video Content Search</h1>
		<h2>Current Task</h2>
		<p>{{ info }}</p>
	</div>
	<SearchBar @search="search" :searchTerms="searchTerms"/>
	<VideoList :videos="videos"/>
</template>

<style scoped>
.logo {
	height: 6em;
	padding: 1.5em;
	will-change: filter;
	transition: filter 300ms;
}
.logo:hover {
	filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
	filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

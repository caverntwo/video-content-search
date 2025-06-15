<script setup>
import { ref } from 'vue'

defineProps({
	hls_url: {
		type: String,
		required: true
	},
	timeStamp: {
		type: String,
		required: CSSFontFeatureValuesRule
	}
})

document.addEventListener('DOMContentLoaded', () => {
			var video = document.getElementById('main-video');
			var source = hls_url;
			//var source = "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8";
			console.log(source);
			const defaultOptions = {};

			if (!Hls.isSupported()) {
				video.src = source;
				console.log("fallback: " + source);
				var player = new Plyr(video, defaultOptions);
			} else {
				// For more Hls.js options, see https://github.com/dailymotion/hls.js
				const hls = new Hls();
				hls.loadSource(source);
				console.log("Source loaded");
				console.log(hls);

				// From the m3u8 playlist, hls parses the manifest and returns
				// all available video qualities. This is important, in this approach,
				// we will have one source on the Plyr player.
				hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {

					console.log("parsing manifest...");
					// Transform available levels into an array of integers (height values).
					const availableQualities = hls.levels.map((l) => l.height)
					availableQualities.unshift(0) //prepend 0 to quality array
					console.log(hls.levels);

					// Add new qualities to option
					defaultOptions.quality = {
						default: 0, //Default - AUTO
						options: availableQualities,
						forced: true,
						onChange: (e) => updateQuality(e),
					}
					// Add Auto Label 
					defaultOptions.i18n = {
						qualityLabel: {
							0: 'Auto',
						}
					}

					defaultOptions.debug = true
				
					defaultOptions.volume = 0;

					hls.on(Hls.Events.LEVEL_SWITCHED, function (event, data) {
						var span = document.querySelector(".plyr__menu__container [data-plyr='quality'][value='0'] span")
						if (hls.autoLevelEnabled) {
							span.innerHTML = `AUTO (${hls.levels[data.level].height}p)`
						} else {
							span.innerHTML = `AUTO`
						}
					})

					// Initialize new Plyr player with quality options
					var player = new Plyr(video, defaultOptions);
				});

				hls.attachMedia(video);
				console.log("attach");
				window.hls = hls;
			}

			function updateQuality(newQuality) {
				if (newQuality === 0) {
					window.hls.currentLevel = -1; //Enable AUTO quality if option.value = 0
				} else {
					window.hls.levels.forEach((level, levelIndex) => {
						if (level.height === newQuality) {
							console.log("Found quality match with " + newQuality);
							window.hls.currentLevel = levelIndex;
						}
					});
				}
			}
		});
</script>

<template>
	<h1>{{ hls_url }}</h1>

	<div class="video-container">
		<video id="main-video" crossorigin controls data-plyr-config='{ "volume": 0 }' playsinline autoplay debug></video>
	</div>
</template>

<style scoped>
	div {
		background-color: red;
	}
</style>

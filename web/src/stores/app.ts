import { defineStore } from "pinia"
import { ref } from "vue"

export const useAppStore = defineStore('app', () => {
  const search = ref('')

	function setSearch(newValue :string) {
		search.value = newValue;
	}


  return { search, setSearch }
})
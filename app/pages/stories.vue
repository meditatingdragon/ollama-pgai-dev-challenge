<template>
  <div class="flex place-content-center my-4">
    <div class="w-8/12">
      <label class="form-control mx-4 w-full">
        <span class="label-text text-xl font-bold">Stories</span>
        <div class="label">
          <span class="label-text">Find stories about...</span>
        </div>
        <div class="flex">
          <input
            type="text"
            v-model="searchText"
            placeholder="Search here (e.g. spaceships)"
            class="input input-bordered w-full mr-2"
          />
          <button class="btn btn-success btn-md" @click="findStories">
            Find Stories
          </button>
        </div>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const searchText = ref("");
const suggestions = ref("");
const wordCount = computed(() => {
  const text = editorText.value;
  return text.split(" ")?.length ? text.split(" ")?.length : 0;
});

async function findStories() {}

async function getSuggestions() {
  const response = await $fetch("http://localhost:8080/suggestions", {
    method: "POST",
    body: {
      editor_text: editorText.value,
    },
  });
  suggestions.value = processResponse(response[0]);
}

function processResponse(response) {
  if (response) {
    const chat = response.ollama_chat_complete;
    const message = chat?.message?.content;
    return message;
  }
}
</script>

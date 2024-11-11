<template>
  <div class="container mx-auto">
    <div class="editor">
      <label class="input input-bordered flex items-center gap-2 mx-4">
        Title
        <input
          type="text"
          class="grow"
          placeholder="Maverick Days"
          v-model="title"
        />
      </label>
      <label class="form-control">
        <div class="label mx-4">
          <span class="label-text text-lg font-bold">Editor</span>
        </div>

        <textarea
          class="textarea textarea-bordered h-24 p-4 mx-4"
          v-model="editorText"
        ></textarea>
        <div class="label mx-4">
          <span class="label-text-alt"></span>
          <span class="label-text-alt">{{ wordCount }} words</span>
        </div>
      </label>
      <div class="align-end mx-4 w-full">
        <button class="btn btn-success btn-sm" @click="saveStory">
          Save Story
        </button>
      </div>
    </div>
    <div class="text-lg font-bold m-4 min-h-96">
      <div class="my-6">
        Personalized AI Assistant
        <button class="btn btn-info btn-sm" @click="getSuggestions">
          Help complete my story.
        </button>
      </div>
      <article class="prose-sm p-4 bg-base-300 rounded" v-if="suggestions">
        <p>{{ suggestions }}</p>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const editorText = ref("It was a dark and stormy night...");
const suggestions = ref("");
const title = ref("");
const wordCount = computed(() => {
  const text = editorText.value;
  return text.split(" ")?.length ? text.split(" ")?.length : 0;
});

async function getSuggestions() {
  const response = await $fetch("http://localhost:8080/suggestions", {
    method: "POST",
    body: {
      editor_text: editorText.value,
    },
  });
  suggestions.value = processResponse(response[0]);
}

async function saveStory() {
  const response = await $fetch("http://localhost:8080/stories", {
    method: "POST",
    body: {
      title: title.value,
      content: editorText.value,
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

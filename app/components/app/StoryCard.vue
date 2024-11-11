<template>
  <div
    class="card bg-base-100 w-96 shadow-xl p-2 hover:bg-slate-200"
    @click="goToStory"
  >
    <div class="card-body">
      <h2 class="card-title">{{ story.title }}</h2>
      <div class="max-h-10 text-sm overflow-hidden">{{ story.content }}</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps(["story"]);

async function goToStory() {
  await navigateTo("/stories/" + props.story.id);
}
</script>

<template>
  <div class="container mx-auto my-5">
    <div class="flex place-content-center">
      <div class="py-2">
        <label class="font-bold font-xl">
          {{ story.title }}
        </label>
        <article class="prose">
          {{ story.content }}
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
const route = useRoute();

const { data } = await useAsyncData("story", () =>
  $fetch(`http://localhost:8080/stories/${route.params.id}`)
);

const story = reactive(data);
</script>

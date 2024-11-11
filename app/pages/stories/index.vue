<template>
  <div class="flex place-content-center my-4 w-8/12">
    <label class="form-control mx-4 w-full">
      <span class="label-text text-xl font-bold">Stories</span>
      <div class="label">
        <span class="label-text">Find stories about...</span>
      </div>
    </label>
  </div>
  <div class="w-full flex flex-row flex-wrap place-content-center">
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
    <div class="w-full flex flex-row flex-wrap place-content-center my-2">
      <StoryCard :story="story" v-for="story in stories" class="m-2" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import StoryCard from "~/components/app/StoryCard.vue";

const searchText = ref("");

const { data } = await useAsyncData("stories", () =>
  $fetch("http://localhost:8080/stories")
);

const stories = reactive(data);
</script>

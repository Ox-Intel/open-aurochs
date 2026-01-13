import { defineStore } from "pinia";

export const useAurochsData = defineStore("aurochsData", {
  state: () => window.aurochs.data,
});
export const useAurochsRoot = defineStore("aurochsRoot", {
  state: () => window.aurochs,
});

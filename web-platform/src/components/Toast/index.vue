<template lang="pug" >
   div
    v-snackbar(
      v-for="toast in toasts"
      :key="toast.id"
      v-model="toast.show"
      :color="toast.color"
      :timeout="4000"
      location="top right"
      :multi-line="!!toast.title"
      transition="slide-x-reverse-transition"
      :style="{ top: `${toast.topOffset}px` }"
      @update:modelValue="handleSnackbarUpdate(toast.id, $event)"
    )
      .d-flex.align-center
        v-icon(:icon="toast.icon" class="mr-3")
        .flex-grow-1
          div.font-weight-bold.comic-font.mb-1(v-if="toast.title") {{ toast.title }}
          div.comic-font {{ toast.message }}
        v-btn(
          icon="mdi-close"
          size="small"
          variant="text"
          @click="removeToast(toast.id)"
        )
  </template>
  
  <script setup>
  import { useToast } from '@/utils/toast'
  
  const { toasts, removeToast, handleSnackbarUpdate } = useToast()
  </script>
  
  <style scoped>
    .comic-font {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    }
  
  :deep(.v-snackbar) {
    position: fixed !important;
  }
  
  :deep(.v-snackbar__wrapper) {
    max-width: 400px;
    min-width: 320px;
  }
  
  @media (max-width: 640px) {
    :deep(.v-snackbar__wrapper) {
      min-width: unset;
      max-width: calc(100vw - 40px);
    }
  }
  </style>
<template lang="pug">
  v-container.pa-4(style="max-width: 1200px; min-height: 100px")
    v-card.rounded-xl.elevation-5.music-app-card
      div.app-header.pa-6.rounded-t-xl.text-left
        h1.text-h3.font-weight-bold.text-grey-lighten-2 Free Online Key Chord Predictor
        p.text-body-1.text-grey-lighten-2.mt-2.font-weight-bold
          | Instantly detect the key and chords of your song using AI.
          | Upload your audio to reveal its harmonic structure in seconds.
      div.app-content.pa-6
        div(v-if="waveReady").text-center.mb-2.key-display
          h2(v-if="!loadingKey").text-subtitle-1.font-weight-medium.text-grey-darken-2 MAIN CHORD
          h2(v-if="loadingKey").text-subtitle-1.font-weight-medium.text-grey-darken-2 Wait to detect
          h1.text-h1.font-weight-bold.gradient-text(v-if="!loadingKey") {{ detectedKey || '...' }}
          v-progress-circular(indeterminate color="primary" v-if="loadingKey")
        div.mt-1.text-center(v-if="currentChord")
          v-chip(color="primary" variant="elevated" size="large" class="chord-chip px-6 py-2")
            v-icon(start class="mr-2") mdi-music-note
            span.text-subtitle-1 Current Chord: {{ currentChord }}
        
        WaveformPlayer(
          v-if="waveReady"
          :audio-file="selectedFile"
          :is-playing="isPlaying"
          :audio-duration="audioDuration"
          :chords="chords"
          @play="onPlay"
          @pause="onPause"
          @delete="onDeleteAudio"
          @ready="onWaveReady"
          @finish="onWaveFinish"
          @chord-change="onChordChange"
          @time-update="onTimeUpdate"
        )
        
        v-btn.upload-btn.mt-5(size="large" color="primary" v-if="waveReady" @click="onDetectKey" :disabled="loadingKey") Detect KeyChord
        div.upload-container.mt-8.pa-6.rounded-lg(v-if="!waveReady")
          input(type="file" accept="audio/*" @change="onFileChange" hidden ref="fileInput")
          div.d-flex.flex-column.align-center
            v-icon(size="64" color="primary") mdi-cloud-upload
            span.font-weight-medium.text-h6.mt-4 Choose a file or drag it here
            span.text-caption.text-grey-darken-1.mt-1 Supported formats: .mp3, .wav, .flac
            v-btn.upload-btn.mt-6(size="large" color="primary" @click="selectFile" prepend-icon="mdi-music-note")
              | Upload Audio
</template>
  
<script setup lang="ts">
import { ref, nextTick } from 'vue'
import WaveformPlayer from '@/components/WaveformPlayer/index.vue' // Import component mới
import api from '@/plugins/axios'
 
const detectedKey = ref<string | null>('')
const loadingKey = ref(false)
const currentChord = ref('')
const chords = ref([
  { chord: 'C', start_time: 0, end_time: 3.0 },
  { chord: 'D', start_time: 3.0, end_time: 6.0 },
  { chord: 'E', start_time: 6.0, end_time: 10.0 },
  { chord: 'N', start_time: 10.0, end_time: 15.0 },
  { chord: 'G', start_time: 15.0, end_time: 20.0 },
])
const fileInput = ref<HTMLInputElement | null>(null)
const isPlaying = ref(false)
const waveReady = ref(false)
const audioDuration = ref(0)
const selectedFile = ref<File | null>(null)

const selectFile = () => {
  fileInput.value?.click()
}

const onDetectKey = async () => {
  loadingKey.value = true  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  const response = await api.post('api/predict-chord', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  if (response.status === 200){
    loadingKey.value = false
    detectedKey.value = response.data.key
    chords.value = response.data.chord_segments
  }
} 

const onFileChange = async (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  console.log(file)
  
  if (file) {
    selectedFile.value = file
    waveReady.value = true
    isPlaying.value = false
    await nextTick()
  }
}

// Handlers for WaveformPlayer events
const onPlay = () => {
  isPlaying.value = true
}

const onPause = () => {
  isPlaying.value = false
}

const onDeleteAudio = () => {
  isPlaying.value = false
  waveReady.value = false
  detectedKey.value = null
  audioDuration.value = 0
  loadingKey.value = false
  selectedFile.value = null
}

const onWaveReady = (duration: number) => {
  audioDuration.value = duration
  isPlaying.value = false
}

const onWaveFinish = () => {
  isPlaying.value = false
}

const onChordChange = (chord: string) => {
  currentChord.value = chord
}

const onTimeUpdate = (time: number) => {
  // Handle time updates if needed
  console.log('Current time:', time)
}
</script>
  
<style scoped>
.music-app-card {
  overflow: hidden;
  border: none;
  animation: fadeIn 0.7s ease-out;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.app-header {
  background: linear-gradient(135deg, #775CF0 0%, #4A3AFF 100%);
  color: white;
  padding: 48px;
  border-radius: 24px 24px 0 0;
  position: relative;
  overflow: hidden;
}

.app-header::after {
  content: '';
  position: absolute;
  bottom: -30px;
  right: -30px;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.07);
  border-radius: 50%;
  z-index: 0;
}

.app-header h1,
.app-header p {
  z-index: 1;
  position: relative;
}

.app-header h1 {
  font-size: 2.8rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 700;
  letter-spacing: 1px;
}

.app-header p {
  font-size: 1.35rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 600;
  margin-top: 12px;
}

.key-display {
  padding: 24px 0;
}

.gradient-text {
  background: linear-gradient(135deg, #775CF0, #4A3AFF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 4rem;
  font-weight: bold;
}

.upload-container {
  border-width: 3px !important;
  border-style: dashed !important;
  border-color: #775CF0 !important;
  background-color: #f9f9fc;
  text-align: center;
  border-radius: 16px;
  transition: 0.3s;
}

.upload-container:hover {
  border-color: #775CF0;
  background-color: #f3f2ff;
  box-shadow: 0 10px 24px rgba(124, 58, 237, 0.12);
}

.upload-btn {
  min-width: 200px;
  border-radius: 12px;
  padding: 14px 28px;
  font-weight: 600;
  text-transform: none;
  box-shadow: 0 6px 16px rgba(74, 58, 255, 0.25);
  transition: 0.3s;
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 58, 255, 0.35);
}

.chord-chip {
  font-weight: 600;
  font-size: 1.1rem;
  background: linear-gradient(135deg, #775CF0, #4A3AFF);
  color: white;
  box-shadow: 0 4px 12px rgba(74, 58, 255, 0.15);
}

@media (max-width: 768px) {
  .app-header {
    padding: 24px;
  }

  .app-header h1 {
    font-size: 2rem;
  }

  .app-header p {
    font-size: 1.1rem;
  }

  .gradient-text {
    font-size: 3rem;
  }

  .upload-btn, .detect-btn {
    padding: 12px 20px;
    min-width: 160px;
  }

  .key-display {
    padding: 16px 0;
  }

  .chord-chip {
    font-size: 1rem;
    padding: 8px 16px !important;
  }
}

@media (max-width: 480px) {
  .app-header h1 {
    font-size: 1.8rem;
  }

  .app-header p {
    font-size: 1rem;
  }

  .gradient-text {
    font-size: 2.5rem;
  }

  .upload-container {
    padding: 24px 16px;
  }

  .upload-btn {
    width: 100%;
    margin-top: 16px;
  }

  .chord-chip {
    width: 100%;
    justify-content: center;
  }
}

.comic-font {
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
}
</style>
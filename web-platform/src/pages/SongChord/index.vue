<template lang="pug">
  v-container.pa-4
    v-card.rounded-xl.elevation-5.music-app-card
      div.app-header.pa-6.rounded-t-xl.text-left
        h1.text-h3.font-weight-bold.text-grey-lighten-2 Free Online Key Chord Predictor
        p.text-body-1.text-grey-lighten-2.mt-2.font-weight-bold
          | Instantly detect the key and chords of your song using AI.
          | Upload your audio to reveal its harmonic structure in seconds.
      div.app-content.pa-6
        div(v-if="waveReady").text-center.mb-8.key-display
          h2.text-subtitle-1.font-weight-medium.text-grey-darken-2 MAIN CHORD
          h1.text-h2.font-weight-bold.gradient-text(v-if="!loadingKey") {{ detectedKey || '...' }}
          v-progress-circular(indeterminate color="primary" v-if="loadingKey")
        div.mt-4.text-center(v-if="currentChord")
          v-chip(color="primary" variant="elevated" size="large" class="chord-chip px-6 py-2")
            v-icon(start class="mr-2") mdi-music-note
            span.text-subtitle-1 Current Chord: {{ currentChord }}
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
import { ref, onMounted, nextTick } from 'vue'
import WaveSurfer from 'wavesurfer.js'
import api from '@/plugins/axios'
 
const detectedKey = ref<string | null>('G')
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
const waveformContainer = ref<HTMLDivElement | null>(null)
let wavesurfer: WaveSurfer | null = null
const isPlaying = ref(false)
const waveReady = ref(false)
const audioDuration = ref(0)

const formatTime = (timeInSeconds: number): string => {
  const minutes = Math.floor(timeInSeconds / 60)
  const seconds = Math.floor(timeInSeconds % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = async (e: Event) => {
  // Always reset the input value so the same file can be uploaded again
  if (fileInput.value) fileInput.value.value = ''
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  console.log(file)
  
  if (file) {
    const formData = new FormData()
    formData.append('file', file)
    loadingKey.value = true
    const response = await api.post('api/predict-chord', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    detectedKey.value = response.data.key
    chords.value = response.data.chord_segments

    if (waveformContainer.value) {
      if (wavesurfer) {
        wavesurfer.destroy()
      }
      

      // Create new wavesurfer instance with modern styling
      wavesurfer = WaveSurfer.create({
        container: waveformContainer.value,
        waveColor: 'rgba(119, 92, 240, 0.4)', // Light purple
        progressColor: '#775CF0', // Purple
        barWidth: 4,
        barGap: 3,
        barRadius: 4,
        height: 70,
        cursorColor: '#333',
        cursorWidth: 2
      })
      
      wavesurfer.loadBlob(file)
      
      wavesurfer.on('ready', () => {
        waveReady.value = true
        isPlaying.value = false
        loadingKey.value = false
      })
      
      wavesurfer.on('finish', () => {
        isPlaying.value = false
      })
      
      wavesurfer.on('audioprocess', (time) => {
        const chord = chords.value.find(
          (c) => time >= c.start_time && time < c.end_time
        )
        currentChord.value = chord?.chord || ''
      })
    }
  }
}
const onDeleteAudio = () => {
  if (wavesurfer) {
    wavesurfer.destroy()
    wavesurfer = null
  }
  isPlaying.value = false
  waveReady.value = false
  detectedKey.value = null
  audioDuration.value = 0
}
const togglePlay = () => {
  if (wavesurfer) {
    wavesurfer.playPause()
    isPlaying.value = wavesurfer.isPlaying()
  }
}
</script>
  
<style scoped>
.music-app-card {
  overflow: hidden;
  border: none;
  /* background-color: #ffffff; */
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

.wave-container {
  background-color: #fafbff;
  border: 1px solid #e0e6f0;
  border-radius: 16px;
  padding: 24px;
  transition: box-shadow 0.3s;
}

.wave-container:hover {
  box-shadow: 0 10px 20px rgba(74, 58, 255, 0.1);
}

.wave-container span {
  font-size: 1.25rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 600;
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

.control-btn {
  transition: transform 0.2s;
}

.control-btn:hover {
  transform: scale(1.15);
}

@media (max-width: 768px) {
  .app-header {
    padding: 24px;
  }

  .gradient-text {
    font-size: 2.8rem;
  }

  .upload-btn {
    padding: 12px 20px;
    min-width: 160px;
  }
}

.upload-container span.font-weight-medium.text-h6.mt-4 {
  font-size: 1.4rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 700;
  padding: 8px 0;
}

.upload-container span.text-caption.text-grey-darken-1.mt-1 {
  font-size: 1.1rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 500;
  padding-bottom: 8px;
}
</style>

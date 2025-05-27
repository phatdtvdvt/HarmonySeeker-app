<template lang="pug">
  v-container.pa-4
    v-card.rounded-xl.elevation-5.music-app-card
      div.app-header.pa-6.rounded-t-xl.text-left
        h1.text-h3.font-weight-bold.text-grey-lighten-2 AI Voice Separator
        p.text-body-1.text-grey-lighten-2.mt-2.font-weight-bold
          | Separate vocals and instrumentals from your music using advanced AI technology.
          | Perfect for karaoke, remixing, or music production.
      div.app-content.pa-6
        // Original Audio Section
        div.wave-container.mt-6.rounded-lg.pa-4(v-if="originalWaveReady")
          div.d-flex.align-center.justify-space-between.mb-4
            h3.text-h6.font-weight-medium.comic-font Original Audio
            span.duration-text.comic-font Duration: {{ formatTime(originalDuration) }}
          div.d-flex.align-center.justify-space-between
            v-btn(icon size="large" color="primary" variant="tonal" class="control-btn mr-2" @click="toggleOriginalPlay")
              v-icon(size="32") {{ isOriginalPlaying ? 'mdi-pause' : 'mdi-play' }}
            div.flex-grow-1(ref="originalWaveformContainer")
            v-btn(icon size="large" color="error" variant="tonal" class="control-btn ml-2" @click="onDeleteAudio")
              v-icon(size="26") mdi-delete

        // Separated Audio Sections
        template(v-if="separationComplete")
          // Vocals Section
          div.wave-container.mt-6.rounded-lg.pa-4
            div.d-flex.align-center.justify-space-between.mb-4
              h3.text-h6.font-weight-medium.comic-font 
                v-icon(color="primary" class="mr-2") mdi-microphone
                | Vocals
              div.d-flex.align-center
                v-btn(icon size="small" color="primary" variant="text" class="mr-2" @click="downloadVocals")
                  v-icon(size="20") mdi-download
                span.duration-text.comic-font Duration: {{ formatTime(vocalsDuration) }}
            div.d-flex.align-center.justify-space-between
              v-btn(icon size="large" color="primary" variant="tonal" class="control-btn mr-2" @click="toggleVocalsPlay")
                v-icon(size="32") {{ isVocalsPlaying ? 'mdi-pause' : 'mdi-play' }}
              div.flex-grow-1(ref="vocalsWaveformContainer")

          // Instrumental Section
          div.wave-container.mt-6.rounded-lg.pa-4
            div.d-flex.align-center.justify-space-between.mb-4
              h3.text-h6.font-weight-medium.comic-font
                v-icon(color="primary" class="mr-2") mdi-piano
                | Instrumental
              div.d-flex.align-center
                v-btn(icon size="small" color="primary" variant="text" class="mr-2" @click="downloadInstrumental")
                  v-icon(size="20") mdi-download
                span.duration-text.comic-font Duration: {{ formatTime(instrumentalDuration) }}
            div.d-flex.align-center.justify-space-between
              v-btn(icon size="large" color="primary" variant="tonal" class="control-btn mr-2" @click="toggleInstrumentalPlay")
                v-icon(size="32") {{ isInstrumentalPlaying ? 'mdi-pause' : 'mdi-play' }}
              div.flex-grow-1(ref="instrumentalWaveformContainer")

        // Upload Container
        div.upload-container.mt-8.pa-6.rounded-lg(v-if="!originalWaveReady")
          input(type="file" accept="audio/*" @change="onFileChange" hidden ref="fileInput")
          div.d-flex.flex-column.align-center
            v-icon(size="64" color="primary") mdi-music-box-multiple
            span.font-weight-medium.text-h6.mt-4.comic-font Choose a song to separate
            span.text-caption.text-grey-darken-1.mt-1.comic-font Supported formats: .mp3, .wav, .flac
            v-btn.upload-btn.mt-6(
              size="large" 
              color="primary" 
              @click="selectFile" 
              prepend-icon="mdi-music-note"
              :loading="isUploading"
            )
              | Upload Audio

        // Processing Animation
        div.processing-container.mt-8(v-if="isProcessing")
          v-progress-circular(
            indeterminate
            color="primary"
            size="64"
          )
          h3.text-h6.mt-4.comic-font Separating audio...
          p.text-body-2.text-grey-darken-1.comic-font This may take a few moments
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import WaveSurfer from 'wavesurfer.js'
import api from '@/plugins/axios'

// State Management
const fileInput = ref<HTMLInputElement | null>(null)
const originalWaveformContainer = ref<HTMLDivElement | null>(null)
const vocalsWaveformContainer = ref<HTMLDivElement | null>(null)
const instrumentalWaveformContainer = ref<HTMLDivElement | null>(null)

const originalWaveReady = ref(false)
const separationComplete = ref(false)
const isUploading = ref(false)
const isProcessing = ref(false)

const isOriginalPlaying = ref(false)
const isVocalsPlaying = ref(false)
const isInstrumentalPlaying = ref(false)

const originalDuration = ref(0)
const vocalsDuration = ref(0)
const instrumentalDuration = ref(0)

// Wavesurfer instances
let originalWavesurfer: WaveSurfer | null = null
let vocalsWavesurfer: WaveSurfer | null = null
let instrumentalWavesurfer: WaveSurfer | null = null

// Helper Functions
const formatTime = (timeInSeconds: number): string => {
  const minutes = Math.floor(timeInSeconds / 60)
  const seconds = Math.floor(timeInSeconds % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

const createWaveSurfer = (container: HTMLElement) => {
  return WaveSurfer.create({
    container: container,
    waveColor: 'rgba(119, 92, 240, 0.4)',
    progressColor: '#775CF0',
    barWidth: 4,
    barGap: 3,
    barRadius: 4,
    height: 70,
    cursorColor: '#333',
    cursorWidth: 2
  })
}

// Event Handlers
const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = async (e: Event) => {
  if (fileInput.value) fileInput.value.value = ''
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    isUploading.value = true
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Load original audio waveform
      if (originalWaveformContainer.value) {
        if (originalWavesurfer) {
          originalWavesurfer.destroy()
        }
        originalWavesurfer = createWaveSurfer(originalWaveformContainer.value)
        originalWavesurfer.loadBlob(file)
        
        originalWavesurfer.on('ready', () => {
          originalWaveReady.value = true
          isOriginalPlaying.value = false
          originalDuration.value = originalWavesurfer?.getDuration() || 0
        })
        
        originalWavesurfer.on('finish', () => {
          isOriginalPlaying.value = false
        })
      }

      // Upload and process
      isProcessing.value = true
      const response = await api.post('api/separate-voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      // Load separated audio waveforms
      if (vocalsWaveformContainer.value && instrumentalWaveformContainer.value) {
        // Create vocals waveform
        if (vocalsWavesurfer) vocalsWavesurfer.destroy()
        vocalsWavesurfer = createWaveSurfer(vocalsWaveformContainer.value)
        
        // Create instrumental waveform
        if (instrumentalWavesurfer) instrumentalWavesurfer.destroy()
        instrumentalWavesurfer = createWaveSurfer(instrumentalWaveformContainer.value)

        // Load the separated audio files
        const vocalsBlob = new Blob([response.data.vocals], { type: 'audio/wav' })
        const instrumentalBlob = new Blob([response.data.instrumental], { type: 'audio/wav' })

        vocalsWavesurfer.loadBlob(vocalsBlob)
        instrumentalWavesurfer.loadBlob(instrumentalBlob)

        vocalsWavesurfer.on('ready', () => {
          vocalsDuration.value = vocalsWavesurfer?.getDuration() || 0
        })

        instrumentalWavesurfer.on('ready', () => {
          instrumentalDuration.value = instrumentalWavesurfer?.getDuration() || 0
          separationComplete.value = true
          isProcessing.value = false
        })
      }
    } catch (error) {
      console.error('Error processing audio:', error)
      isProcessing.value = false
    } finally {
      isUploading.value = false
    }
  }
}

const onDeleteAudio = () => {
  if (originalWavesurfer) {
    originalWavesurfer.destroy()
    originalWavesurfer = null
  }
  if (vocalsWavesurfer) {
    vocalsWavesurfer.destroy()
    vocalsWavesurfer = null
  }
  if (instrumentalWavesurfer) {
    instrumentalWavesurfer.destroy()
    instrumentalWavesurfer = null
  }
  
  originalWaveReady.value = false
  separationComplete.value = false
  isOriginalPlaying.value = false
  isVocalsPlaying.value = false
  isInstrumentalPlaying.value = false
  originalDuration.value = 0
  vocalsDuration.value = 0
  instrumentalDuration.value = 0
}

const toggleOriginalPlay = () => {
  if (originalWavesurfer) {
    originalWavesurfer.playPause()
    isOriginalPlaying.value = originalWavesurfer.isPlaying()
  }
}

const toggleVocalsPlay = () => {
  if (vocalsWavesurfer) {
    vocalsWavesurfer.playPause()
    isVocalsPlaying.value = vocalsWavesurfer.isPlaying()
  }
}

const toggleInstrumentalPlay = () => {
  if (instrumentalWavesurfer) {
    instrumentalWavesurfer.playPause()
    isInstrumentalPlaying.value = instrumentalWavesurfer.isPlaying()
  }
}

const downloadVocals = () => {
  // Implement download logic for vocals
}

const downloadInstrumental = () => {
  // Implement download logic for instrumental
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

.wave-container {
  background-color: #fafbff;
  border: 1px solid #e0e6f0;
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.wave-container:hover {
  box-shadow: 0 10px 20px rgba(74, 58, 255, 0.1);
  transform: translateY(-2px);
}

.duration-text {
  font-size: 1rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  font-weight: 600;
  color: #666;
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

.control-btn {
  transition: transform 0.2s;
}

.control-btn:hover {
  transform: scale(1.15);
}

.processing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
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

  .wave-container {
    padding: 16px;
  }

  .upload-btn {
    padding: 12px 20px;
    min-width: 160px;
  }
}

.comic-font {
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
}
</style> 
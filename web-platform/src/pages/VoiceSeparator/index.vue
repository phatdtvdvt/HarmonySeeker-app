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
        template(v-if="originalAudioFile")
          div.section-header.mb-4
            h3.text-h6.font-weight-medium.comic-font 
              v-icon(color="primary" class="mr-2") mdi-music-note
              | Original Audio
          
          WaveformPlayer(
            :audioFile="originalAudioFile"
            :isPlaying="isOriginalPlaying"
            :audioDuration="originalDuration"
            waveColor="rgba(25, 118, 210, 0.4)"
            progressColor="#1976D2"
            @play="isOriginalPlaying = true"
            @pause="isOriginalPlaying = false"
            @delete="handleDeleteOriginal"
            @ready="handleOriginalReady"
            @finish="isOriginalPlaying = false"
          )
          
          // Separate Button
          div.text-center.mt-6(v-if="!separationComplete && !isProcessing")
            v-btn.separate-btn(
              size="large"
              color="primary"
              @click="handleSeparateVoice"
              prepend-icon="mdi-music-box-multiple"
              :loading="isProcessing"
            )
              | Separate Voice
        
        // Processing Animation
        div.processing-container.mt-8(v-if="isProcessing")
          v-progress-circular(
            indeterminate
            color="primary"
            size="64"
          )
          h3.text-h6.mt-4.comic-font Separating audio...
          p.text-body-2.text-grey-darken-1.comic-font This may take a few moments

        // Separated Audio Sections
        template(v-if="separationComplete")
          // Vocals Section
          div.section-header.mb-4.mt-8
            h3.text-h6.font-weight-medium.comic-font 
              v-icon(color="success" class="mr-2") mdi-microphone
              | Vocals
            v-btn(
              icon 
              size="small" 
              color="success" 
              variant="text" 
              @click="downloadVocals"
              class="ml-auto"
            )
              v-icon(size="20") mdi-download
          
          WaveformPlayer(
            :audioFile="vocalsAudioFile"
            :isPlaying="isVocalsPlaying"
            :audioDuration="vocalsDuration"
            waveColor="rgba(76, 175, 80, 0.4)"
            progressColor="#4CAF50"
            @play="isVocalsPlaying = true"
            @pause="isVocalsPlaying = false"
            @ready="handleVocalsReady"
            @finish="isVocalsPlaying = false"
          )

          // Instrumental Section
          div.section-header.mb-4.mt-6
            h3.text-h6.font-weight-medium.comic-font
              v-icon(color="warning" class="mr-2") mdi-piano
              | Instrumental
            v-btn(
              icon 
              size="small" 
              color="warning" 
              variant="text" 
              @click="downloadInstrumental"
              class="ml-auto"
            )
              v-icon(size="20") mdi-download

          WaveformPlayer(
            :audioFile="instrumentalAudioFile"
            :isPlaying="isInstrumentalPlaying"
            :audioDuration="instrumentalDuration"
            waveColor="rgba(255, 152, 0, 0.4)"
            progressColor="#FF9800"
            @play="isInstrumentalPlaying = true"
            @pause="isInstrumentalPlaying = false"
            @ready="handleInstrumentalReady"
            @finish="isInstrumentalPlaying = false"
          )

          // New Separation Button
          div.text-center.mt-8
            v-btn.new-separation-btn(
              size="large"
              color="secondary"
              variant="outlined"
              @click="handleNewSeparation"
              prepend-icon="mdi-refresh"
            )
              | New Separation

        // Upload Container
        div.upload-container.mt-8.pa-6.rounded-lg(v-if="!originalAudioFile")
          input(
            type="file" 
            accept="audio/*" 
            @change="onFileChange" 
            hidden 
            ref="fileInput"
          )
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
</template>

<script setup lang="ts">
import { ref } from 'vue'
import WaveformPlayer from '@/components/WaveformPlayer/index.vue'
import api from '@/plugins/axios'
import JSZip from 'jszip'

// State Management
const fileInput = ref<HTMLInputElement | null>(null)

const originalAudioFile = ref<File | null>(null)
const vocalsAudioFile = ref<File | null>(null)
const instrumentalAudioFile = ref<File | null>(null)

const separationComplete = ref(false)
const isUploading = ref(false)
const isProcessing = ref(false)

const isOriginalPlaying = ref(false)
const isVocalsPlaying = ref(false)
const isInstrumentalPlaying = ref(false)

const originalDuration = ref(0)
const vocalsDuration = ref(0)
const instrumentalDuration = ref(0)

// Event Handlers
const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    isUploading.value = true
    originalAudioFile.value = file
    isUploading.value = false
  }
}

const handleOriginalReady = (duration: number) => {
  originalDuration.value = duration
}

const handleVocalsReady = (duration: number) => {
  vocalsDuration.value = duration
}

const handleInstrumentalReady = (duration: number) => {
  instrumentalDuration.value = duration
}

const handleDeleteOriginal = () => {
  originalAudioFile.value = null
  vocalsAudioFile.value = null
  instrumentalAudioFile.value = null
  separationComplete.value = false
  resetPlayingStates()
}

const handleSeparateVoice = async () => {
  if (!originalAudioFile.value) return
  
  isProcessing.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', originalAudioFile.value)

    const response = await api.post('api/separate-voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob'
    })
    const { vocalsBlob, instrumentalBlob } = await extractAudioFromZipWithJSZip(response.data)
    console.log(vocalsBlob, instrumentalBlob)
    vocalsAudioFile.value = new File([vocalsBlob], 'vocals.wav', { type: 'audio/wav' })
    instrumentalAudioFile.value = new File([instrumentalBlob], 'instrumental.wav', { type: 'audio/wav' })
    
    separationComplete.value = true
    
  } catch (error) {
    console.error('Error processing audio:', error)
    // Handle error appropriately
  } finally {
    isProcessing.value = false
  }
}

const extractAudioFromZipWithJSZip = async (zipBlob: Blob) => {
  const JSZip = (await import('jszip')).default
  const zip = await JSZip.loadAsync(zipBlob)
  
  const vocalsFile = zip.file('vocals.wav')
  const musicFile = zip.file('music.wav')
  
  if (!vocalsFile || !musicFile) {
    throw new Error('Could not find vocals.wav or music.wav in zip file')
  }
  
  const vocalsBlob = new Blob([await vocalsFile.async('uint8array')], { type: 'audio/wav' })
  const instrumentalBlob = new Blob([await musicFile.async('uint8array')], { type: 'audio/wav' })
  
  return { vocalsBlob, instrumentalBlob }
}

const handleNewSeparation = () => {
  // Reset everything to start fresh
  originalAudioFile.value = null
  vocalsAudioFile.value = null
  instrumentalAudioFile.value = null
  separationComplete.value = false
  resetPlayingStates()
  resetDurations()
  
  // Clear file input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const resetPlayingStates = () => {
  isOriginalPlaying.value = false
  isVocalsPlaying.value = false
  isInstrumentalPlaying.value = false
}

const resetDurations = () => {
  originalDuration.value = 0
  vocalsDuration.value = 0
  instrumentalDuration.value = 0
}

const downloadVocals = () => {
  if (vocalsAudioFile.value) {
    const url = URL.createObjectURL(vocalsAudioFile.value)
    const a = document.createElement('a')
    a.href = url
    a.download = 'vocals.wav'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
}

const downloadInstrumental = () => {
  if (instrumentalAudioFile.value) {
    const url = URL.createObjectURL(instrumentalAudioFile.value)
    const a = document.createElement('a')
    a.href = url
    a.download = 'instrumental.wav'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
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

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.separate-btn {
  min-width: 180px;
  border-radius: 12px;
  padding: 16px 32px;
  font-weight: 600;
  text-transform: none;
  box-shadow: 0 6px 16px rgba(74, 58, 255, 0.25);
  transition: 0.3s;
}

.separate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 58, 255, 0.35);
}

.new-separation-btn {
  min-width: 160px;
  border-radius: 12px;
  padding: 14px 28px;
  font-weight: 600;
  text-transform: none;
  transition: 0.3s;
}

.new-separation-btn:hover {
  transform: translateY(-2px);
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

  .upload-btn, .separate-btn {
    padding: 12px 20px;
    min-width: 160px;
  }
}

.comic-font {
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
}
</style>
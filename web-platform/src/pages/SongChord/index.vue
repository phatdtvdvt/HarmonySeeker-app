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
            
        div.wave-container.mt-6.rounded-lg.pa-4
          span Duration: {{ formatTime(audioDuration) }}

          div.d-flex.align-center.justify-space-between
            template(v-if="waveReady")
              v-btn(icon size="large" color="primary" variant="tonal" class="control-btn mr-2" @click="togglePlay")
                v-icon(size="32") {{ isPlaying ? 'mdi-pause' : 'mdi-play' }}
            div.flex-grow-1(ref="waveformContainer")
            template(v-if="waveReady")
              v-btn(icon size="large" color="error" variant="tonal" class="control-btn ml-2" @click="onDeleteAudio")
                v-icon(size="26") mdi-delete
                
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
        responsive: true,
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
}

.app-header {
  background: linear-gradient(135deg, #775CF0 0%, #4A3AFF 100%);
  position: relative;
}

.app-header::after {
  content: '';
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  z-index: 0;
}

.wave-container {
  background-color: #f9f9fc;
  border: 1px solid #eaeaea;
  border-radius: 16px;
}

.upload-container {
  border: 2px dashed #d0d0f0;
  background-color: #f9f9fc;
  transition: all 0.3s ease;
}

.upload-container:hover {
  border-color: #775CF0;
  background-color: #f0f0ff;
}

.chord-chip {
  font-weight: 600;
  background: linear-gradient(135deg, #775CF0 0%, #4A3AFF 100%);
  color: white;
  box-shadow: 0 4px 10px rgba(74, 58, 255, 0.2);
}

.control-btn {
  transition: all 0.2s ease;
}

.control-btn:hover {
  transform: scale(1.1);
}

.gradient-text {
  background: linear-gradient(135deg, #775CF0 0%, #4A3AFF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 3.5rem;
}

.key-display {
  padding: 20px;
  position: relative;
}

.upload-btn {
  min-width: 200px;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: none;
  box-shadow: 0 4px 12px rgba(74, 58, 255, 0.25);
  transition: all 0.3s ease;
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(74, 58, 255, 0.3);
}

/* For small screens */
@media (max-width: 600px) {
  .app-header {
    padding: 16px !important;
  }
  
  .app-header h1 {
    font-size: 1.8rem !important;
  }
  
  .gradient-text {
    font-size: 2.5rem;
  }
}
</style>
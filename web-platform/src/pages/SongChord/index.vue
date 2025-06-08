<template lang="pug">
  v-container.pa-4(style="max-width: 1200px; min-height: 100px")
    v-card.rounded-xl.elevation-5.music-app-card
      div.app-header.pa-6.rounded-t-xl.text-left
        h1.text-h3.font-weight-bold.text-grey-lighten-2.comic-font Free Online Key Chord Predictor
        p.text-body-1.text-grey-lighten-2.mt-2.font-weight-bold.comic-font
          | Instantly detect the key and chords of your song using AI.
          | Upload your audio to reveal its harmonic structure in seconds.
      div.app-content.pa-6
        div(v-if="waveReady").text-center.mb-2.key-display
          h2(v-if="!loadingKey").h3.text-h5.font-weight-bold.mb-4.comic-font.text-primary Song Key
          h2(v-if="loadingKey").text-subtitle-1.font-weight-bold.text-grey-darken-2.comic-font Wait to detect
          h1.text-h1.font-weight-bold.gradient-text.comic-font(v-if="!loadingKey") {{ detectedKey || '...' }}
          v-progress-circular(indeterminate color="primary" v-if="loadingKey")
        
        // Circle of Fifth and Chord Suggestions
        div.circle-of-fifth-container.mt-6.mb-6(v-if="waveReady && detectedKey")
          h3.text-h5.font-weight-bold.mb-4.comic-font.text-primary Circle of Fifth
          div.circle-wrapper
            div.circle-of-fifth
              // Outer circle (Major keys)
              div.circle-element.major(v-for="(majorKey, index) in circleOfFifthMajor" :key="'major-'+index" 
                  :class="{'active-chord': detectedKey === majorKey}"
                  :style="getCirclePosition(index, circleOfFifthMajor.length, 140)")
                span.comic-font {{ majorKey }}
              
              // Inner circle (Minor keys)
              div.circle-element.minor(v-for="(minorKey, index) in circleOfFifthMinor" :key="'minor-'+index" 
                  :class="{'active-chord': detectedKey === minorKey}"
                  :style="getCirclePosition(index, circleOfFifthMinor.length, 80)")
                span.comic-font {{ minorKey }}
            
            // Center chord
            div.center-chord
              span.comic-font {{ detectedKey }}
          
          // Chord Suggestions
          div.chord-suggestions.mt-8
            h3.text-h5.font-weight-bold.mb-4.comic-font.text-primary Suggested Chord Progressions

            v-card.suggestion-card.pa-5.rounded-xl.mb-5(elevation="4" shaped)
              template(v-if="chordSuggestions[detectedKey]")
                // Key Title
                div.d-flex.justify-space-between.align-center.mb-3
                  h4.text-h6.font-weight-bold.comic-font Key of {{ detectedKey }}
                  v-chip.color-deep-purple.text-white(label) Scale Mode

                // Scale Display
                p.mb-4.text-body-2.font-italic.text-secondary.comic-font 🎼 Scale: {{ chordSuggestions[detectedKey].scale }}

                // Popular Progression Block
                v-divider.my-3

                h5.text-subtitle-1.font-weight-bold.mb-2.comic-font.text-indigo Popular Progression:
                div.d-flex.flex-wrap
                  v-chip.ma-1(v-for="(chord, i) in chordSuggestions[detectedKey].popular.split(' – ')" :key="i"
                        color="deep-purple lighten-2" text-color="white" variant="elevated" label)
                    span.comic-font {{ chord }}

                // Formula Caption
                p.mt-3.text-caption.text-grey.comic-font Formula: {{ chordSuggestions[detectedKey].formula }}

              // No data fallback
              div(v-else).text-center.py-6
                v-icon.large.mb-2(color="grey lighten-1") mdi-emoticon-sad-outline
                p.text-body-2.comic-font.text-grey No suggestions available for this key

        
        div.mt-1.text-center(v-if="currentChord")
          v-chip(color="primary" variant="elevated" size="large" class="chord-chip px-6 py-2")
            v-icon(start class="mr-2") mdi-music-note
            span.text-subtitle-1.comic-font Current Chord: {{ currentChord }}
        
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
        
        v-btn.upload-btn.mt-5(size="large" color="primary" v-if="waveReady" @click="onDetectKey" :disabled="loadingKey")
          span.comic-font Detect KeyChord
        div.upload-container.mt-8.pa-6.rounded-lg(v-if="!waveReady")
          input(type="file" accept="audio/*" @change="onFileChange" hidden ref="fileInput")
          div.d-flex.flex-column.align-center
            v-icon(size="64" color="primary") mdi-cloud-upload
            span.font-weight-medium.text-h6.mt-4.comic-font Choose a file or drag it here
            span.text-caption.text-grey-darken-1.mt-1.comic-font Supported formats: .mp3, .wav, .flac
            v-btn.upload-btn.mt-6(size="large" color="primary" @click="selectFile" prepend-icon="mdi-music-note")
              span.comic-font Upload Audio
</template>
  
<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'
import WaveformPlayer from '@/components/WaveformPlayer/index.vue'
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

// Circle of Fifth data for major and minor keys
const circleOfFifthMajor = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
const circleOfFifthMinor = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'Bbm', 'Fm', 'Cm', 'Gm', 'Dm']

// Get position for circle of fifth elements
const getCirclePosition = (index: number, total: number, radius: number) => {
  const angle = (index * 2 * Math.PI / total) - Math.PI/2
  const x = radius * Math.cos(angle)
  const y = radius * Math.sin(angle)
  return {
    left: `calc(50% + ${x}px)`,
    top: `calc(50% + ${y}px)`,
    transform: 'translate(-50%, -50%)'
  }
}

// Chord suggestions for each key
const chordSuggestions = {
  // Major keys
  "C": {
    scale: "C – Dm – Em – F – G – Am – B°",
    popular: "C – G – Am – F",
    formula: "I–V–vi–IV"
  },
  "C:min": {
    scale: "Cm – D° – Eb – Fm – Gm – Ab – Bb",
    popular: "Cm – Ab – Bb – Gm",
    formula: "i–VI–VII–v"
  },
  "C#": {
    scale: "C# – D#m – E#m – F# – G# – A#m – B#°",
    popular: "C# – G# – A#m – F#",
    formula: "I–V–vi–IV"
  },
  "C#:min": {
    scale: "C#m – D#° – E – F#m – G#m – A – B",
    popular: "C#m – A – B – G#",
    formula: "i–VI–VII–v"
  },
  "D": {
    scale: "D – Em – F#m – G – A – Bm – C#°",
    popular: "D – A – Bm – G",
    formula: "I–V–vi–IV"
  },
  "D:min": {
    scale: "Dm – E° – F – Gm – Am – Bb – C",
    popular: "Dm – Bb – C – Am",
    formula: "i–VI–VII–v"
  },
  "D#": {
    scale: "Eb – Fm – Gm – Ab – Bb – Cm – D°",
    popular: "Eb – Bb – Cm – Ab",
    formula: "I–V–vi–IV"
  },
  "D#:min": {
    scale: "D#m – E#° – F# – G#m – A#m – B – C#",
    popular: "D#m – B – C# – A#",
    formula: "i–VI–VII–v"
  },
  "E": {
    scale: "E – F#m – G#m – A – B – C#m – D#°",
    popular: "E – B – C#m – A",
    formula: "I–V–vi–IV"
  },
  "E:min": {
    scale: "Em – F#° – G – Am – Bm – C – D",
    popular: "Em – C – D – B",
    formula: "i–VI–VII–v"
  },
  "F": {
    scale: "F – Gm – Am – Bb – C – Dm – E°",
    popular: "F – C – Dm – Bb",
    formula: "I–V–vi–IV"
  },
  "F:min": {
    scale: "Fm – G° – Ab – Bbm – Cm – Db – Eb",
    popular: "Fm – Db – Eb – Cm",
    formula: "i–VI–VII–v"
  },
  "F#": {
    scale: "F# – G#m – A#m – B – C# – D#m – E#°",
    popular: "F# – C# – D#m – B",
    formula: "I–V–vi–IV"
  },
  "F#:min": {
    scale: "F#m – G#° – A – Bm – C#m – D – E",
    popular: "F#m – D – E – C#",
    formula: "i–VI–VII–v"
  },
  "G": {
    scale: "G – Am – Bm – C – D – Em – F#°",
    popular: "G – D – Em – C",
    formula: "I–V–vi–IV"
  },
  "G:min": {
    scale: "Gm – A° – Bb – Cm – Dm – Eb – F",
    popular: "Gm – Eb – F – Dm",
    formula: "i–VI–VII–v"
  },
  "G#": {
    scale: "Ab – Bbm – Cm – Db – Eb – Fm – G°",
    popular: "Ab – Eb – Fm – Db",
    formula: "I–V–vi–IV"
  },
  "G#:min": {
    scale: "G#m – A#° – B – C#m – D#m – E – F#",
    popular: "G#m – E – F# – D#",
    formula: "i–VI–VII–v"
  },
  "A": {
    scale: "A – Bm – C#m – D – E – F#m – G#°",
    popular: "A – E – F#m – D",
    formula: "I–V–vi–IV"
  },
  "A:min": {
    scale: "Am – B° – C – Dm – Em – F – G",
    popular: "Am – F – G – Em",
    formula: "i–VI–VII–v"
  },
  "A#": {
    scale: "Bb – Cm – Dm – Eb – F – Gm – A°",
    popular: "Bb – F – Gm – Eb",
    formula: "I–V–vi–IV"
  },
  "A#:min": {
    scale: "A#m – B#° – C# – D#m – E#m – F# – G#",
    popular: "A#m – F# – G# – E#",
    formula: "i–VI–VII–v"
  },
  "B": {
    scale: "B – C#m – D#m – E – F# – G#m – A#°",
    popular: "B – F# – G#m – E",
    formula: "I–V–vi–IV"
  },
  "B:min": {
    scale: "Bm – C#° – D – Em – F#m – G – A",
    popular: "Bm – G – A – F#",
    formula: "i–VI–VII–v"
  }
}

const selectFile = () => {
  fileInput.value?.click()
}

const onDetectKey = async () => {
  loadingKey.value = true  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  try {
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
  } catch (error) {
    console.error('Error detecting key:', error)
    loadingKey.value = false
    detectedKey.value = 'Error'
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

/* Circle of Fifth Styles */
.circle-of-fifth-container {
  margin: 40px 0;
}

.circle-wrapper {
  position: relative;
  width: 320px;
  height: 320px;
  margin: 0 auto;
}

.circle-of-fifth {
  position: relative;
  width: 100%;
  height: 100%;
}

.circle-element {
  position: absolute;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.circle-element.major {
  background-color: #f0f4ff;
  color: #4A3AFF;
  z-index: 1;
}

.circle-element.minor {
  background-color: #f5f0ff;
  color: #775CF0;
  font-size: 0.9rem;
}

.circle-element.active-chord {
  background: linear-gradient(135deg, #775CF0, #4A3AFF);
  color: white !important;
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(74, 58, 255, 0.3);
  z-index: 10;
}

.center-chord {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #775CF0, #4A3AFF);
  color: white;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: bold;
  box-shadow: 0 4px 16px rgba(74, 58, 255, 0.3);
  z-index: 5;
}

/* Chord Suggestion Styles */
.chord-suggestions {
  max-width: 600px;
  margin: 0 auto;
}

.suggestion-card {
  background-color: #f9f9fc;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.suggestion-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
}

.chord-scale {
  background-color: #f5f5f5;
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.popular-progression {
  border-bottom: 1px dashed #e0e0e0;
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
  
  .circle-wrapper {
    width: 280px;
    height: 280px;
  }
  
  .circle-element {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }
  
  .circle-element.minor {
    font-size: 0.8rem;
  }
  
  .center-chord {
    width: 60px;
    height: 60px;
    font-size: 1.3rem;
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
  
  .circle-wrapper {
    width: 240px;
    height: 240px;
  }
  
  .circle-element {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }
  
  .circle-element.minor {
    font-size: 0.7rem;
  }
  
  .center-chord {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
}

.comic-font {
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
}
</style>
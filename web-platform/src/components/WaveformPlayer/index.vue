<template lang="pug">
    div.wave-container.mt-6.rounded-lg.pa-4
      span.d-flex.text-left.ml-2 {{ formatTime(audioDuration) }}
      div.d-flex.align-center.justify-space-between
        div
          v-btn(
            icon 
            size="large" 
            color="primary" 
            variant="tonal" 
            class="control-btn mr-2" 
            @click="handleTogglePlay"
          )
            v-icon(size="32") {{ isPlaying ? 'mdi-pause' : 'mdi-play' }}
        div.flex-grow-1(ref="waveformContainer")
        div
          v-btn(
            icon 
            size="large" 
            color="error" 
            variant="tonal" 
            class="control-btn ml-2" 
            @click="handleDelete"
          )
            v-icon(size="26") mdi-delete
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
  import WaveSurfer from 'wavesurfer.js'
  
  interface Props {
    audioFile?: File | null
    isPlaying?: boolean
    audioDuration?: number
    chords?: Array<{
      chord: string
      start_time: number
      end_time: number
    }>
    waveColor?: string
    progressColor?: string
  }
  
  interface Emits {
    (e: 'play'): void
    (e: 'pause'): void
    (e: 'delete'): void
    (e: 'ready', duration: number): void
    (e: 'finish'): void
    (e: 'chord-change', chord: string): void
    (e: 'time-update', time: number): void
  }
  
  const props = withDefaults(defineProps<Props>(), {
    audioFile: null,
    isPlaying: false,
    audioDuration: 0,
    chords: () => [],
    waveColor: 'rgba(119, 92, 240, 0.4)',
    progressColor: '#775CF0'
  })
  
  const emit = defineEmits<Emits>()
  
  const waveformContainer = ref<HTMLDivElement | null>(null)
  let wavesurfer: WaveSurfer | null = null
  
  const formatTime = (timeInSeconds: number): string => {
    const minutes = Math.floor(timeInSeconds / 60)
    const seconds = Math.floor(timeInSeconds % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }
  
  const handleTogglePlay = () => {
    if (wavesurfer) {
      wavesurfer.playPause()
      if (wavesurfer.isPlaying()) {
        emit('play')
      } else {
        emit('pause')
      }
    }
  }
  
  const handleDelete = () => {
    if (wavesurfer) {
      wavesurfer.destroy()
      wavesurfer = null
    }
    emit('delete')
  }
  
  const initWaveSurfer = async (file: File) => {
    await nextTick()
    if (!waveformContainer.value) return
  
    if (wavesurfer) {
      wavesurfer.destroy()
    }
    
    wavesurfer = WaveSurfer.create({
      container: waveformContainer.value,
      waveColor: props.waveColor,
      progressColor: props.progressColor,
      barWidth: 4,
      barGap: 3,
      barRadius: 4,
      height: 70,
      cursorColor: '#333',
      cursorWidth: 2
    })
  
    wavesurfer.loadBlob(file)
  
    wavesurfer.on('ready', () => {
      const duration = wavesurfer?.getDuration() || 0
      emit('ready', duration)
    })
  
    wavesurfer.on('finish', () => {
      emit('finish')
    })
  
    wavesurfer.on('audioprocess', (time) => {
      emit('time-update', time)
      
      const chord = props.chords.find(
        (c) => time >= c.start_time && time < c.end_time
      )
      if (chord) {
        emit('chord-change', chord.chord)
      }
    })
  }
  
  // Watch for audioFile changes
  watch(() => props.audioFile, (newFile) => {
    console.log('compo', newFile)
    if (newFile) {
      initWaveSurfer(newFile)
    }
  }, { immediate: true })
  
  // Expose methods for parent component
  defineExpose({
    play: () => wavesurfer?.play(),
    pause: () => wavesurfer?.pause(),
    stop: () => wavesurfer?.stop(),
    getCurrentTime: () => wavesurfer?.getCurrentTime() || 0,
    getDuration: () => wavesurfer?.getDuration() || 0,
    seekTo: (time: number) => wavesurfer?.seekTo(time),
    destroy: () => {
      if (wavesurfer) {
        wavesurfer.destroy()
        wavesurfer = null
      }
    }
  })
  
  onUnmounted(() => {
    if (wavesurfer) {
      wavesurfer.destroy()
    }
  })
  </script>
  
  <style scoped>
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
    font-size: 1.0rem;
    font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: 600;
  }
  
  .control-btn {
    transition: transform 0.2s;
  }
  
  .control-btn:hover {
    transform: scale(1.15);
  }
  </style>
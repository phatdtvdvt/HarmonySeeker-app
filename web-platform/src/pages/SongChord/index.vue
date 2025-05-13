<template lang="pug">
    .songchord-container
      // Header Section
      .header
        h1 Free Online Song Chord Finder
        p.description
          | Find chords from any song in a flash with AI-based technology. Upload your 
          | audio and get accurate chord progressions and lyrics synchronized in real-time
    
      // Upload Section
      .upload-section(v-if="!audioUploaded")
        .upload-box
          .upload-icon
            svg(xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round")
              path(d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4")
              polyline(points="17 8 12 3 7 8")
              line(x1="12" y1="3" x2="12" y2="15")
          p.upload-text Choose a file or drag it here
          p.supported-formats Supported formats: .mp3, .wav, .flac
          button.upload-button(@click="handleUpload") Upload Audio
          
      // Audio Player Section (appears after upload)
      .audio-player-section(v-if="audioUploaded")
        .audio-player
          .audio-info
            span.audio-filename {{ audioFile.name }}
            button.delete-button(@click="removeAudio")
              svg(xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round")
                path(d="M3 6h18")
                path(d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6")
                path(d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2")
          .audio-controls
            button.play-button(@click="togglePlay")
              span {{ isPlaying ? '⏸️' : '▶️' }}
            .progress-bar
              .progress-track
                .progress-fill(:style="{ width: progress + '%' }")
              input.progress-slider(type="range" min="0" max="100" v-model="progress" @input="seekAudio")
            span.time-duration {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
        
        // Key Detection Result Section
        .key-detection-result(v-if="keyDetected")
          h3 Detected Key
          .key-display
            h2.key-value {{ detectedKey }}
          .loading-spinner(v-if="isAnalyzing")
            span Analyzing audio...
    
      // Features Section
      .features-section
        .feature
          .feature-icon 🎸
          h3 Accurate Chord Detection
          p Our AI precisely identifies chords from any song
        .feature
          .feature-icon 🎵
          h3 Synchronized Lyrics
          p Get lyrics and chords perfectly timed together
        .feature
          .feature-icon ⏱️
          h3 Real-time Processing
          p Process your songs in seconds with our advanced AI
    </template>
    
    <script setup>
    import { ref, onMounted, onUnmounted } from 'vue'
    
    // Audio state
    const audioUploaded = ref(false)
    const audioFile = ref(null)
    const audioElement = ref(null)
    const isPlaying = ref(false)
    const progress = ref(0)
    const currentTime = ref(0)
    const duration = ref(0)
    
    // Key detection state
    const isAnalyzing = ref(false)
    const keyDetected = ref(false)
    const detectedKey = ref('')
    
    // API endpoint for chord detection
    const API_ENDPOINT = 'http://172.16.0.84:8000/predict-chord-crnn'
    
    // Handle file upload
    const handleUpload = async () => {
      // This would normally trigger a file input dialog
      const fileInput = document.createElement('input')
      fileInput.type = 'file'
      fileInput.accept = 'audio/*'
      fileInput.onchange = async (event) => {
        const file = event.target.files[0]
        if (file) {
          audioFile.value = file
          audioUploaded.value = true
          
          // Create audio element to play the file
          audioElement.value = new Audio(URL.createObjectURL(file))
          audioElement.value.addEventListener('loadedmetadata', () => {
            duration.value = audioElement.value.duration
          })
          audioElement.value.addEventListener('timeupdate', updateProgress)
          audioElement.value.addEventListener('ended', () => {
            isPlaying.value = false
          })
          
          // Send the audio file to the API for key detection
          await detectKey(file)
        }
      }
      fileInput.click()
    }
    
    // Detect key from audio file
    const detectKey = async (file) => {
      try {
        isAnalyzing.value = true
        keyDetected.value = false
        
        // Create form data for API request
        const formData = new FormData()
        formData.append('file', file)
        
        // Send request to API
        const response = await fetch(API_ENDPOINT, {
          method: 'POST',
          body: formData
        })
        console.log(response)
        if (!response.ok) {
          throw new Error('Failed to detect key')
        }
        
        // Parse API response
        const data = await response.json()
        
        // Display the detected key
        detectedKey.value = data.main_chord || 'Unknown'
        keyDetected.value = true
      } catch (error) {
        console.error('Error detecting key:', error)
        detectedKey.value = 'Detection failed'
        keyDetected.value = true
      } finally {
        isAnalyzing.value = false
      }
    }
    
    // Update progress bar
    const updateProgress = () => {
      if (audioElement.value) {
        currentTime.value = audioElement.value.currentTime
        progress.value = (audioElement.value.currentTime / audioElement.value.duration) * 100
      }
    }
    
    // Play/pause toggle
    const togglePlay = () => {
      if (!audioElement.value) return
      
      if (isPlaying.value) {
        audioElement.value.pause()
      } else {
        audioElement.value.play()
      }
      isPlaying.value = !isPlaying.value
    }
    
    // Seek audio to position
    const seekAudio = () => {
      if (audioElement.value) {
        const seekTime = (progress.value * audioElement.value.duration) / 100
        audioElement.value.currentTime = seekTime
        currentTime.value = seekTime
      }
    }
    
    // Remove audio
    const removeAudio = () => {
      if (audioElement.value) {
        audioElement.value.pause()
        audioElement.value = null
      }
      audioFile.value = null
      audioUploaded.value = false
      isPlaying.value = false
      progress.value = 0
      currentTime.value = 0
      duration.value = 0
      keyDetected.value = false
      detectedKey.value = ''
    }
    
    // Format time in MM:SS
    const formatTime = (seconds) => {
      if (!seconds) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    // Clean up audio element on component unmount
    onUnmounted(() => {
      if (audioElement.value) {
        audioElement.value.removeEventListener('timeupdate', updateProgress)
        audioElement.value = null
      }
    })
    </script>
    
    <style scoped>
    .songchord-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }
    
    .header {
      text-align: center;
      margin-bottom: 2rem;
    }
    
    .header h1 {
      font-size: 2rem;
      color: #2d3748;
      margin-bottom: 1rem;
    }
    
    .description {
      color: #4a5568;
      max-width: 600px;
      margin: 0 auto;
    }
    
    .upload-section {
      margin-bottom: 3rem;
    }
    
    .upload-box {
      border: 2px dashed #cbd5e0;
      border-radius: 0.5rem;
      padding: 3rem 2rem;
      text-align: center;
      background-color: #f7fafc;
      transition: border-color 0.3s ease;
      cursor: pointer;
    }
    
    .upload-box:hover {
      border-color: #3182ce;
    }
    
    .upload-icon {
      margin-bottom: 1rem;
      color: #3182ce;
    }
    
    .upload-text {
      font-size: 1.25rem;
      font-weight: 500;
      margin-bottom: 0.5rem;
      color: #2d3748;
    }
    
    .supported-formats {
      color: #718096;
      margin-bottom: 1.5rem;
      font-size: 0.875rem;
    }
    
    .upload-button {
      background-color: #3182ce;
      color: white;
      font-weight: 600;
      padding: 0.75rem 1.5rem;
      border-radius: 0.375rem;
      border: none;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    
    .upload-button:hover {
      background-color: #2c5282;
    }
    
    /* Audio Player Styles */
    .audio-player-section {
      margin-bottom: 3rem;
    }
    
    .audio-player {
      background-color: #f1f5f9;
      border-radius: 0.5rem;
      padding: 1rem;
    }
    
    .audio-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }
    
    .audio-filename {
      font-weight: 500;
      color: #2d3748;
    }
    
    .delete-button {
      background: none;
      border: none;
      color: #e53e3e;
      cursor: pointer;
      padding: 0.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .audio-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    
    .play-button {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
      width: 40px;
      height: 40px;
    }
    
    .progress-bar {
      flex: 1;
      position: relative;
    }
    
    .progress-track {
      height: 4px;
      background-color: #cbd5e0;
      border-radius: 2px;
      overflow: hidden;
      position: relative;
    }
    
    .progress-fill {
      height: 100%;
      background-color: #3182ce;
      position: absolute;
      top: 0;
      left: 0;
      transition: width 0.1s linear;
    }
    
    .progress-slider {
      position: absolute;
      top: -8px;
      left: 0;
      width: 100%;
      height: 20px;
      margin: 0;
      opacity: 0;
      cursor: pointer;
    }
    
    .time-duration {
      min-width: 80px;
      text-align: right;
      font-size: 0.875rem;
      color: #4a5568;
    }
    
    .features-section {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 2rem;
    }
    
    .feature {
      text-align: center;
      padding: 1.5rem;
      background-color: #f7fafc;
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    
    .feature h3 {
      margin-bottom: 0.75rem;
      color: #2d3748;
    }
    
    .feature p {
      color: #4a5568;
    }
    
    @media (max-width: 640px) {
      .features-section {
        grid-template-columns: 1fr;
      }
    }
    </style>
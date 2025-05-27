<template>
  <div class="introduction-page">
    <section class="intro-hero">
      <h1 class="intro-title" :class="{ 'fade-visible': showTitle }">HarmonySeeker <span class="gradient-text">Introduction</span></h1>
      <p class="intro-desc" :class="{ 'fade-visible': showDesc }">Discover the power of AI for music analysis. Instantly detect key, chords, and more from your audio files with a beautiful, user-friendly interface.</p>
      <div class="intro-button-container" :class="{ 'fade-visible': showButton }">
        <button class="start-detect-btn" @click="startDetect">
          🎵 Start Detect
        </button>
      </div>
    </section>

    <section class="intro-features">
      <h2 class="section-title">Features</h2>
      <div class="features-list">
        <div class="feature-card">
          <h3>🎵 Key & Chord Detection</h3>
          <p>Upload your song and get instant key and chord predictions using advanced AI models.</p>
        </div>
        <div class="feature-card">
          <h3>🎤 Voice Separator</h3>
          <p>Separate vocals and instrumentals for karaoke or remixing with a single click.</p>
        </div>
        <div class="feature-card">
          <h3>⚡ Fast & Beautiful UI</h3>
          <p>Enjoy a modern, responsive, and friendly interface designed for musicians and music lovers.</p>
        </div>
      </div>
    </section>

    <section class="intro-faq">
      <h2 class="section-title">Frequently asked questions</h2>
      <div class="faq-list">
        <div v-for="(item, idx) in faqs" :key="idx" class="faq-item" :class="{ active: openFaq === idx }">
          <div class="faq-question" @click="toggleFaq(idx)">
            {{ item.q }}
            <span class="arrow" :class="{ open: openFaq === idx }">&#9660;</span>
          </div>
          <div class="faq-answer-wrapper" :class="{ open: openFaq === idx }">
            <div class="faq-answer" v-html="item.a"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const showTitle = ref(false)
const showDesc = ref(false)
const showButton = ref(false)
const openFaq = ref(-1)
const router = useRouter()

const faqs = [
  {
    q: 'How do I use HarmonySeeker?',
    a: 'Simply upload your audio file on the Song Chord page and let the AI analyze it for you. For voice removal, go to the Voice Removal page.'
  },
  {
    q: 'Which audio formats are supported?',
    a: 'We support .mp3, .wav, and .flac files for both chord/key detection and voice removal.'
  },
  {
    q: 'Who created this project?',
    a: `This project was created by Trần Đức Trí and Phạm Nguyễn Anh Phát as part of our graduation thesis at the University of Science and Technology - The University of Danang (Đại học Bách Khoa Đà Nẵng).<br>
      Facebook: 
      <a href="https://www.facebook.com/tranductri2003/" target="_blank">Trần Đức Trí</a> | 
      <a href="https://www.facebook.com/phamnguyenanhphat" target="_blank">Phạm Nguyễn Anh Phát</a><br>
      LinkedIn: 
      <a href="https://www.linkedin.com/in/duc-tri-tran-464343218/" target="_blank">Trần Đức Trí</a> | 
      <a href="https://www.linkedin.com/in/phat-pham-327aa1220/" target="_blank">Phạm Nguyễn Anh Phát</a>`
  },
  {
    q: 'Is this project open source?',
    a: `Absolutely! We're happy to share our work with the community.<br>
      Feel free to explore or contribute:<br>
      GitHub: 
      <a href="https://github.com/tranductri2003/HarmonySeeker-app" target="_blank">HarmonySeeker-app</a> | 
      <a href="https://github.com/tranductri2003/HarmonySeeker-ai" target="_blank">HarmonySeeker-ai</a>`
  }
];

onMounted(() => {
  setTimeout(() => { showTitle.value = true }, 300)
  setTimeout(() => { showDesc.value = true }, 1200)
  setTimeout(() => { showButton.value = true }, 2000)
})

function toggleFaq(idx) {
  openFaq.value = openFaq.value === idx ? -1 : idx
}

function startDetect() {
  router.push('/songchord')
}
</script>

<style scoped>
.introduction-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px 64px 16px;
}
.intro-hero {
  padding: 72px 0 48px 0;
  text-align: center;
}
.intro-title,
.intro-desc,
.intro-button-container {
  opacity: 0;
  transition: opacity 0.8s;
  pointer-events: none;
  min-height: 48px;
}
.intro-title {
  font-size: 2.8rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  font-weight: 700;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
.gradient-text {
  background: linear-gradient(90deg, #9c27b0 0%, #673ab7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.intro-desc {
  font-size: 1.25rem;
  color: #444;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  margin-bottom: 0;
  margin-top: 0;
}
.intro-button-container {
  margin-top: 32px;
}
.start-detect-btn {
  background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 16px 32px;
  font-size: 1.1rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
  transition: all 0.3s ease;
  transform: translateY(0);
}
.start-detect-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4);
  background: linear-gradient(135deg, #ad29c4 0%, #7c4dff 100%);
}
.start-detect-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
}
.section-title {
  font-size: 2rem;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  font-weight: 700;
  margin: 56px 0 32px 0;
  text-align: center;
}
.features-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 40px;
  margin-bottom: 32px;
}
.feature-card {
  background: #fafbff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(124, 58, 237, 0.07);
  padding: 40px 32px;
  max-width: 320px;
  min-width: 220px;
  text-align: left;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  transition: box-shadow 0.2s;
}
.feature-card:hover {
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.13);
}
.feature-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 10px;
}
.feature-card p {
  font-size: 1rem;
  color: #555;
}
.intro-faq {
  max-width: 800px;
  margin: 0 auto 48px auto;
}
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 22px;
}
.faq-item {
  background: #f8f8fc;
  border-radius: 14px;
  padding: 0;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.10);
  overflow: hidden;
  border: 1.5px solid #e0d7fa;
  margin-bottom: 2px;
  transition: box-shadow 0.25s, border 0.25s;
}
.faq-item.active {
  box-shadow: 0 6px 24px rgba(124, 58, 237, 0.13);
  border: 2px solid #9c27b0;
}
.faq-question {
  font-weight: 700;
  font-size: 1.1rem;
  padding: 20px 28px;
  cursor: pointer;
  background: #f5f5fa;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
}
.faq-question:hover {
  background: #edeafd;
}
.arrow {
  margin-left: 12px;
  font-size: 1.3em;
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
  display: inline-block;
}
.arrow.open {
  transform: rotate(180deg) scale(1.2);
  color: #9c27b0;
}

.faq-answer-wrapper {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.faq-answer-wrapper.open {
  max-height: 500px;
}
.faq-answer {
  color: #555;
  font-size: 1rem;
  padding: 18px 28px 22px 28px;
  background: #f8f8fc;
  border-top: 1px solid #ece8fa;
  text-align: left;
}
.faq-answer a {
  color: #7c3aed;
  text-decoration: underline;
  font-weight: 600;
  margin: 0 4px;
}

.fade-visible {
  opacity: 1;
  pointer-events: auto;
}
@media (max-width: 900px) {
  .features-list {
    flex-direction: column;
    align-items: center;
    gap: 18px;
  }
  .feature-card {
    max-width: 100%;
    min-width: 0;
    width: 100%;
  }
}
</style>
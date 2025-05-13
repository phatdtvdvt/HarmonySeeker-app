<template lang="pug">
.app-layout
  // Sidebar
  .sidebar
    .logo
      RouterLink(to="/") HarmonySeeker
    
    nav.nav-menu
      RouterLink.nav-item.active(to="/songchord")
        span.nav-icon 🎵
        span.nav-text Song Chord
      RouterLink.nav-item(to="/stem-splitter")
        span.nav-icon ✂️
        span.nav-text Stem Splitter
    
  // Main Content
  .main-content
    main.page-content
      RouterView
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.sidebar {
  width: 260px;
  background-color: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 0;
}

.logo {
  margin-bottom: 2rem;
  padding-left: 0.25rem;
}

.logo-img {
  height: 30px;
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-left: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0.5rem;
  border-radius: 0.375rem;
  color: #4a5568;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.nav-item:hover {
  background-color: #f7fafc;
  color: #2d3748;
}

.nav-item.active, .nav-item.router-link-active {
  background-color: #ebf8ff;
  color: #3182ce;
}

.nav-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.nav-text {
  font-weight: 500;
}

.sidebar-footer {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 0.5rem;
}

.download-button {
  background-color: #00e676;
  color: black;
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.download-button:hover {
  background-color: #00c853;
}

.login-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  border-radius: 0.375rem;
  border: 1px solid #e2e8f0;
  background-color: white;
  color: #4a5568;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: #f7fafc;
}

.login-icon {
  margin-right: 0.5rem;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
  border-bottom: 1px solid #e2e8f0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.access-button {
  background-color: #3182ce;
  color: white;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
}

.tools-button {
  background-color: white;
  color: #4a5568;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: 1px solid #e2e8f0;
  cursor: pointer;
}

.install-button {
  background-color: #f7fafc;
  color: #4a5568;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: 1px solid #e2e8f0;
  cursor: pointer;
}

.app-download-button {
  background-color: #00e676;
  color: black;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
}

.page-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 1024px) {
  .header-right {
    gap: 0.5rem;
  }
  
  .install-button {
    display: none;
  }
}

@media (max-width: 768px) {
  .app-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
    padding: 1rem;
  }
  
  .nav-menu {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .nav-item {
    width: calc(50% - 0.5rem);
  }
  
  .header-right {
    display: none;
  }
}
</style>
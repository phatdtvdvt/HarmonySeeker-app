<template lang="pug">
  .header-navigation
    .nav-container
      // Logo and brand name (left side)
      .brand-section
        .logo
          v-icon(color="primary" size="32") mdi-music-note-outline
        .brand-name HarmonySeeker
          
      // Navigation items (right side)
      .nav-items
        .nav-item(
          v-for="(item, index) in navItems"
          :key="index"
          :class="{ active: route.path === item.to, disabled: item.disabled }"
          @click="selectItem(index)"
        )
          .item-text {{ item.text }}
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const navItems = ref([
  { 
    text: 'Introduction',
    to: '/',
    disabled: false
  },
  { 
    text: 'Song Chord',
    to: '/songchord',
    disabled: false
  },
  { 
    text: 'Voice Separator',
    to: '/voiceseparator',
    disabled: false
  }
])

const selectItem = (index) => {
  const to = navItems.value[index].to
  if (to && !navItems.value[index].disabled) {
    router.push(to)
  }
}

const handleLogin = () => {
  // Handle login logic here
  console.log('Login clicked')
  // router.push('/login')
}
</script>

<style lang="scss" scoped>
.header-navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
  
  .nav-container {
    max-width: 1400px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
  }
  
  // Brand section (left side)
  .brand-section {
    display: flex;
    align-items: center;
    
    .logo {
      margin-right: 12px;
    }
    
    .brand-name {
      font-size: 22px;
      font-weight: 700;
      color: #333;
      background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: 0.5px;
      font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
    }
  }
  
  // Navigation items (right side)
  .nav-items {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .nav-item {
      position: relative;
      padding: 8px 16px;
      cursor: pointer;
      border-radius: 6px;
      transition: color 0.25s cubic-bezier(0.4, 0, 0.2, 1), background 0.2s;
      font-weight: 500;
      font-family: 'Comic Neue', 'Comic Sans MS', cursive, sans-serif !important;
      background: transparent;
      box-shadow: none;
      
      &:hover:not(.active):not(.login-button) {
        background-color: #f5f5f5;
      }
      
      &:hover:not(.active):not(.login-button) .item-text {
        position: static;
      }
      
      &:hover:not(.active):not(.login-button) .item-text::after {
        content: none;
        display: none;
      }
      
      &.active {
        position: relative;
        color: #9c27b0;
        font-weight: 600;
        transition: color 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        
        &::after {
          content: '';
          position: absolute;
          bottom: -4px;
          left: 0;
          width: 100%;
          height: 3px;
          background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
          border-radius: 8px;
          transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s, opacity 0.3s;
          opacity: 1;
        }
      }
      
      &:not(.active)::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%);
        border-radius: 8px;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s, opacity 0.3s;
        opacity: 0;
      }
      
      &.disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      
      .item-text {
        font-size: 16px;
        color: inherit;
        transition: color 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      }
      
      &.login-button {
        background-color: #9c27b0;
        color: white;
        border-radius: 8px;
        padding: 8px 18px;
        display: flex;
        align-items: center;
        margin-left: 16px;
        
        &:hover {
          background-color: #7b1fa2;
          transform: translateY(-1px);
          box-shadow: 0 4px 8px rgba(156, 39, 176, 0.3);
        }
        
        .item-text {
          color: white;
        }
      }
    }
  }
}

// Responsive design
@media (max-width: 768px) {
  .header-navigation {
    height: auto;
    padding: 12px 0;
    
    .nav-container {
      flex-direction: column;
      gap: 12px;
      padding: 0 16px;
    }
    
    .nav-items {
      width: 100%;
      justify-content: space-between;
      
      .nav-item {
        padding: 6px 10px;
        font-size: 14px;
        
        &.login-button {
          margin-left: 0;
        }
      }
    }
  }
}

// For extra small screens
@media (max-width: 480px) {
  .header-navigation .nav-items {
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    
    .nav-item {
      .item-text {
        font-size: 14px;
      }
    }
  }
  
  .brand-section .brand-name {
    font-size: 18px;
  }
}
</style>
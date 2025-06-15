// composables/useToast.js
import { ref } from 'vue'

const toasts = ref([])

const toastConfigs = {
  success: { color: 'success', icon: 'mdi-check-circle' },
  error: { color: 'error', icon: 'mdi-alert-circle' },
  warning: { color: 'warning', icon: 'mdi-alert' },
  info: { color: 'info', icon: 'mdi-information' }
}

export const useToast = () => {
  const Toast = (state, title = '', message) => {
    const config = toastConfigs[state] || toastConfigs.info
    const toastHeight = 70
    const topOffset = 20 + (toasts.value.length * (toastHeight + 10))
    
    const newToast = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      type: state,
      title: title || undefined,
      message,
      show: true,
      color: config.color,
      icon: config.icon,
      topOffset
    }
    
    toasts.value.push(newToast)
    
    setTimeout(() => {
      removeToast(newToast.id)
    }, 4000)
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value[index].show = false
      setTimeout(() => {
        toasts.value.splice(index, 1)
        toasts.value.forEach((toast, i) => {
          const toastHeight = 70
          toast.topOffset = 20 + (i * (toastHeight + 10))
        })
      }, 300)
    }
  }

  const handleSnackbarUpdate = (id, show) => {
    if (!show) {
      removeToast(id)
    }
  }

  return {
    toasts,
    Toast,
    removeToast,
    handleSnackbarUpdate
  }
}
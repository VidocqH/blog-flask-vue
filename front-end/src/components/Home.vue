<template>
  <div class="container" v-if="alert.showAlert">
    <alert
      v-for="(alert, index) in alerts" :key="index"
      v-bind:variant="alert.alertVariant"
      v-bind:message="alert.alertMessage">
    </alert>
  </div>
</template>

<script>
import Alert from './Alert'
export default {
  name: 'Home',
  components: {
    alert: Alert
  },
  data() {
    return {
      alert: [
        {
          showAlert: true,
          alertVariant: 'danger',
          alertMessage: 0
        },
        {
          showAlert: true,
          alertVariant: 'info',
          alertMessage: 1
        },
        {
          showAlert: true,
          alertVariant: 'dark',
          alertMessage: 2
        }
      ]
    }
  }
}
</script>

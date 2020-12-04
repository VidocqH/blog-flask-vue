<template>
  <div class="container">
    <alert
      v-for="(alert, index) in alerts" :key="index"
      v-bind:variant="alert.variant"
      v-bind:message="alert.message">
    </alert>
    <button type="button" class="btn btn-primary">HomePage</button>
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
      alerts: [
        {
          variant: 'info',
          message: '1'
        },
        {
          variant: 'danger',
          message: '2'
        },
        {
          variant: 'success',
          message: '3'
        }
      ]
    }
  }
}
</script>

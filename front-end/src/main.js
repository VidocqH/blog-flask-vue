// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// Import Bootstrap css files
import 'bootstrap/dist/css/bootstrap.css'
import VueToasted from 'vue-toasted'
import axios from './http'
import moment from 'moment'
// Import Bootstrap css and js files
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

Vue.config.productionTip = false

Vue.prototype.$moment = moment
Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

Vue.use(VueToasted, {
  // Theme: primary/outline/bubble
  theme: 'bubble',
  // Display position
  position: 'top-center',
  // Display duration
  duration: 3000,
  // Icon Pack
  iconPack: 'material',
  // Actions that support
  action: {
    text: 'Cancel',
    onClick: (e, toastObject) => {
      toastObject.goAway(0)
    }
  }
})

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
// Fonts and Icons
import './assets/icon-line/css/simple-line-icons.css'
import './assets/icon-material/material-icons.css'
// styles of bootstrap-markdown
import './assets/bootstrap-markdown/css/bootstrap-markdown.min.css'
import './assets/bootstrap-markdown/css/custom.css'
import './assets/icon-awesome/css/font-awesome.min.css'  // 编辑器上的按钮图标是使用 font-awesome 字体图标
// styles of markdown
import './assets/markdown-styles/github-markdown.css'
// custom css
import './assets/core.css'
import './assets/custom.css'
// Import Bootstrap css and js files
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
// highlight css
import 'highlight.js/styles/atom-one-dark-reasonable.css'
import './assets/markdown-styles/github-markdown.css'

import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark-reasonable.css'
Vue.directive('highlight', function(el) {
  let blocks = el.querySelectorAll('pre code')
  blocks.forEach((block) => {
    hljs.highlightBlock(block)
  })
})

import VueSweetAlert2 from 'vue-sweetalert2'
Vue.use(VueSweetAlert2)

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

import Vue from 'vue'
import App from './App.vue'
import VueMaterial from "vue-material";
import VueRouter from "vue-router";

import router from "./router";
import VueYouTubeEmbed from 'vue-youtube-embed'


import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

Vue.config.productionTip = false

Vue.use(VueYouTubeEmbed, { global: true, componentId: "youtube-media" })
Vue.use(VueRouter);
Vue.use(VueMaterial);


new Vue({
  render: h => h(App),
  router,
  components: {App},
}).$mount('#app')

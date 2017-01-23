<template>
  <div id="app">
    <img src="/api/captcha">
    <input type="text" placeholder="輸入Captcha" v-model="captcha"/>
    <button @click="start">Captcha</button>
    <button @click="cancelOrder">Cancel</button>
  </div>
</template>

<script>
import * as cookie from 'cookie'

export default {
  name: 'app',
  data () {
    return {
      captcha: ''
    }
  },
  computed: {
    csrfHeader () {
      return {
        headers: {
          'X-CSRFToken': cookie.parse(document.cookie).csrftoken
        }
      }
    }
  },
  methods: {
    orderID () {
      return {
        id: 'abcdef',
        resNo: 'kerker'
      }
    },
    order () {
      return {
        ...this.orderID(),
        vegetarianBox: 1,
        ribsBox: 3,
        vat: 'nop',
        captcha: this.captcha
      }
    },
    cancelOrder () {
      this.$http.post('/api/cancel', this.orderID(), this.csrfHeader)
    },
    updateOrder () {
      let order = this.order()
      order.ribsBox = 5
      this.$http.post('/api/update', order, this.csrfHeader)
    },
    lookupOrder () {
      this.$http.post('/api/query', this.orderID(), this.csrfHeader).then(this.updateOrder)
    },
    createOrder () {
      this.$http.post('/api/order', this.order(), this.csrfHeader).then(this.lookupOrder)
    },
    login () {
      this.$http.get('/api/force_login').then(this.createOrder)
    },
    start () {
      this.login()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

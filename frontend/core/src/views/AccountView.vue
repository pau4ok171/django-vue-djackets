<template>
  <div class="page-account">
    <div class="columns-is-miltiple">
      <div class="column is-12">
        <h1 class="title">My account</h1>
      </div>

      <div class="column is-12">
        <button @click="logout" class="button is-danger">Log out</button>
      </div>

      <hr>

      <div class="column is-12">
        <h2 class="subtitle">My orders</h2>
        <OrderSummary
          v-for="order in orders"
          v-bind:key="order.id"
          v-bind:order="order"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import axios from "axios";
  import store from "@/store";
  import OrderSummary from "@/components/OrderSummary.vue";

  export default {
    name: 'Account',
    components: {
      OrderSummary
    },
    data() {
      return {
        orders: []
      }
    },
    mounted() {
      document.title = 'My account | Djackets'

      this.getCustomerOrders()
    },
    methods: {
      logout() {
        axios.defaults.headers.common['Authorization'] = ""

        localStorage.removeItem("token")
        localStorage.removeItem("username")
        localStorage.removeItem("userid")

        store.commit('removeToken')

        this.$router.push('/')

      },
      async getCustomerOrders() {
        store.commit('setIsLoading', true)

        await axios
            .get('/api/v1/orders/')
            .then(response => this.orders = response.data)
            .catch(error => console.log(error))

        store.commit('setIsLoading', false)
      }
    }
  }
</script>

<style scoped>

</style>
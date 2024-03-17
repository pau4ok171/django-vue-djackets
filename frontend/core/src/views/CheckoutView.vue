<template>
  <div class="page-checkout">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Checkout</h1>
      </div>

      <div class="column is-12">
        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
            </tr>
          </thead>

          <tbody>
          <tr
            v-for="item in cart.items"
            v-bind:key="item.product.id"
          >
            <td>{{ item.product.name }}</td>
            <td>${{ item.product.price }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ getItemTotal(item).toFixed(2) }}</td>
          </tr>
          </tbody>
        </table>
      </div>

      <div class="column is-12 box">
        <h2 class="subtitle">Shipping details</h2>

        <p class="has-text-grey mb-4">* All fields are required</p>

        <div class="columns is-multiline">

          <div class="column is-6">
            <div class="field">
              <label>First name*</label>
              <div class="control">
                <input type="text" class="input" v-model="first_name">
              </div>
            </div>

            <div class="field">
              <label>Last name*</label>
              <div class="control">
                <input type="text" class="input" v-model="last_name">
              </div>
            </div>

            <div class="field">
              <label>E-mail*</label>
              <div class="control">
                <input type="email" class="input" v-model="email">
              </div>
            </div>

            <div class="field">
              <label>Phone*</label>
              <div class="control">
                <input type="text" class="input" v-model="phone">
              </div>
            </div>
          </div>

          <div class="column is-6">

            <div class="field">
              <label>Address*</label>
              <div class="control">
                <input type="text" class="input" v-model="address">
              </div>
            </div>

            <div class="field">
              <label>Zip code*</label>
              <div class="control">
                <input type="email" class="input" v-model="zipcode">
              </div>
            </div>

            <div class="field">
              <label>Place*</label>
              <div class="control">
                <input type="text" class="input" v-model="place">
              </div>
            </div>
          </div>
        </div>

        <div class="notification is-danger mt-4" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <hr>

          <div id="card-element" class="mb-5"></div>

          <template v-if="cartTotalLength">
            <hr>

            <button class="button is-dark" @click="submitForm">Pay with Stripe</button>
          </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import axios from "axios";
  import store from "@/store";

  export default {
    name: 'Checkout',
    data() {
      return {
        cart: {
          items: []
        },
        stripe: {},
        card: {},
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
        zipcode: '',
        place: '',
        errors: [],
      }
    },
    mounted() {
      document.title = 'Checkout | Djackets'

      this.cart = store.state.cart

      if (this.cartTotalLength > 0) {
        this.stripe = Stripe('pk_test_51Ov2e402tO0i7CJA76ZiamulHqcmlRL1mosjDFIQSzBWykQnHTjiQjdy6LATJMWwlR7380xc8R7XpFuBi7XH3ra900bRwyrbON')
        const elements = this.stripe.elements();
        this.card = elements.create('card', { hidePostalCode: true })

        this.card.mount('#card-element')
      }
    },
    methods: {
      getItemTotal(item) {
        return item.quantity * item.product.price
      },
      submitForm() {
        this.errors = []

        const fields = {
          first_name: {name: 'first name', field_value: this.first_name},
          last_name: {name: 'last name', field_value: this.last_name},
          email: {name: 'email', field_value: this.email},
          phone: {name: 'phone', field_value: this.phone},
          address: {name: 'address', field_value: this.address},
          zipcode: {name: 'zip code', field_value: this.zipcode},
          place: {name: 'place', field_value: this.place},
        }

        for (const [key, value] of Object.entries(fields)) {
          if (value.field_value === '') {
            this.errors.push(`The ${value.name} field is missing!`)
          }
        }

        if (!this.errors.length) {
          store.commit('setIsLoading', true)

          this.stripe.createToken(this.card).then(result => {
            if (result.error) {
              store.commit('setIsLoading', false)
              this.errors.push('Something went wrong with Stripe. Please try again')
              console.log(result.error.message)
            } else {
              this.stripeTokenHandler(result.token)
              store.commit('setIsLoading', false)
            }
          })
        }
      },
      async stripeTokenHandler(token) {
        const items = []

        for (let i = 0; i < this.cart.items.length; i++) {
          const item = this.cart.items[i]
          const obj = {
            product: item.product.id,
            quantity: item.quantity,
            price: item.product.price * item.quantity
          }

          items.push(obj)
        }

        const data = {
          'first_name': this.first_name,
          'last_name': this.last_name,
          'email': this.email,
          'phone': this.phone,
          'address': this.address,
          'zipcode': this.zipcode,
          'place': this.place,
          'items': items,
          'stripe_token': token.id,
        }

        await axios
            .post('api/v1/checkout/', data)
            .then(response => {
              store.commit('clearCart')
              this.$router.push('/cart/success')
            })
            .catch(error => {
              this.errors.push('Something went wrong. Please try again')

              console.log(error)
            })

      },
    },
    computed: {
      cartTotalPrice() {
        return this.cart.items.reduce((acc, curVal) => {
          return acc += curVal.product.price * curVal.quantity
        }, 0)
      },
      cartTotalLength() {
        return this.cart.items.reduce((acc, curVal) => {
          return acc += curVal.quantity
        }, 0)
      }
    }
  }
</script>

<style scoped>

</style>
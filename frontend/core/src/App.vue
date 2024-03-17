<script lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import store from "@/store";
import CartIcon from "@/components/icons/CartIcon.vue";
import SearchIcon from "@/components/icons/SearchIcon.vue";
import axios from "axios";
export default {
  components: {SearchIcon, CartIcon, RouterLink, RouterView},
  data() {
    return {
      showMobileMenu: false,
      cart: {
        items: []
      },
    }
  },
  beforeCreate() {
    store.commit('initializeStore')

    const token = store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = store.state.cart
  },
  computed: {
    store() {
      return store
    },
    cartTotalLength() {
      let totalLength = 0
      for (let i = 0; i < this.cart.items.length; i++) {
        totalLength += this.cart.items[i].quantity
      }
      return totalLength
    }
  }
}
</script>

<template>
  <div id="wrapper">
   <nav class="navbar is-dark">
     <div class="navbar-brand">
       <RouterLink to="/" class="navbar-item"><strong>Djackets</strong></RouterLink>
       <a
         class="navbar-burger"
         aria-label="menu"
         aria-expanded="false"
         data-target="navbar-menu"
         @click="showMobileMenu = !showMobileMenu"
       >
         <span aria-hidden="true"></span>
         <span aria-hidden="true"></span>
         <span aria-hidden="true"></span>
       </a>
     </div>

     <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu}">
       <div class="navbar-start">
         <div class="navbar-item">
           <form method="get" action="/search">
             <div class="field has-addons">
               <div class="control">
                 <input type="text" class="input" placeholder="What are you looking for?" name="query">
               </div>
               <div class="control">
                 <button class="button is-success">
                   <span class="icon">
                     <SearchIcon/>
                   </span>
                 </button>
               </div>
             </div>
           </form>
         </div>
       </div>
       <div class="navbar-end">
         <RouterLink to="/summer" class="navbar-item">Summer</RouterLink>
         <RouterLink to="/winter" class="navbar-item">Winter</RouterLink>

         <div class="navbar-item">
           <div class="buttons">
             <template v-if="store.state.isAuthenticated">
               <RouterLink to="/account" class="button is-light">Account</RouterLink>
             </template>

             <template v-else>
               <RouterLink to="/log-in" class="button is-light">Log in</RouterLink>
             </template>

             <RouterLink to="/cart" class="button is-success">
               <span class="icon"><CartIcon/></span>
               <span>Cart ({{ cartTotalLength }})</span>
             </RouterLink>
           </div>
         </div>
       </div>
     </div>
    </nav>

    <div
      class="is-loading-bar has-text-centered"
      v-bind:class="{ 'is-loading': store.state.isLoading }"
    >
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <RouterView />
    </section>

    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2024</p>
    </footer>
  </div>
</template>

<style lang="css">
  @import "node_modules/bulma/css/bulma.min.css";

  .lds-dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
  }

  .lds-dual-ring:after {
    content: "";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }

  @keyframes lds-dual-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .is-loading-bar {
    height: 0;
    overflow: hidden;

    -webkit-transition: all .3s;
    transition: all .3s;
  }

  .is-loading-bar.is-loading {
      height: 80px;
    }
</style>

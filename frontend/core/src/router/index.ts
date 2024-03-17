import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store";

// Views
import HomeView from '../views/HomeView.vue'
import ProductDetailView from "@/views/ProductDetailView.vue";
import CategoryDetailView from "@/views/CategoryDetailView.vue";
import SearchVue from "@/views/SearchVue.vue";
import CartView from "@/views/CartView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";
import AccountView from "@/views/AccountView.vue";
import CheckoutView from "@/views/CheckoutView.vue";
import SuccessView from "@/views/SuccessView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/sign-up',
      name: 'sign_up',
      component: SignUpView
    },
    {
      path: '/log-in',
      name: 'log_in',
      component: LoginView
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
      meta: {
        requireLogin: true
      }
    },
    {
      path: '/search',
      name: 'search',
      component: SearchVue
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/cart/checkout',
      name: 'checkout',
      component: CheckoutView,
      meta: {
        requireLogin: true
      }
    },
   {
      path: '/cart/success',
      name: 'success',
      component: SuccessView
    },
    {
      path: '/:category_slug/:product_slug',
      name: 'product_detail',
      component: ProductDetailView
    },
    {
      path: '/:category_slug/',
      name: 'category_detail',
      component: CategoryDetailView
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({name: 'log_in', query: { to: to.path }})
  } else {
    next()
  }
})

export default router

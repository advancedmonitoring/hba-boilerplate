import { createRouter, createWebHistory } from 'vue-router'

const ErrorPage = () => import(/* webpackChunkName: "main" */'@/pages/ErrorPage')
const HomeView = () => import(/* webpackChunkName: "main" */'@/pages/Home')
const LoginPage = () => import(/* webpackChunkName: "auth" */'@/pages/Login')

import i18n from '@/shared/translation'

const routes = [
  {
    path: '/auth',
    name: 'auth',
    component: LoginPage,
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/404',
    name: 'notFound',
    component: ErrorPage,
    props: { title: '404', message: i18n.global.t('main.pageNotFound') },
  },
  {
    path: '/403',
    name: 'forbidden',
    component: ErrorPage,
    props: { title: '403', message: i18n.global.t('main.permissionsDenied') },
  },
  { path: '/:pathMatch(.*)*', redirect: '/404' },
]

const router = createRouter({
  history: createWebHistory(process.env.VUE_APP_ROUTE_PATH),
  routes,
})

export default router

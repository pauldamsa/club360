import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    name: 'Login',
    path: '/login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    name: 'ClubMembersPage',
    path: '/club-members',
    component: () => import('@/pages/ClubMembers.vue'),
  },
  {
    name:'ClubMemberDetailsPage',
    path:'/club-members/:full_name',
    component: () => import('@/pages/ClubMemberDetails.vue'),
  },
  {
    name: 'PlannerPage',
    path: '/planner',
    component: () => import('@/pages/PlannerPage.vue'),
  },
  {
    name: 'CoachesPage',
    path: '/coaches',
    component: () => import('@/pages/CoachesPage.vue'),
  },
  {
    name:'CoachDetailsPage',
    path:'/coaches/:id_herbalife',
    component: () => import('@/pages/CoachDetailsPage.vue'),
  },
  {
    name:'VisitsPage',
    path:'/visits',
    component: () => import('@/pages/VisitsPage.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router

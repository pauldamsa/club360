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
    path: '/login',
    name: 'LoginPage',
    component: () => import('@/pages/Login.vue'),
  },
  {
    name: 'ClubMembersPage',
    path: '/club-members',
    component: () => import('@/pages/ClubMembers.vue'),
  },
  {
    name:'ClubMemberDetailsPage',
    path:'/club-members/:id_club_member',
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
  {
    name:'StockPage',
    path:'/stock',
    component: () => import('@/pages/StockPage.vue'),
  },
  {
    name:'StatisticsPage',
    path:'/statistics/club',
    component: () => import('@/pages/StatisticsPage.vue'),
  },
  {
    name:'NetworkPage',
    path:'/statistics/network',
    component: () => import('@/pages/NetworkPage.vue'),
  },
  {
    name:'ProfileClubPage',
    path:'/profile/club',
    component: () => import('@/pages/ProfileClubPage.vue'),
  },
  {
    name:'ClubMemberAttentionPage',
    path:'/members/expire',
    component: () => import('@/pages/ClubMemberAttentionPage.vue'),
  }
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
  
  if (to.name === 'LoginPage' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'LoginPage' && !isLoggedIn) {
    next({ name: 'LoginPage' })
  }else {
    next()
  }
})

export default router

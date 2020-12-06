import Vue from 'vue'
import Router from 'vue-router'
// Main
import PostDetail from '@/components/PostDetail'
import Ping from '@/components/Ping'
import Home from '@/components/Home'
// User
import Overview from '@/components/User/Overview'
import User from '@/components/User/User'
import Followers from '@/components/User/Followers'
import Following from '@/components/User/Following'
import Login from '@/components/User/Auth/Login'
import Register from '@/components/User/Auth/Register'
import Account from '@/components/User/Settings/Account'
import Email from '@/components/User/Settings/Email'
import Notification from '@/components/User/Settings/Notification'
import Profile from '@/components/User/Settings/Profile'
import Settings from '@/components/User/Settings/Settings'

// Post
import UserFollowedsPostsList from '@/components/Post/UserFollowedsPostsList'
import UserPostsList from '@/components/Post/UserPostsList'

// Base
import Alert from '@/components/Base/Alert'
import Member from '@/components/Base/Member'
import Navbar from '@/components/Base/Navbar'
import Pagination from '@/components/Base/Pagination'
import Post from '@/components/Base/Post'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user/:id',
      name: 'User',
      component: User,
      children: [
        { path: '', component: Overview },
        { path: 'overview', name: 'UserOverview', component: Overview },
        { path: 'followers', name: 'UserFollowers', component: Followers },
        { path: 'following', name: 'UserFollowing', component: Following },
        { path: 'posts', name: 'UserPostsList', component: UserPostsList},
        { path: 'followeds-posts', name: 'UserFollowedsPostsList', component: UserFollowedsPostsList }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/posts/:id',
      name: 'PostDetail',
      component: PostDetail
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/settings',
      component: Settings,
      children: [
        { path: '', component: Profile },
        { path: 'profile', name: 'SettingProfile', component: Profile},
        { path: 'account', name: 'SettingAccount', component: Account },
        { path: 'email', name: 'SettingEmail', component: Email },
        { path: 'notification', name: 'SettingNotification', component: Notification}
      ],
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('madblog-token')
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    Vue.toasted.show('Please log in to access this page.', { icon: 'fingerprint' })
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name == 'Login') {
    // User already login, prevent goto login page
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {
    Vue.toasted.error('404: Not Found', { icon: 'fingerprint' })
    if (from.name) {
      next({
        name: from.name
      })
    }
  } else {
    next()
  }
})

export default router

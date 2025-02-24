<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
    <!-- Logo Section -->
    <div class="mb-8 text-center">
      <h1 class="text-4xl font-bold text-blue-600">Club360</h1>
      <p class="text-gray-600 mt-2">Welcome back! Please login to continue.</p>
    </div>

    <Card class="w-full max-w-md bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl border border-gray-100">
      <div class="p-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">Login</h2>
        <form class="space-y-6" @submit.prevent="submit">
          <div class="space-y-2">
            <Input
              required
              name="email"
              type="text"
              placeholder="johndoe@email.com"
              label="Email"
              class="w-full"
              inputclass="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div class="space-y-2">
            <Input
              required
              name="password"
              type="password"
              placeholder="••••••"
              label="Password"
              class="w-full"
              inputclass="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <Button 
            :loading="session.login.loading" 
            variant="solid" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg transition-colors duration-200"
          >
            Sign In
          </Button>
        </form>
      </div>
    </Card>

    <div class="mt-8 text-center text-sm text-gray-600">
      <p>© 2025 Club360. All rights reserved.</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { session } from '../data/session'

function submit(e) {
  let formData = new FormData(e.target)
  session.login.submit({
    email: formData.get('email'),
    password: formData.get('password'),
  })
}
</script>

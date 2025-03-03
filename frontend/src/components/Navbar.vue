<template>
    <div class="bg-white shadow w-full fixed top-0 right-0 z-30">
        <div class="px-4 sm:px-6">
            <div class="flex justify-between h-16">
                <!-- Left side - Logo -->
                <div class="flex items-center">
                    <router-link to="/" class="flex items-center space-x-2">
                        <img src="/club360logo.png" alt="Club 360 Logo" class="h-10 w-auto" />
                        <span class="text-xl font-bold text-gray-900 hover:text-gray-700">Club360</span>
                    </router-link>
                </div>

                <!-- Right side - Avatar and Logout -->
                <div class="flex items-center space-x-4">
                    <span class="text-sm font-medium text-gray-700 hidden md:inline">
                        {{ session.user }}
                    </span>
                    <Avatar
                        :label="session.user"
                        size="md"
                        class="cursor-pointer"
                        @click="handleAvatarClick"
                    />
                    <Button
                        variant="danger"
                        icon="log-out"
                        label="Logout"
                        class="cursor-pointer"
                        @click="handleLogout"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Avatar, Button } from 'frappe-ui';
import { useRouter } from 'vue-router';
import { session } from '../data/session';

const router = useRouter();

function handleAvatarClick() {
    router.push({
        name: 'ProfileClubPage',
        params: { id: session.user_id }
    })

}

function handleLogout() {
    // Add logout logic here
    console.log('Logging out...');
    session.logout.submit();
}
</script>
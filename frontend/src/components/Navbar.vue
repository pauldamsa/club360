<template>
    <div class="bg-white shadow w-full fixed top-0 right-0 z-30">
        <div class="px-4 sm:px-6">
            <div class="flex justify-between h-16">
                <!-- Left side - Logo -->
                <div class="flex items-center">
                    <span class="text-xl font-bold text-gray-900">Club360</span>
                </div>

                <!-- Right side - Avatar and Logout -->
                <div class="flex items-center space-x-4">
                    <span class="text-sm font-medium text-gray-700">
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
    // Add profile navigation or other functionality
    console.log('Avatar clicked');
}

function handleLogout() {
    // Add logout logic here
    console.log('Logging out...');
    session.logout.submit();
}
</script>
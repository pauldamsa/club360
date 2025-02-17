<template>
    <div class="min-h-screen bg-gray-50">
        <div class="flex h-screen overflow-hidden">
            <Sidebar v-if="session.user" />
            <div class="flex-1 flex flex-col w-0">
                <Navbar v-if="session.user" />
                <main class="flex-1 overflow-y-auto">
                    <router-view />
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
import Sidebar from '@/components/Sidebar.vue';
import { session } from './data/session.js';
</script>

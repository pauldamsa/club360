<template>
    <div class="min-h-screen bg-gray-50">
        <div class="flex h-screen overflow-hidden">
            <Sidebar2 v-if="session.user" />
            <div class="flex-1 flex flex-col w-0" :class="{ 'ml-14': true, 'lg:ml-60': true }">
                <Navbar v-if="session.user" />
                <main class="flex-1 overflow-y-auto mt-16">
                    <router-view />
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { watch } from 'vue';
import { useRoute } from 'vue-router';
import { titleMap } from './utils/titleMap';
import Navbar from '@/components/Navbar.vue';
import Sidebar from '@/components/Sidebar.vue';
import Sidebar2 from '@/components/Sidebar2.vue';
import { session } from './data/session.js';

const route = useRoute();

// Watch for route changes and update document title
watch(
    () => route.name,
    (newRouteName) => {
        document.title = titleMap[newRouteName] || titleMap.default;
    },
    { immediate: true }
);
</script>

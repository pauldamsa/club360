<template>
    <div class="min-h-screen bg-gray-50">
        <div class="flex h-screen overflow-hidden">
            <Sidebar2 v-if="session.user" ref="sidebar" />
            <div class="flex-1 flex flex-col w-0" :class="{ 'ml-0 lg:ml-60': true }">
                <div class="relative">
                    <Navbar v-if="session.user" />
                </div>
                <main class="flex-1 overflow-y-auto mt-16">
                    <router-view />
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { watch } from 'vue';
import { useRoute } from 'vue-router';
import { titleMap } from './utils/titleMap';
import Navbar from '@/components/Navbar.vue';
import Sidebar2 from '@/components/Sidebar2.vue';
import { FeatherIcon } from 'frappe-ui';
import { session } from './data/session.js';

const route = useRoute();
const sidebar = ref(null);

function toggleSidebar() {
    if (sidebar.value?.toggleMobileMenu) {
        sidebar.value.toggleMobileMenu();
    }
}

// Watch for route changes and update document title
watch(
    () => route.name,
    (newRouteName) => {
        document.title = titleMap[newRouteName] || titleMap.default;
    },
    { immediate: true }
);
</script>

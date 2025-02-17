<template>
    <!-- Mobile overlay -->
    <div 
        v-if="!isCollapsed && isMobileMenuOpen" 
        class="fixed inset-0 bg-gray-600 bg-opacity-50 transition-opacity lg:hidden"
        @click="closeMobileMenu"
    ></div>

    <div 
        class="fixed inset-y-0 left-0 z-30 transform lg:transform-none lg:opacity-100
               transition duration-300 ease-in-out lg:relative"
        :class="{
            'translate-x-0 opacity-100': isMobileMenuOpen || !isMobile,
            '-translate-x-full opacity-0': !isMobileMenuOpen && isMobile,
            'w-64': !isCollapsed,
            'w-16': isCollapsed
        }"
    >
        <div class="h-full flex flex-col bg-white border-r border-gray-200 shadow-lg">
            <div class="h-full flex flex-col">
                <!-- Logo section -->
                <div class="h-16 flex items-center px-4 border-b border-gray-200 overflow-hidden">
                    <span class="text-xl font-bold text-gray-900 whitespace-nowrap">
                        {{ isCollapsed ? '360' : 'Club 360' }}
                    </span>
                </div>

                <!-- Navigation -->
                <nav class="flex-1 overflow-y-auto p-4 space-y-2">
                    <!-- Home -->
                    <router-link 
                        to="/" 
                        class="flex items-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                        :class="{ 'bg-gray-100': $route.path === '/' }"
                    >
                        <FeatherIcon name="home" class="w-5 h-5" :class="{ 'mr-3': !isCollapsed }" />
                        <span v-show="!isCollapsed">Home</span>
                    </router-link>

                    <!-- Members Section -->
                    <div class="space-y-1">
                        <button
                            @click="toggleMembers"
                            class="w-full flex items-center justify-between px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                        >
                            <div class="flex items-center">
                                <FeatherIcon name="users" class="w-5 h-5" :class="{ 'mr-3': !isCollapsed }" />
                                <span v-show="!isCollapsed">Members</span>
                            </div>
                            <FeatherIcon 
                                v-show="!isCollapsed"
                                :name="showMembers ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        <transition
                            enter-active-class="transition duration-200 ease-out"
                            enter-from-class="transform scale-y-95 opacity-0"
                            enter-to-class="transform scale-y-100 opacity-100"
                            leave-active-class="transition duration-200 ease-in"
                            leave-from-class="transform scale-y-100 opacity-100"
                            leave-to-class="transform scale-y-95 opacity-0"
                        >
                            <div v-show="showMembers && !isCollapsed" class="pl-11 space-y-1 origin-top">
                                <router-link
                                    v-for="(item, index) in memberItems"
                                    :key="index"
                                    :to="item.to"
                                    class="block py-2 px-3 text-sm text-gray-600 rounded-lg hover:bg-gray-100"
                                    :class="{ 'bg-gray-100': $route.path === item.to }"
                                >
                                    {{ item.label }}
                                </router-link>
                            </div>
                        </transition>
                    </div>

                    <!-- Administration Section -->
                    <div class="space-y-1">
                        <button
                            @click="toggleAdmin"
                            class="w-full flex items-center justify-between px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                        >
                            <div class="flex items-center">
                                <FeatherIcon name="settings" class="w-5 h-5" :class="{ 'mr-3': !isCollapsed }" />
                                <span v-show="!isCollapsed">Administration</span>
                            </div>
                            <FeatherIcon 
                                v-show="!isCollapsed"
                                :name="showAdmin ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        <transition
                            enter-active-class="transition duration-200 ease-out"
                            enter-from-class="transform scale-y-95 opacity-0"
                            enter-to-class="transform scale-y-100 opacity-100"
                            leave-active-class="transition duration-200 ease-in"
                            leave-from-class="transform scale-y-100 opacity-100"
                            leave-to-class="transform scale-y-95 opacity-0"
                        >
                            <div v-show="showAdmin && !isCollapsed" class="pl-11 origin-top">
                                <router-link
                                    to="/admin/stock"
                                    class="block py-2 px-3 text-sm text-gray-600 rounded-lg hover:bg-gray-100"
                                    :class="{ 'bg-gray-100': $route.path === '/admin/stock' }"
                                >
                                    Stock
                                </router-link>
                            </div>
                        </transition>
                    </div>
                </nav>

                <!-- Collapse Button - Moved to bottom -->
                <div class="border-t border-gray-200">
                    <button 
                        @click="toggleCollapse" 
                        class="w-full flex items-center justify-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                    >
                        <FeatherIcon 
                            :name="isCollapsed ? 'chevron-right' : 'chevron-left'" 
                            class="w-4 h-4"
                        />
                        <span v-show="!isCollapsed" class="ml-2">Collapse</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Mobile menu button -->
    <button 
        class="fixed bottom-4 right-4 lg:hidden z-40 bg-blue-600 text-white p-3 rounded-full shadow-lg"
        @click="toggleMobileMenu"
    >
        <FeatherIcon 
            :name="isMobileMenuOpen ? 'x' : 'menu'"
            class="w-6 h-6"
        />
    </button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { FeatherIcon } from 'frappe-ui';

const showMembers = ref(false);
const showAdmin = ref(false);
const isCollapsed = ref(false);
const isMobileMenuOpen = ref(false);
const isMobile = ref(false);

const memberItems = [
    { label: 'Visits', to: '/visits' },
    { label: 'Club Members', to: '/club-members' },
    { label: 'Coaches', to: '/coaches' }
];

function toggleMembers() {
    showMembers.value = !showMembers.value;
}

function toggleAdmin() {
    showAdmin.value = !showAdmin.value;
}

function toggleCollapse() {
    isCollapsed.value = !isCollapsed.value;
    if (isMobile.value && !isCollapsed.value) {
        isMobileMenuOpen.value = true;
    }
}

function checkMobile() {
    isMobile.value = window.innerWidth < 1024; // lg breakpoint
    if (isMobile.value) {
        isCollapsed.value = true;
        isMobileMenuOpen.value = false;
    } else {
        isCollapsed.value = false;
    }
}

function toggleMobileMenu() {
    isMobileMenuOpen.value = !isMobileMenuOpen.value;
    if (isMobileMenuOpen.value) {
        isCollapsed.value = false;
    }
}

function closeMobileMenu() {
    isMobileMenuOpen.value = false;
    if (isMobile.value) {
        isCollapsed.value = true;
    }
}

// Handle screen resize
onMounted(() => {
    checkMobile();
    window.addEventListener('resize', checkMobile);
});

onUnmounted(() => {
    window.removeEventListener('resize', checkMobile);
});
</script>
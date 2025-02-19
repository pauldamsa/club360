<template>
    <div
        class="fixed top-16 left-0 h-[calc(100vh-4rem)] flex flex-shrink-0 flex-col bg-white shadow-xl transition-all duration-300 z-40"
        :class="{ 'w-60': !isCollapsed, 'w-14': isCollapsed }"
        v-if="currentRoute"
    >
        <!-- Main content wrapper -->
        <div class="flex-1 overflow-y-auto p-2.5">
			<div class="mt-4 flex flex-col">
				<nav class="flex-1 space-y-1 pb-4 text-base">
                    <router-link 
                        to="/" 
                        class="flex items-center px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                        :class="{ 'bg-gray-100': $route.path === '/' }"
                    >
                        <FeatherIcon name="home" class="w-5 h-5" :class="{ 'mr-3': !isCollapsed }" />
                        <span v-show="!isCollapsed">Home</span>
                    </router-link>
					<!-- Members Section with Dropdown -->
					<div class="w-full">
						<button
							@click="toggleMembers"
							class="w-full flex items-center justify-between px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
							:class="{ 'bg-gray-200/70': isMembersActive }"
						>
							<div class="flex items-center">
								<Users class="h-5 w-5 flex-shrink-0 mr-3" />
								<span v-show="!isCollapsed">Members</span>
							</div>
							<FeatherIcon 
								v-show="!isCollapsed"
								:name="showMembers ? 'chevron-down' : 'chevron-right'" 
								class="w-4 h-4"
							/>
						</button>
						
						<div v-show="showMembers && !isCollapsed" class="mt-1 ml-7 space-y-1">
							<router-link
								v-for="item in membersItems"
								:key="item.path"
								:to="item.path"
								class="block py-2 px-3 text-sm text-gray-600 rounded-lg hover:bg-gray-100"
								:class="{ 'bg-gray-100': $route.path === item.path }"
							>
								{{ item.label }}
							</router-link>
						</div>
					</div>

                    <!-- Administration Section with Dropdown -->
                    <div class="w-full">
                        <button
                            @click="toggleAdmin"
                            class="w-full flex items-center justify-between px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                            :class="{ 'bg-gray-200/70': isAdminActive }"
                        >
                            <div class="flex items-center">
                                <Settings class="h-5 w-5 flex-shrink-0 mr-3" />
                                <span v-show="!isCollapsed">Administration</span>
                            </div>
                            <FeatherIcon 
                                v-show="!isCollapsed"
                                :name="showAdmin ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        
                        <div v-show="showAdmin && !isCollapsed" class="mt-1 ml-7 space-y-1">
                            <router-link
                                v-for="item in adminItems"
                                :key="item.path"
                                :to="item.path"
                                class="block py-2 px-3 text-sm text-gray-600 rounded-lg hover:bg-gray-100"
                                :class="{ 'bg-gray-100': $route.path === item.path }"
                            >
                                {{ item.label }}
                            </router-link>
                        </div>
                    </div>

                    <!-- Statistics Section with Dropdown -->
                    <div class="w-full">
                        <button
                            @click="toggleStats"
                            class="w-full flex items-center justify-between px-3 py-2 text-gray-600 rounded-lg hover:bg-gray-100"
                            :class="{ 'bg-gray-200/70': isStatsActive }"
                        >
                            <div class="flex items-center">
                                <BarChart2 class="h-5 w-5 flex-shrink-0 mr-3" />
                                <span v-show="!isCollapsed">Statistics</span>
                            </div>
                            <FeatherIcon 
                                v-show="!isCollapsed"
                                :name="showStats ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        
                        <div v-show="showStats && !isCollapsed" class="mt-1 ml-7 space-y-1">
                            <router-link
                                v-for="item in statsItems"
                                :key="item.path"
                                :to="item.path"
                                class="block py-2 px-3 text-sm text-gray-600 rounded-lg hover:bg-gray-100"
                                :class="{ 'bg-gray-100': $route.path === item.path }"
                            >
                                {{ item.label }}
                            </router-link>
                        </div>
                    </div>
                    
				</nav>
			</div>
        </div>

        <!-- Collapse button fixed at bottom -->
        <div class="border-t border-gray-200  mt-auto">
            <button 
                @click="toggleCollapse" 
                class="w-full flex items-center justify-center px-3 py-2 text-gray-600 hover:bg-gray-100"
            >
                <FeatherIcon 
                    :name="isCollapsed ? 'chevron-right' : 'chevron-left'" 
                    class="w-4 h-4"
                />
                <span v-show="!isCollapsed" class="ml-2">Collapse</span>
            </button>
        </div>
    </div>
</template>

<script setup>
import { Avatar, FeatherIcon, Tooltip } from 'frappe-ui'
// ...existing imports...

const isCollapsed = ref(false);

// Add responsive handling
function checkScreenSize() {
    isCollapsed.value = window.innerWidth < 1024; // collapse for screens smaller than lg breakpoint
}

// Add lifecycle hooks for screen size checks
onMounted(() => {
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
});

onUnmounted(() => {
    window.removeEventListener('resize', checkScreenSize);
});

function toggleCollapse() {
    isCollapsed.value = !isCollapsed.value;
}

import {
	Building2,
	HomeIcon,
    Users,
    Settings,
    BarChart2
} from 'lucide-vue-next'
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const sidebarItems = ref([
	{
		path: '/',
		label: 'Home',
		icon: HomeIcon,
		name: 'Home',
		current: false,
	}
])

const showMembers = ref(false);
const membersItems = [
    { label: 'Visits', path: '/visits' },
    { label: 'Club Members', path: '/club-members' },
    { label: 'Coaches', path: '/coaches' }
];

const isMembersActive = computed(() => {
    return membersItems.some(item => route.path === item.path);
});

function toggleMembers() {
    showMembers.value = !showMembers.value;
}

const showAdmin = ref(false);
const adminItems = [
    { label: 'Stock', path: '/stock' },
    { label: 'Planner', path: '/planner' }
];

const isAdminActive = computed(() => {
    return adminItems.some(item => route.path === item.path);
});

function toggleAdmin() {
    showAdmin.value = !showAdmin.value;
}

const showStats = ref(false);
const statsItems = [
    { label: 'Club', path: '/statistics/club' }
];

const isStatsActive = computed(() => {
    return statsItems.some(item => route.path === item.path);
});

function toggleStats() {
    showStats.value = !showStats.value;
}

const route = useRoute()
const currentRoute = computed(() => {
	sidebarItems.value.forEach((item) => {
		// check if /<route> or /<route>/<id> is in sidebar item path
		item.current = route.path.match(new RegExp(`^${item.path}(/|$)`))
	})
	return route.path
})
</script>

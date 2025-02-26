<template>
    <!-- Mobile overlay backdrop -->
    <div 
        v-if="isMobileOrTablet && isMobileMenuOpen"
        class="fixed inset-0 bg-black bg-opacity-50 z-30"
        @click="toggleMobileMenu"
    ></div>

    <div
        class="fixed top-16 left-0 h-[calc(100vh-4rem)] w-60 flex flex-shrink-0 flex-col bg-white shadow-xl transition-all duration-300"
        :class="{
            'z-40': isMobileMenuOpen,
            '-translate-x-full': isMobileOrTablet && !isMobileMenuOpen,
            'translate-x-0': !isMobileOrTablet || isMobileMenuOpen
        }"
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
                        <FeatherIcon name="home" class="w-5 h-5 mr-3" />
                        <span>Home</span>
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
									<span>Members</span>
							</div>
							<FeatherIcon 
								:name="showMembers ? 'chevron-down' : 'chevron-right'" 
								class="w-4 h-4"
							/>
						</button>
						
						<div v-show="showMembers" class="mt-1 ml-7 space-y-1">
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
                                <span>Administration</span>
                            </div>
                            <FeatherIcon 
                                :name="showAdmin ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        
                        <div v-show="showAdmin" class="mt-1 ml-7 space-y-1">
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
                                <span>Statistics & Reports</span>
                            </div>
                            <FeatherIcon 
                                :name="showStats ? 'chevron-down' : 'chevron-right'" 
                                class="w-4 h-4"
                            />
                        </button>
                        
                        <div v-show="showStats" class="mt-1 ml-7 space-y-1">
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
    </div>

    <!-- Mobile Menu Button -->
    <button 
        v-if="isMobileOrTablet"
        class="fixed bottom-4 left-4 z-50 p-3 rounded-full bg-white shadow-lg hover:bg-gray-100"
        @click="toggleMobileMenu"
    >
        <FeatherIcon 
            :name="isMobileMenuOpen ? 'x' : 'menu'" 
            class="w-6 h-6 text-gray-600"
        />
    </button>
</template>

<script setup>
import { Avatar, FeatherIcon, Tooltip } from 'frappe-ui'
import { Building2, HomeIcon, Users, Settings, BarChart2 } from 'lucide-vue-next'
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

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
    { label: 'Club', path: '/statistics/club' },
    { label: 'Reports', path: '/statistics/reports' }  // Added Reports menu item
];

const isStatsActive = computed(() => {
    return statsItems.some(item => route.path === item.path);
});

function toggleStats() {
    showStats.value = !showStats.value;
}

const currentRoute = computed(() => {
	sidebarItems.value.forEach((item) => {
		// check if /<route> or /<route>/<id> is in sidebar item path
		item.current = route.path.match(new RegExp(`^${item.path}(/|$)`))
	})
	return route.path
})

const isMobileOrTablet = ref(false);
const isMobileMenuOpen = ref(false);

function checkScreenSize() {
    isMobileOrTablet.value = window.innerWidth < 1024; // lg breakpoint
    if (!isMobileOrTablet.value) {
        isMobileMenuOpen.value = false;
    }
}

function toggleMobileMenu() {
    isMobileMenuOpen.value = !isMobileMenuOpen.value;
}

// Add lifecycle hooks for screen size checks
onMounted(() => {
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
});

onUnmounted(() => {
    window.removeEventListener('resize', checkScreenSize);
});
</script>

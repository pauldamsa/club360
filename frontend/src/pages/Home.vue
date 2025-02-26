<template>
    <div class="p-6">
        <!-- Welcome Section -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-900">Welcome back, {{ session.user }}!</h1>
            <p class="mt-2 text-gray-600">Here's what's happening in your club today</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <Card @click="addVisitDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-4 flex items-center space-x-4">
                    <div class="p-3 bg-green-100 rounded-lg">
                        <CheckSquare class="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                        <h3 class="font-medium">Add Visits</h3>
                        <p class="text-sm text-gray-500">Record member visits</p>
                    </div>
                </div>
            </Card>
            
            <Card @click="addMemberDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-4 flex items-center space-x-4">
                    <div class="p-3 bg-blue-100 rounded-lg">
                        <UserPlus class="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                        <h3 class="font-medium">Add Member</h3>
                        <p class="text-sm text-gray-500">Register a new club member</p>
                    </div>
                </div>
            </Card>

            <Card @click="addCoachDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-4 flex items-center space-x-4">
                    <div class="p-3 bg-purple-100 rounded-lg">
                        <Users class="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                        <h3 class="font-medium">Add Coach</h3>
                        <p class="text-sm text-gray-500">Register a new coach</p>
                    </div>
                </div>
            </Card>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <Card>
                <div class="p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-gray-500 text-sm">Total Visits</h3>
                        <Activity class="w-5 h-5 text-blue-500" />
                    </div>
                    <p class="text-2xl font-semibold">{{ totalVisits }}</p>
                    <p class="text-sm text-gray-500 mt-2">+8% from last month</p>
                </div>
            </Card>

            <Card>
                <div class="p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-gray-500 text-sm">Active Members</h3>
                        <Users class="w-5 h-5 text-green-500" />
                    </div>
                    <p class="text-2xl font-semibold">{{ activeMembersCount }}</p>
                    <p class="text-sm text-gray-500 mt-2">12 new this month</p>
                </div>
            </Card>

            <Card>
                <div class="p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-gray-500 text-sm">Total Referrals</h3>
                        <Users class="w-5 h-5 text-purple-500" />
                    </div>
                    <p class="text-2xl font-semibold">{{ referralsCount }}</p>
                    <p class="text-sm text-gray-500 mt-2">2 new this month</p>
                </div>
            </Card>
        </div>

        <!-- Today's Visits -->
        <Card>
            <div class="p-4">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-lg font-medium">Today's Visits</h2>
                    <span class="px-2 py-1 text-sm font-medium bg-blue-100 text-blue-800 rounded-md">
                        Total: {{ allVisitsCount }}
                    </span>
                </div>
                <div class="space-y-4">
                    <div v-if="todayVisits.length === 0" class="text-center text-gray-500 py-4">
                        No visits recorded today
                    </div>
                    <div v-else class="divide-y divide-gray-100">
                        <div v-for="visit in formattedVisits" :key="visit.name" class="flex items-center justify-between py-3">
                            <div class="flex items-center space-x-3">
                                <Avatar :label="memberNames[visit.club_member] || visit.club_member" size="sm" />
                                <div>
                                    <p class="text-sm font-medium text-gray-900">
                                        {{ memberNames[visit.club_member] || visit.club_member }}
                                    </p>
                                    <p class="text-xs text-gray-500">{{ formatTime(visit.date) }}</p>
                                </div>
                            </div>
                            <Badge :label="visit.type_event" variant="solid" class="bg-green-100 text-green-800" />
                        </div>
                    </div>
                </div>
            </div>
        </Card>
    </div>

    <AddMemberDialog ref="addMemberDialog" @memberAdded="handleMemberAdded" />
    <AddCoachDialog ref="addCoachDialog" @coachAdded="handleCoachAdded" />
    <AddVisitDialog ref="addVisitDialog" @visitAdded="handleVisitAdded" />
</template>

<script setup>
import { ref, computed } from 'vue';
import { Card, Dialog, Button, Avatar, Badge, createListResource } from 'frappe-ui';
import { session } from '../data/session';
import AddMemberDialog from '@/components/AddMemberDialog.vue';
import AddCoachDialog from '@/components/AddCoachDialog.vue';
import AddVisitDialog from '@/components/AddVisitDialog.vue';
import { UserPlus, CheckSquare, Users, Activity, CreditCard } from 'lucide-vue-next';
import { formatDistance } from 'date-fns';

const addMemberDialog = ref(null);
const addCoachDialog = ref(null);
const addVisitDialog = ref(null);

// Add members resource to get names
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    auto: true
});

// Create mapping for member names
const memberNames = computed(() => {
    const mapping = {};
    if (membersResource.list.data) {
        membersResource.list.data.forEach(member => {
            mapping[member.name] = member.full_name;
        });
    }
    return mapping;
});

const visitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'club_member', 'type_event', 'date'],
    filters: {
        date: ['>=', new Date().toISOString().split('T')[0]]
    },
    orderBy: 'date desc',
    auto: true
});

const todayVisits = computed(() => visitsResource.list.data || []);

const formattedVisits = computed(() => {
    return todayVisits.value.map(visit => ({
        ...visit,
        date: new Date(visit.date)
    }));
});

function formatTime(date) {
    const baseTime = new Date(date);
    baseTime.setHours(7, 0, 0); // Set time to 7:00 AM
    return formatDistance(baseTime, new Date(), { addSuffix: true });
}

function handleMemberAdded() {
    // Reload members to update the mapping
    membersResource.reload();
    
    // Show success message (optional)
    console.log('Member added successfully');
}

// Add coaches resource for quick updates
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['name', 'full_name'],
    auto: true
});

function handleCoachAdded() {
    // Reload coaches to update any lists/mappings
    coachesResource.reload();
    
    // Show success message (optional)
    console.log('Coach added successfully');
}

// Update visits count resource to only count today's visits
const allVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name'],
    filters: {
        date: ['>=', new Date().toISOString().split('T')[0]]
    },
    auto: true
});

const allVisitsCount = computed(() => {
    return allVisitsResource.list.data?.length || 0;
});

function handleVisitAdded() {
    // Reload visits to update the lists
    visitsResource.reload();
    allVisitsResource.reload();
}

// Add total visits count resource (all-time)
const totalVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name'],
    auto: true
});

const totalVisits = computed(() => {
    return totalVisitsResource.list.data?.length || 0;
});

// Add active members count resource
const activeMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name'],
    filters: {
        status: 'Active'
    },
    auto: true
});

const activeMembersCount = computed(() => {
    return activeMembersResource.list.data?.length || 0;
});

// Add referrals count resource
const referralsResource = createListResource({
    doctype: 'Club Member',
    fields: ['name'],
    filters: {
        source: 'Referral'
    },
    auto: true
});

const referralsCount = computed(() => {
    return referralsResource.list.data?.length || 0;
});
</script>

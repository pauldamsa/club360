<template>
    <div class="p-4 md:p-6">
        <!-- Welcome Section -->
        <div class="mb-6 md:mb-8">
            <h1 class="text-xl md:text-2xl font-bold text-gray-900">Welcome back, {{ session.user }}!</h1>
            <p class="mt-2 text-sm md:text-base text-gray-600">Here's what's happening in your club today</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 mb-6 md:mb-8">
            <Card @click="addVisitDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-3 md:p-4 flex items-center space-x-3 md:space-x-4">
                    <div class="p-2 md:p-3 bg-green-100 rounded-lg">
                        <CheckSquare class="w-5 h-5 md:w-6 md:h-6 text-green-600" />
                    </div>
                    <div>
                        <h3 class="font-medium text-sm md:text-base">Add Visits</h3>
                        <p class="text-xs md:text-sm text-gray-500">Record member visits</p>
                    </div>
                </div>
            </Card>
            
            <Card @click="addMemberDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-3 md:p-4 flex items-center space-x-3 md:space-x-4">
                    <div class="p-2 md:p-3 bg-blue-100 rounded-lg">
                        <UserPlus class="w-5 h-5 md:w-6 md:h-6 text-blue-600" />
                    </div>
                    <div>
                        <h3 class="font-medium text-sm md:text-base">Add Member</h3>
                        <p class="text-xs md:text-sm text-gray-500">Register a new club member</p>
                    </div>
                </div>
            </Card>

            <Card @click="addCoachDialog.openDialog()" class="cursor-pointer hover:shadow-lg transition-shadow">
                <div class="p-3 md:p-4 flex items-center space-x-3 md:space-x-4">
                    <div class="p-2 md:p-3 bg-purple-100 rounded-lg">
                        <Users class="w-5 h-5 md:w-6 md:h-6 text-purple-600" />
                    </div>
                    <div>
                        <h3 class="font-medium text-sm md:text-base">Add Coach</h3>
                        <p class="text-xs md:text-sm text-gray-500">Register a new coach</p>
                    </div>
                </div>
            </Card>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-6 mb-6 md:mb-8">
            <Card>
                <div class="p-3 md:p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-xs md:text-sm text-gray-500">Total Visits</h3>
                        <Activity class="w-4 h-4 md:w-5 md:h-5 text-blue-500" />
                    </div>
                    <p class="text-xl md:text-2xl font-semibold">{{ totalVisits }}</p>
                    <p class="text-xs md:text-sm text-gray-500 mt-1 md:mt-2">
                        average visits in last 3 months: {{ averageVisits }}
                    </p>
                </div>
            </Card>

            <Card>
                <div class="p-3 md:p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-xs md:text-sm text-gray-500">Active Members</h3>
                        <Users class="w-4 h-4 md:w-5 md:h-5 text-green-500" />
                    </div>
                    <p class="text-xl md:text-2xl font-semibold">{{ activeMembersCount }}</p>
                    <p class="text-xs md:text-sm text-gray-500 mt-1 md:mt-2">{{ newMembersCount }} new this month</p>
                </div>
            </Card>

            <Card>
                <div class="p-3 md:p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-xs md:text-sm text-gray-500">Total Referrals</h3>
                        <Users class="w-4 h-4 md:w-5 md:h-5 text-purple-500" />
                    </div>
                    <p class="text-xl md:text-2xl font-semibold">{{ referralsCount }}</p>
                    <p class="text-xs md:text-sm text-gray-500 mt-1 md:mt-2">{{ newReferralsCount }} new this month</p>
                </div>
            </Card>
        </div>

        <!-- Today's Visits -->
        <Card>
            <div class="p-3 md:p-4">
                <div class="flex items-center justify-between mb-3 md:mb-4">
                    <h2 class="text-base md:text-lg font-medium">Today's Visits</h2>
                    <span class="px-2 py-1 text-xs md:text-sm font-medium bg-blue-100 text-blue-800 rounded-md">
                        Total: {{ allVisitsCount }}
                    </span>
                </div>
                <div class="space-y-3 md:space-y-4">
                    <div v-if="todayVisits.length === 0" class="text-center text-gray-500 py-4 text-sm md:text-base">
                        No visits recorded today
                    </div>
                    <div v-else class="divide-y divide-gray-100">
                        <div v-for="visit in formattedVisits" 
                             :key="visit.name" 
                             class="flex items-center justify-between py-2 md:py-3"
                        >
                            <div class="flex items-center space-x-2 md:space-x-3">
                                <Avatar :label="memberNames[visit.club_member] || visit.club_member" 
                                      size="sm" 
                                />
                                <div>
                                    <p class="text-xs md:text-sm font-medium text-gray-900">
                                        {{ memberNames[visit.club_member] || visit.club_member }}
                                    </p>
                                    <p class="text-xs text-gray-500">{{ formatTime(visit.date) }}</p>
                                </div>
                            </div>
                            <Badge 
                                :label="visit.type_event" 
                                variant="solid" 
                                class="text-xs md:text-sm bg-green-100 text-green-800" 
                            />
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
    filters: {
        owner: session.user
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
    auto: true
});


const visitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'club_member', 'type_event', 'date'],
    filters: {
        owner: session.user,
        date: ['>=', new Date().toISOString().split('T')[0]]
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
    orderBy: 'date desc',
    auto: true
});

// Add detailed members resource to get full names
const membersDetailsResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name'],
    filters: {
        owner: session.user
    },
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
    auto: true
});

// Create mapping for member names
const memberNames = computed(() => {
    const mapping = {};
    if (membersDetailsResource.list.data) {
        membersDetailsResource.list.data.forEach(member => {
            mapping[member.name] = member.full_name;
        });
    }
    return mapping;
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
}

// Add coaches resource for quick updates
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['name', 'full_name'],
    auto: true,
    pageLength: 9999, // Increase page length to get all records
    limit: 0, // No limit on the number of records
});

function handleCoachAdded() {
    // Reload coaches to update any lists/mappings
    coachesResource.reload();
}

// Update visits count resource to only count today's visits
const allVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name'],
    filters: {
        owner: session.user,
        date: ['>=', new Date().toISOString().split('T')[0]] 
    },
    pageLength: 99999, // Set a large number to get all records
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

// Update total visits count resource to get all records
const totalVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name'],
    filters: {
        owner: session.user
    },
    pageLength: 99999, // Set a large number to get all records
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
        owner: session.user,
        status: 'Active'
    },
    pageLength: 99999, // Set a large number to get all records
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
        owner: session.user,
        source: 'Referral'
    },
    pageLength: 99999, // Set a large number to get all records
    auto: true
});

const referralsCount = computed(() => {
    return referralsResource.list.data?.length || 0;
});

// Add resource for this month's referrals
const newReferralsResource = createListResource({
    doctype: 'Club Member',
    fields: ['name'],
    filters: {
        owner: session.user,
        source: 'Referral',
        creation: ['>=', new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0]]
    },
    pageLength: 99999, // Set a large number to get all records
    auto: true
});

const newReferralsCount = computed(() => {
    return newReferralsResource.list.data?.length || 0;
});

// Add resource for new members this month
const newMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name'],
    filters: {
        owner: session.user,
        creation: ['>=', new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0]]
    },
    pageLength: 99999, // Set a large number to get all records
    auto: true
});

const newMembersCount = computed(() => {
    return newMembersResource.list.data?.length || 0;
});

// Add resource for last 3 months visits
const lastThreeMonthsVisitsResource = createListResource({
    doctype: 'Visit',
    fields: ['name', 'date'],
    filters: {
        owner: session.user,
        date: ['>=', new Date(new Date().setMonth(new Date().getMonth() - 3)).toISOString().split('T')[0]]
    },
    pageLength: 99999, // Set a large number to get all records
    auto: true
});

const averageVisits = computed(() => {
    if (!lastThreeMonthsVisitsResource.list.data) return 0;
    
    const visits = lastThreeMonthsVisitsResource.list.data.length;
    const months = 3;
    return Math.round(visits / months);
});
</script>

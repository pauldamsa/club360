<template>
    <div class="p-6">
        <!-- Welcome Section -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-900">Welcome back, {{ session.user }}!</h1>
            <p class="mt-2 text-gray-600">Here's what's happening in your club today</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card class="cursor-pointer hover:shadow-lg transition-shadow">
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
                    <p class="text-2xl font-semibold">1,000</p>
                    <p class="text-sm text-gray-500 mt-2">+8% from last month</p>
                </div>
            </Card>

            <Card>
                <div class="p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-gray-500 text-sm">Active Members</h3>
                        <Users class="w-5 h-5 text-green-500" />
                    </div>
                    <p class="text-2xl font-semibold">100</p>
                    <p class="text-sm text-gray-500 mt-2">12 new this month</p>
                </div>
            </Card>

            <Card>
                <div class="p-4">
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-gray-500 text-sm">Active Memberships</h3>
                        <CreditCard class="w-5 h-5 text-purple-500" />
                    </div>
                    <p class="text-2xl font-semibold">300</p>
                    <p class="text-sm text-gray-500 mt-2">5 expiring soon</p>
                </div>
            </Card>
        </div>

        <!-- Today's Visits -->
        <Card>
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Today's Visits</h2>
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
    <AddCoachDialog ref="addCoachDialog" />
</template>

<script setup>
import { ref, computed } from 'vue';
import { Card, Dialog, Button, Avatar, Badge, createListResource } from 'frappe-ui';
import { session } from '../data/session';
import AddMemberDialog from '@/components/AddMemberDialog.vue';
import AddCoachDialog from '@/components/AddCoachDialog.vue';
import { UserPlus, CheckSquare, Users, Activity, CreditCard } from 'lucide-vue-next';
import { formatDistance } from 'date-fns';

const addMemberDialog = ref(null);
const addCoachDialog = ref(null);

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
    return formatDistance(date, new Date(), { addSuffix: true });
}

function handleMemberAdded() {
    // Handle successful member addition
    console.log('Member added successfully');
}
</script>

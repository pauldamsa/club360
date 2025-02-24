<template>
    <div class="p-6">
        <!-- Welcome Section -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-900">Welcome back, {{ session.user }}!</h1>
            <p class="mt-2 text-gray-600">Here's what's happening in your club today</p>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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

        <!-- Recent Activity -->
        <Card>
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Recent Activity</h2>
                <div class="space-y-4">
                    <div v-for="(activity, index) in recentActivities" :key="index" class="flex items-center space-x-4">
                        <div class="p-2 rounded-full" :class="activity.bgColor">
                            <component :is="activity.icon" class="w-4 h-4" :class="activity.iconColor" />
                        </div>
                        <div>
                            <p class="text-sm font-medium">{{ activity.text }}</p>
                            <p class="text-xs text-gray-500">{{ activity.time }}</p>
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
import { ref } from 'vue';
import { Card, Dialog, Button } from 'frappe-ui';
import { session } from '../data/session';
import AddMemberDialog from '@/components/AddMemberDialog.vue';
import AddCoachDialog from '@/components/AddCoachDialog.vue';
import { UserPlus, CheckSquare, Users, Activity, CreditCard } from 'lucide-vue-next';

const addMemberDialog = ref(null);
const addCoachDialog = ref(null);

const recentActivities = [
    {
        icon: CheckSquare,
        text: 'John Doe completed their visit',
        time: '2 minutes ago',
        bgColor: 'bg-green-100',
        iconColor: 'text-green-600'
    },
    {
        icon: UserPlus,
        text: 'New member Jane Smith registered',
        time: '1 hour ago',
        bgColor: 'bg-blue-100',
        iconColor: 'text-blue-600'
    },
    {
        icon: CreditCard,
        text: 'Mike Johnson renewed membership',
        time: '3 hours ago',
        bgColor: 'bg-purple-100',
        iconColor: 'text-purple-600'
    }
];

function handleMemberAdded() {
    // Handle successful member addition
    console.log('Member added successfully');
}
</script>

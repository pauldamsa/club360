<template>
    <div class="p-6 space-y-6">
        <!-- Overview Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card class="bg-white">
                <div class="p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Members</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-2xl font-semibold">{{ stats.totalMembers }}</div>
                        <FeatherIcon name="users" class="w-8 h-8 text-blue-500" />
                    </div>
                    <div class="mt-2 text-sm text-gray-600">
                        Active: {{ stats.activeMembers }}
                    </div>
                </div>
            </Card>

            <Card class="bg-white">
                <div class="p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Coaches</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-2xl font-semibold">{{ stats.totalCoaches }}</div>
                        <FeatherIcon name="user-check" class="w-8 h-8 text-green-500" />
                    </div>
                    <div class="mt-2 text-sm text-gray-600">
                        Active: {{ stats.activeCoaches }}
                    </div>
                </div>
            </Card>

            <Card class="bg-white">
                <div class="p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Visits</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-2xl font-semibold">{{ stats.totalVisits }}</div>
                        <FeatherIcon name="check-square" class="w-8 h-8 text-purple-500" />
                    </div>
                    <div class="mt-2 text-sm text-gray-600">
                        This Month: {{ stats.visitsThisMonth }}
                    </div>
                </div>
            </Card>

            <Card class="bg-white">
                <div class="p-4">
                    <h3 class="text-sm font-medium text-gray-500">Active Memberships</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-2xl font-semibold">{{ stats.activeMemberships }}</div>
                        <FeatherIcon name="credit-card" class="w-8 h-8 text-yellow-500" />
                    </div>
                    <div class="mt-2 text-sm text-gray-600">
                        Expiring Soon: {{ stats.expiringSoonMemberships }}
                    </div>
                </div>
            </Card>
        </div>

        <!-- Visits Chart -->
        <Card class="bg-white">
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Visits Trend</h2>
                <div class="h-64">
                    <!-- Add your chart component here -->
                    <div class="text-center text-gray-500">Chart Coming Soon</div>
                </div>
            </div>
        </Card>

        <!-- Member Sources -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card class="bg-white">
                <div class="p-4">
                    <h2 class="text-lg font-medium mb-4">Member Sources</h2>
                    <table class="min-w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="(count, source) in stats.memberSources" :key="source">
                                <td class="py-2">{{ source }}</td>
                                <td class="py-2 text-right">
                                    <Badge :label="count" />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>

            <!-- Stock Overview -->
            <Card class="bg-white">
                <div class="p-4">
                    <h2 class="text-lg font-medium mb-4">Current Stock</h2>
                    <table class="min-w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="(stock, product) in stats.currentStock" :key="product">
                                <td class="py-2">{{ product }}</td>
                                <td class="py-2 text-right">
                                    <Badge 
                                        :label="stock"
                                        :variant="stock < 10 ? 'danger' : 'solid'"
                                    />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Card, Badge, FeatherIcon, createResource } from 'frappe-ui';

const stats = ref({
    totalMembers: 0,
    activeMembers: 0,
    totalCoaches: 0,
    activeCoaches: 0,
    totalVisits: 0,
    visitsThisMonth: 0,
    activeMemberships: 0,
    expiringSoonMemberships: 0,
    memberSources: {
        'Facebook': 0,
        'Instagram': 0,
        'Referral': 0,
        'Active Contact': 0,
        'Roadshow': 0
    },
    currentStock: {
        'Formula 1': 0,
        'Herbal Tea': 0,
        'Aloe': 0,
        'PDM': 0
    }
});

const statisticsResource = createResource({
    url: 'club360.api.get_dashboard_statistics',
    onSuccess: (data) => {
        stats.value = data;
    }
});

onMounted(() => {
    statisticsResource.submit();
});
</script>
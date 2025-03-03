<template>
    <div class="p-4 md:p-6 space-y-4 md:space-y-6">
        <!-- Overview Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
            <!-- Total Members Card -->
            <Card class="bg-white">
                <div class="p-3 md:p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Members</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-xl md:text-2xl font-semibold">{{ stats.totalMembers }}</div>
                        <FeatherIcon name="users" class="w-6 h-6 md:w-8 md:h-8 text-blue-500" />
                    </div>
                    <div class="mt-2 text-xs md:text-sm text-gray-600">
                        Active: {{ stats.activeMembers }}
                    </div>
                </div>
            </Card>

            <Card class="bg-white">
                <div class="p-3 md:p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Visits</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-xl md:text-2xl font-semibold">{{ stats.totalVisits }}</div>
                        <FeatherIcon name="check-square" class="w-6 h-6 md:w-8 md:h-8 text-purple-500" />
                    </div>
                    <div class="mt-2 text-xs md:text-sm text-gray-600">
                        This Month: {{ stats.visitsThisMonth }}
                    </div>
                </div>
            </Card>

            <Card class="bg-white">
                <div class="p-3 md:p-4">
                    <h3 class="text-sm font-medium text-gray-500">Total Coaches</h3>
                    <div class="mt-2 flex items-center justify-between">
                        <div class="text-xl md:text-2xl font-semibold">{{ stats.totalCoaches }}</div>
                        <FeatherIcon name="award" class="w-6 h-6 md:w-8 md:h-8 text-yellow-500" />
                    </div>
                </div>
            </Card>
             <!-- Member Sources -->
            <Card class="bg-white sm:col-span-2 lg:col-span-1">
                <div class="p-3 md:p-4">
                    <h2 class="text-base md:text-lg font-medium mb-3 md:mb-4">Member Sources</h2>
                    <div class="overflow-x-auto">
                        <table class="min-w-full">
                            <thead>
                                <tr class="text-xs md:text-sm text-gray-500 border-b">
                                    <th class="text-left pb-2">Source</th>
                                    <th class="text-right pb-2">Total</th>
                                    <th class="text-right pb-2">This Month</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr v-for="(counts, source) in stats.memberSources" :key="source" class="text-sm">
                                    <td class="py-2">{{ source }}</td>
                                    <td class="py-2 text-right">
                                        <Badge :label="counts.total" class="text-xs md:text-sm" />
                                    </td>
                                    <td class="py-2 text-right">
                                        <Badge 
                                            :label="counts.thisMonth" 
                                            :class="[
                                                counts.thisMonth > 0 ? 'bg-green-100 text-green-800' : '',
                                                'text-xs md:text-sm'
                                            ]"
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </Card>
        </div>

        <!-- Visits Chart -->
        <Card class="bg-white">
            <div class="p-3 md:p-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0 mb-4">
                    <h2 class="text-base md:text-lg font-medium">Daily Visits</h2>
                    <select 
                        v-model="selectedMonth" 
                        class="rounded-md border-gray-300 w-full sm:w-auto"
                        @change="loadChart"
                    >
                        <option v-for="month in lastSixMonths" :key="month.value" :value="month.value">
                            {{ month.label }}
                        </option>
                    </select>
                </div>
                <div class="h-[300px] md:h-[500px]"> 
                    <canvas ref="chartRef"></canvas>
                </div>
            </div>
        </Card>

        <!-- New Members Chart -->
        <Card class="bg-white">
            <div class="p-3 md:p-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0 mb-4">
                    <h2 class="text-base md:text-lg font-medium">New Members Trend</h2>
                    <select 
                        v-model="selectedMembersMonth" 
                        class="rounded-md border-gray-300 w-full sm:w-auto"
                        @change="loadMembersChart"
                    >
                        <option v-for="month in lastSixMonths" :key="month.value" :value="month.value">
                            {{ month.label }}
                        </option>
                    </select>
                </div>
                <div class="h-[300px] md:h-[500px]"> 
                    <canvas ref="membersChartRef"></canvas>
                </div>
            </div>
        </Card>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { Card, Badge, FeatherIcon, createResource } from 'frappe-ui';
import { 
    Chart as ChartJS, 
    CategoryScale, 
    LinearScale, 
    PointElement, 
    LineElement, 
    Title, 
    Tooltip, 
    Legend,
    LineController,
    BarController,
    BarElement
} from 'chart.js';

ChartJS.register(
    CategoryScale, 
    LinearScale, 
    PointElement, 
    LineElement, 
    Title, 
    Tooltip, 
    Legend,
    LineController,
    BarController,
    BarElement
);


const stats = ref({
    totalMembers: 0,
    activeMembers: 0,
    totalCoaches: 0,
    totalVisits: 0,
    visitsThisMonth: 0,
    activeMemberships: 0,
    expiringSoonMemberships: 0,
    memberSources: {
        'Facebook': { total: 0, thisMonth: 0 },
        'Instagram': { total: 0, thisMonth: 0 },
        'Referral': { total: 0, thisMonth: 0 },
        'Active Contact': { total: 0, thisMonth: 0 },
        'Roadshow': { total: 0, thisMonth: 0 }
    }
});

const chartRef = ref(null);
let chart = ref(null);

const selectedMonth = ref(new Date().toISOString().slice(0, 7)); // Format: YYYY-MM

// Updated lastSixMonths computed
const lastSixMonths = computed(() => {
    const months = [];
    const date = new Date();
    
    // Get current month in YYYY-MM format and set as default
    const currentMonth = date.toISOString().slice(0, 7);
    selectedMonth.value = currentMonth;
    
    // Start from current month and go backwards
    for (let i = 0; i < 6; i++) {
        // Fix: Create new date for each iteration to avoid mutation
        const currentDate = new Date();
        // Fix: Set to first day of month to avoid date issues
        currentDate.setDate(1);
        // Fix: Use setMonth instead of calculating with subtraction
        currentDate.setMonth(currentDate.getMonth() - i);
        
        const monthValue = currentDate.toISOString().slice(0, 7);
        months.push({
            label: currentDate.toLocaleString('en', { month: 'long', year: 'numeric' }),
            value: monthValue
        });
    }
    return months;
});

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                stepSize: 1
            },
            title: {
                display: true,
                text: 'Number of Visits'
            }
        },
        x: {
            title: {
                display: true,
                text: 'Day of Month'
            }
        }
    },
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            callbacks: {
                title: (items) => {
                    return `Day ${items[0].label}`;
                }
            }
        }
    }
};

const statisticsResource = createResource({
    url: 'club360.api.get_dashboard_statistics',
    onSuccess: (data) => {
        stats.value = data;
    }
});

const visitsTrendResource = createResource({
    url: 'club360.api.get_visits_trend',
    makeParams: () => ({
        month: selectedMonth.value  // This will now be in YYYY-MM format
    }),
    onSuccess: (data) => {
        updateChart(data);
    }
});

function updateChart(data) {
    if (chart.value) {
        chart.value.destroy();
    }
    const ctx = chartRef.value.getContext('2d');
    chart.value = new ChartJS(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Visits',
                data: data.values,
                fill: false,
                borderColor: '#4F46E5',
                tension: 0.3
            }]
        },
        options: chartOptions
    });
}

// Modify loadChart to be simpler
function loadChart() {
    visitsTrendResource.submit();
}

const membersChartRef = ref(null);
let membersChart = ref(null);
const selectedMembersMonth = ref(new Date().toISOString().slice(0, 7));

const membersChartOptions = {
    ...chartOptions,
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                stepSize: 1
            },
            title: {
                display: true,
                text: 'Number of New Club Members'  // Changed from 'Number of Visits'
            }
        },
        x: {
            title: {
                display: true,
                text: 'Weeks'
            }
        }
    }
};

const newMembersTrendResource = createResource({
    url: 'club360.api.get_new_members_trend',
    makeParams: () => ({
        month: selectedMembersMonth.value
    }),
    onSuccess: (data) => {
        updateMembersChart(data);
    }
});

function updateMembersChart(data) {
    if (membersChart.value) {
        membersChart.value.destroy();
    }
    
    const ctx = membersChartRef.value.getContext('2d');
    membersChart.value = new ChartJS(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'New Members',
                data: data.values,
                fill: false,
                borderColor: '#10B981', // Green color
                tension: 0.3
            }]
        },
        options: membersChartOptions
    });
}

function loadMembersChart() {
    newMembersTrendResource.submit();
}

onMounted(() => {
    statisticsResource.submit();
    loadChart(); // Initial load
    loadMembersChart(); // Initial load for members chart
});

onBeforeUnmount(() => {
    if (chart.value) {
        chart.value.destroy();
    }
    if (membersChart.value) {
        membersChart.value.destroy();
    }
});
</script>
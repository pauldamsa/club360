<template>
    <div class="p-6 space-y-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <h1 class="text-2xl font-bold text-gray-900">Network Hierarchy Report</h1>
            <div class="flex flex-col sm:flex-row gap-4">
                <FormControl
                    type="autocomplete"
                    :options="coachOptions"
                    placeholder="Select Coach"
                    v-model="selectedCoach"
                    class="w-64"
                />
                <FormControl
                    type="select"
                    :options="monthOptions"
                    placeholder="Select Month"
                    v-model="selectedMonth"
                    class="w-48"
                />
                <Button 
                    variant="solid"
                    label="Generate"
                    :loading="reportResource.loading"
                    @click="loadReport"
                />
            </div>
        </div>

        <Card class="bg-white">
            <div class="p-4">
                <div v-if="!networkData.length" class="text-center py-8 text-gray-500">
                    No data available. Please generate a report.
                </div>
                <div v-else class="space-y-4">
                    <NetworkNode 
                        v-for="node in networkData" 
                        :key="node.id"
                        :node="node"
                        :expanded-nodes="expandedNodes"
                        @toggle="toggleNode"
                        class="border rounded-lg"
                    />
                </div>
            </div>
        </Card>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Card, FormControl, Button, createResource, createListResource } from 'frappe-ui';
import { format } from 'date-fns';
import NetworkNode from '../components/NetworkNode.vue';
import { session } from '../data/session';

// Coach options resource
const coachResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name'],
    filters: {
        owner: session.user
    },
    auto: true,
});

const coachOptions = computed(() => {
    if (!coachResource.list.data) return [];
    return [
        { label: 'All Coaches', value: '' },
        ...coachResource.list.data.map(coach => ({
            label: coach.full_name,
            value: coach.id_herbalife
        }))
    ];
});

// Month options with current month selected
const monthOptions = computed(() => {
    const options = [];
    const today = new Date();
    
    for (let i = 0; i < 6; i++) {
        const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
        options.push({
            label: format(date, 'MMMM yyyy'),
            value: format(date, 'yyyy-MM-dd')
        });
    }
    
    return [
        { label: 'All Time', value: '' },
        ...options
    ];
});

const selectedCoach = ref('');
const selectedMonth = ref(format(new Date(), 'yyyy-MM-dd')); // Current month selected
const networkData = ref([]);
const expandedNodes = ref(new Set()); // Track expanded nodes

const reportResource = createResource({
    url: 'club360.api.get_network_hierarchy',
    makeParams: () => ({
        filters: {
            coach: selectedCoach.value,
            date: selectedMonth.value
        }
    }),
    onSuccess: (data) => {
        networkData.value = data;
        // Expand first level by default
        data.forEach(node => expandedNodes.value.add(node.id));
    }
});

function loadReport() {
    expandedNodes.value.clear(); // Reset expanded state
    reportResource.submit();
}

function toggleNode(nodeId) {
    if (expandedNodes.value.has(nodeId)) {
        expandedNodes.value.delete(nodeId);
    } else {
        expandedNodes.value.add(nodeId);
    }
}

// Initial load
loadReport();
</script>
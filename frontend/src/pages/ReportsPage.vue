<template>
    <div class="p-6 space-y-6">
        <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold text-gray-900">Network Hierarchy</h1>
        </div>

        <Card class="bg-white">
            <div class="p-4">
                <div v-if="!networkData.length" class="text-center py-8 text-gray-500">
                    No network data available.
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
import { ref, onMounted } from 'vue';
import { Card, createResource } from 'frappe-ui';
import NetworkNode from '../components/NetworkNode.vue';

const networkData = ref([]);
const expandedNodes = ref(new Set());

const networkResource = createResource({
    url: 'club360.api.get_network_hierarchy',
    onSuccess: (data) => {
        networkData.value = data;
        // Expand first level by default
        data.forEach(node => expandedNodes.value.add(node.id));
    }
});

function toggleNode(nodeId) {
    if (expandedNodes.value.has(nodeId)) {
        expandedNodes.value.delete(nodeId);
    } else {
        expandedNodes.value.add(nodeId);
    }
}

onMounted(() => {
    networkResource.submit();
});
</script>
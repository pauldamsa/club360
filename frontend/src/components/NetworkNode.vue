<template>
    <div class="network-node">
        <div 
            class="flex flex-col sm:flex-row sm:items-center justify-between p-3 md:p-4 cursor-pointer hover:bg-gray-50"
            @click="$emit('toggle', node.id)"
        >
            <!-- Main Info -->
            <div class="flex items-center space-x-3 mb-2 sm:mb-0">
                <FeatherIcon 
                    :name="getNodeIcon"
                    class="w-5 h-5 flex-shrink-0"
                    :class="getNodeColorClass"
                />
                <span class="font-medium truncate">{{ node.name }}</span>
            </div>

            <!-- Badges -->
            <div class="flex flex-wrap items-center gap-2">
                <Badge 
                    v-if="node.type === 'coach'"
                    :label="`Level ${node.level}`"
                    class="bg-yellow-100 text-yellow-800 text-xs"
                />
                <Badge 
                    v-else
                    :label="node.status"
                    :class="[getStatusClass, 'text-xs']"
                />
                <Badge 
                    v-if="node.direct_count > 0"
                    :label="`${node.direct_count} direct`"
                    class="bg-blue-100 text-blue-800 text-xs"
                />
                <Badge 
                    v-if="node.total_count > node.direct_count"
                    :label="`${node.total_count} total`"
                    class="bg-purple-100 text-purple-800 text-xs"
                />
                <span v-if="node.date" class="text-xs text-gray-500 hidden sm:inline">
                    {{ formatDate(node.date) }}
                </span>
                <FeatherIcon 
                    v-if="node.children?.length"
                    :name="isExpanded ? 'chevron-down' : 'chevron-right'" 
                    class="w-5 h-5 text-gray-400 ml-auto sm:ml-0"
                />
            </div>
        </div>

        <div 
            v-if="isExpanded && node.children?.length" 
            class="pl-4 sm:pl-8 space-y-2 pb-2 border-l-2"
        >
            <NetworkNode 
                v-for="child in node.children"
                :key="child.id"
                :node="child"
                :expanded-nodes="expandedNodes"
                @toggle="$emit('toggle', $event)"
            />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { Badge, FeatherIcon } from 'frappe-ui';
import { format } from 'date-fns';

const props = defineProps({
    node: {
        type: Object,
        required: true
    },
    expandedNodes: {
        type: Set,
        required: true
    }
});

defineEmits(['toggle']);

const isExpanded = computed(() => props.expandedNodes.has(props.node.id));

const getNodeIcon = computed(() => {
    if (props.node.type === 'coach') return 'award';
    return 'user';
});

const getNodeColorClass = computed(() => {
    if (props.node.type === 'coach') return 'text-yellow-500';
    return 'text-blue-500';
});

const getStatusClass = computed(() => ({
    'bg-green-100 text-green-800': props.node.status === 'Active',
    'bg-red-100 text-red-800': props.node.status === 'Inactive',
    'bg-yellow-100 text-yellow-800': props.node.status === 'Pending'
}));

function formatDate(date) {
    return format(new Date(date), 'MMM d, yyyy');
}
</script>

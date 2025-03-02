<template>
    <div class="network-node">
        <div 
            class="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50"
            @click="$emit('toggle', node.id)"
        >
            <div class="flex items-center space-x-3">
                <FeatherIcon 
                    :name="getNodeIcon"
                    class="w-5 h-5"
                    :class="getNodeColorClass"
                />
                <span class="font-medium">{{ node.name }}</span>
                <div class="flex items-center space-x-2">
                    <Badge 
                        v-if="node.type === 'coach'"
                        :label="`Level ${node.level}`"
                        class="bg-yellow-100 text-yellow-800"
                    />
                    <Badge 
                        v-else
                        :label="node.status"
                        :class="getStatusClass"
                    />
                    <Badge 
                        v-if="node.children?.length"
                        :label="`${node.direct_count} direct`"
                        class="bg-blue-100 text-blue-800"
                    />
                    <Badge 
                        v-if="node.total_count > node.direct_count"
                        :label="`${node.total_count} total`"
                        class="bg-purple-100 text-purple-800"
                    />
                </div>
                <span v-if="!node.type.includes('coach')" class="text-sm text-gray-500">
                    {{ formatDate(node.date) }}
                </span>
            </div>
            <FeatherIcon 
                v-if="node.children?.length"
                :name="isExpanded ? 'chevron-down' : 'chevron-right'" 
                class="w-5 h-5 text-gray-400"
            />
        </div>

        <div v-if="isExpanded && node.children?.length" class="pl-8 space-y-2 pb-2">
            <NetworkNode 
                v-for="child in node.children"
                :key="child.id"
                :node="child"
                :expanded-nodes="expandedNodes"
                @toggle="$emit('toggle', $event)"
                class="border-l-2"
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
    if (props.node.type === 'direct') return 'user';
    return 'user-plus';
});

const getNodeColorClass = computed(() => {
    if (props.node.type === 'coach') return 'text-yellow-500';
    if (props.node.type === 'direct') return 'text-blue-500';
    return {
        'text-green-500': props.node.type.includes('level_1'),
        'text-purple-500': props.node.type.includes('level_2'),
        'text-orange-500': props.node.type.includes('level_3'),
        'text-red-500': props.node.type.includes('level_4'),
        'text-pink-500': props.node.type.includes('level_5')
    };
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
